from bs4 import BeautifulSoup
import requests
import re
import json

response = requests.get("https://www.youtube.com/results?search_query=yaman").text
soup = BeautifulSoup(response,'lxml')
print(soup)



script = soup.find_all("script")[32]
# print(script)
json_text = re.search('var ytInitialData = (.+)[,;]{1}',str(script)).group(1)

# with open("script.txt","w",encoding="utf-8") as output:
#    output.write(json_text)

json_data = json.loads(json_text)

content = json_data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']

# print(content)