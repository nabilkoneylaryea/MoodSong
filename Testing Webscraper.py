from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = '..\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://www.google.com/")
print(driver.title)
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
    print("URLs")
    i = 0
    for item in items:
        url = item.get_attribute("href")
        filter = url is not None
        if filter:
            second_filter = 'https://www.google.com/search?q=' in url and 'stick=' in url
            if second_filter:
                print(str(i + 1) + ".", url)
                urls.append(url)
                i += 1
    print("VIDEO IDs")
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
    print("Done")