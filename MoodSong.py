import webbrowser
import urllib
import json
import os
# from googlesearch import search
from googleapiclient.discovery import build
from google_auth_oauthlib import flow
import googleapiclient.errors
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# USER INPUT
mood = input("What is the mood or occasion? Please use a single word to describe e.g. driving: ")
not_one_word = " " in mood or "_" in mood or "-" in mood
while not_one_word:
    mood = input("Please use a single word to describe (no spaces, underscores, or hyphens): ")

mood = mood.lower()
# search = search(query, tld='com', lang='en', num=10,start=0, stop=10, pause=2.0)
# if youtube links are not present print("No results found") else run everything below
playlist_name = 'auto-generated-' + mood + '-playlist'

# AUTHENTICATING
print("Authenticating...")
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

service_name = 'youtube'
service_version = 'v3'
secrets = "Youtube_Client_Secret.json"

flow = flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file=secrets, scopes=scopes)
credentials = flow.run_console()

youtube = build(service_name, service_version, developerKey='AIzaSyCCh0YpqomB8I7P-AHhxWWwyhy3CXvG7Ks', credentials=credentials)

# CREATING PLAYLIST
print("Creating " + playlist_name + "...")

request = youtube.playlists().insert(
    part="snippet",
    body={
        "snippet":{
            "title":playlist_name,
            "description":"Generated using a python script."
        }
    }
)
response = request.execute()
playlist_id = response['id']
playlist_url = 'https://www.youtube.com/playlist?list=' + playlist_id
# print(json.dumps(response, sort_keys=True, indent=4))
# webbrowser.open_new_tab(url)

# FINDING SONGS / VIDEO IDs
print("Finding songs...")
query = mood + " music"

PATH = '..\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://www.google.com/")
# print(driver.title)
search = driver.find_element_by_name('q')
search.send_keys('sad music')
search.send_keys(Keys.RETURN)

urls = []
video_ids = []
try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"main"))
    )
    items = main.find_elements_by_tag_name("a")
    # print("URLs")
    i = 0
    for item in items:
        url = item.get_attribute("href")
        filter = url is not None
        if filter:
            second_filter = 'https://www.google.com/search?q=' in url and 'stick=' in url
            if second_filter:
                # print(str(i + 1) + ".", url)
                urls.append(url)
                i += 1
    # print("VIDEO IDs")
    i = 0
    for url in urls:
        try:
            driver.get(url)

            main = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "search"))
            )
            element = main.find_element_by_tag_name("a")
            possible_video_link = element.get_attribute("href")

            try:
                youtube_video = 'https://www.youtube.com/watch?v=' in possible_video_link

            except:
                youtube_video = False

            if youtube_video:
                index = possible_video_link.find('=') + 1
                id = possible_video_link[index:]

                print("ID #" + str(i + 1) + ": ", id)
                i += 1
                video_ids.append(id)
            else:
                print(str(i + 1) + ". No ID found for:", possible_video_link)
                i += 1
            if i > 29:
                break
        finally:
            driver.back()

finally:
    driver.quit()
    # print("Done")

# ADDING SONGS TO PLAYLIST
print("Adding songs to " + playlist_name + "...")
#TODO: Implement a while loop to add songs while the playlist is within a certain duration
i = 0
for video_id in video_ids:
    add_video_request = youtube.playlistItems().insert(
        part="snippet",
        body={
           "snippet":{
               "playlistId":playlist_id,
               "position":i,
               "resourceId": {
                   "kind":"youtube#video",
                   "videoId":video_id
               }
           }
        }
    )
    add_video_response = add_video_request.execute()
    #print(add_video_response)
    video_title = add_video_response["snippet"]["title"]
    print(str(i+1) + ".", video_title)
    i += 1
# print(json.dumps(response, sort_keys=True, indent=4))
webbrowser.open_new_tab(playlist_url)
