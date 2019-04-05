from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings()
from urllib3.util import parse_url


def youtube(msg):
    search = msg.replace(" ","20%")
    response = requests.get(
        "https://www.youtube.com/results?search_query={}".format(search), verify=False).text
    result = BeautifulSoup(response, "html.parser")
    return result.find_all(attrs={'class': 'yt-uix-tile-link'})


print(youtube("apple scab"))