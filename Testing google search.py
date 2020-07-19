from googlesearch import search
query = "sad music"
i = 1
video_ids = []
for result in search(query, tld='com', lang='en', num=10, start=0, stop=9, pause=2.0):
    print(str(i) + ": ", result)
    youtube_link = "https://www.youtube.com/watch?v=" in result
    if youtube_link:
        index = result.find("=") + 1
        id = result[index:]
        video_ids.append(id)
        print("Video ID: ", id)
    i += 1
print(video_ids)