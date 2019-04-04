import requests
import json

class Google:


    def g(self, query):
        
        start_index = 0
        key =  "AIzaSyAL2YTDGBmzJSvgrD52XdblSW6JJLYDfmE"
        cx = "002299373873344878019:e5mgnadgu-q"
        q = query
        url = "https://www.googleapis.com/customsearch/v1"
        if start_index :
            query_string = {"key":key,"cx":cx,"num":"10","q":q,"start":start_index}
        else :
            query_string = {"key":key,"cx":cx,"num":"10","q":q}
        response = requests.request("GET", url, params=query_string)
        json_data = json.loads(response.text)
        json_data = [json_data["items"][i]["link"] for i in range(5)]
        return json_data