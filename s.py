import requests
import json
start_index = 0
key =  "AIzaSyAL2YTDGBmzJSvgrD52XdblSW6JJLYDfmE"
cx = "002299373873344878019:yf5tyg0gmnq"
q = "hello world"
url = "https://www.googleapis.com/customsearch/v1"
if start_index :
    query_string = {"key":key,"cx":cx,"num":"10","q":q,"start":start_index}
else :
    query_string = {"key":key,"cx":cx,"num":"10","q":q}
response = requests.request("GET", url, params=query_string)
json_data = json.loads(response.text)

for i in range(10):
    print(json_data["items"][i]["link"])



# unirest.get("https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/spelling/AutoComplete?text=do")
# .header("X-RapidAPI-Host", "contextualwebsearch-websearch-v1.p.rapidapi.com")
# .header("X-RapidAPI-Key", "8e1ebfcd66msh6964dd67b5771b3p1f73bajsnac7e451e7b58")
# .end(function (result) {
#   console.log(result.status, result.headers, result.body);
# });

import requests

# resp = requests.get(url="https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/spelling/AutoComplete?text=do")