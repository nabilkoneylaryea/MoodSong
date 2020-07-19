import webbrowser
import urllib
import json
import os
from googlesearch import search
from googleapiclient.discovery import build
from google_auth_oauthlib import flow
import googleapiclient.errors

# USER INPUT
mood = input("What is the mood or occasion? Please use a single word to describe e.g. driving: ")
not_one_word = " " in mood or "_" in mood or "-" in mood
while not_one_word:
    mood = input("Please use a single word to describe (no spaces, underscores, or hyphens): ")

mood = mood.lower()
query = mood + " music"
search = search(query, tld='com', lang='en', num=10,start=0, stop=10, pause=2.0)
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
video_ids = []
i = 1
for result in search:
    #print(str(i) + ": ", result)
    youtube_link = "https://www.youtube.com/watch?v=" in result
    if youtube_link:
        index = result.find("=") + 1
        id = result[index:]
        video_ids.append(id)
        #print("Video ID: ", id)
    i += 1

# ADDING SONGS TO PLAYLIST
print("Adding songs to " + playlist_name + "...")
# playlist_short =
# while(playlist_short):
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
