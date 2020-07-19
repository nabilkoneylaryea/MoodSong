import urllib.request
import json
search = input('Search: ')
url = 'http://www.google.com/search?q=' + search + '+music'
request = urllib.request.urlopen(url=url)
json.dumps(request, sort_keys=True, indent=4)
print(request)

