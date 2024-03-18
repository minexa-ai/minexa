import json
import re
import requests
from datetime import datetime

url = "https://api.minexa.ai/data/"
api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"

# Your JSON data for the request body

data = {
    "batches": [
        {
            "robot_id": 161,
            "columns": ["top_10", "col_45"],
            "scraping": {
                "country": "gb",
                "proxy": "residential",
                "provider": "service1",
            },
            "urls": [
                "https://www.amazon.com/s?k=clothes+m&ref=nb_sb_noss",
                "https://www.amazon.com/s?k=clothes+d&ref=nb_sb_noss",
                "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION^87490&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=",
            ],
        },
        {
            "robot_id": 160,
            "columns": ["top_5", "col_25"],
            "scraping": {
                "country": "gb",
                "proxy": "residential",
                "provider": "service1",
                "retry": 1,
            },
            "urls": [
                "https://www.amazon.com/s?k=clothes+m&ref=nb_sb_noss",
                "https://www.amazon.com/s?k=shirt+m&ref=nb_sb_noss",
                "https://www.amazon.com/s?k=shoes+m&ref=nb_sb_noss",
                "https://www.amazon.com/s?k=new+m&ref=nb_sb_noss",
            ],
        },
        {
            "robot_id": 150,
            "columns": ["top_5", "col_25"],
            "scraping": {
                "country": "gb",
                "proxy": "residential",
                "provider": "service1",
                "retry": 1,
            },
            "urls": [
                "https://www.xcxcxc.com/s?k=clothes+m&ref=nb_sb_noss",
            ],
        }
    ]
}

formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M")
# Create the file name
cleaned_filename = f"extract_data_{formatted_datetime}.json"


headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}


api_key = 'JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP'  # free key.
headers = {'HTTP_CONTENT_TYPE': 'application/json', 'HTTP_API_KEY': api_key}
next_set = None
started = 0
while next_set or started == 0:
    # Send a POST request with headers
    data['next'] = next_set
    response = requests.post(url, json=data, headers=headers)
    # Check if the request was successful (status code 2xx)
    if response.status_code // 100 == 2:
        json_content = response.json()
        print("res nbr {}".format(len(json_content['response'])))

        if 'next' in json_content['meta']:
            next_set = json_content['meta']['next']
            print("run " + next_set)
            started += 1
        else:
            print("finished")
            break
        # Now 'json_content' contains the parsed JSON data from the response
        try:
            with open(cleaned_filename, 'w') as file:
                json.dump(response.json(), file)
            utils.write_json_logs(PATH_LOGS + "/", 'extract_data_with_next_{}.json'.format(next_set), response.json(),
                                  ['ensure_ascii'])
        except json.JSONDecodeError:
            print(json_content)
    else:
        # Handle the case where the request was not successful
        print(f"Request failed with status code: {response.status_code}")
        print(response.content)