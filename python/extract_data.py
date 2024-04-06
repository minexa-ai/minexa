import pandas as pd
import json
import os
import requests
from datetime import datetime

url = "https://api.minexa.ai/data/"
api_key = 'JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP'  # free key.

# Your JSON data for the request body
output_format = "json" #json/csv
data = {
    "batches": [
        {
            "robot_id": 58,
            "columns": ["top_10","col_4", "col_29"],
            # "scraping": {
            #     "country": "gb",
            #     "proxy": "residential",
            #     "provider": "service1",
            # },
            "urls": [
                "https://www.flipkart.com/search?q=Laptop",
                "https://www.flipkart.com/search?q=washing+machine&sid=j9e%2Cabm%2C8qx&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_8_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=washing+machine%7CWashing+Machines&requestId=a672e3d3-5560-4e88-bbe7-24ed9b5a2c61&as-searchtext=Washing%20",
                # "https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION^87490&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare=",
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

data = {
  "batches": [
    {
      "robot_id": 96,
      "columns": [
        "col_6",
        "col_19",
        "col_18"
      ],
      "urls": [
        "https://www.flipkart.com/search?q=smartphones&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_6_0_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_6_0_na_na_na&as-pos=6&as-type=HISTORY&suggestionId=smartphones&requestId=dc094101-2122-4557-bd9f-0358b5669186",
        "https://www.flipkart.com/search?q=washing+machine&sid=j9e%2Cabm%2C8qx&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=washing+machine%7CWashing+Machines&requestId=b81ca721-c07d-4fdf-86e3-57b17b2fcec8&as-searchtext=was"
      ]
    }
  ]
}

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}


# headers = {'HTTP_CONTENT_TYPE': 'application/json', 'api-key': api_key}

next_set = None
started = 0
iterated_data = []
extracted_data = []

formatted_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M")
while next_set or started == 0:
    # Send a POST request with headers
    data['next'] = next_set
    response = requests.post(url, json=data, headers=headers)

    # Check if the request was successful (status code 2xx)
    if response.status_code == 200:
        json_content = response.json()

        for extractions in response.json()["response"]:
            for rows in extractions["results"]:
                if rows.get("error", False):
                    continue
                row = {}
                for col,value in rows.items():
                    if isinstance(value, str):
                        row.update({col:value})
                    elif isinstance(value, list):
                        row.update({col:[x["value"] for x in value]})
                iterated_data.append(row)

        extracted_data += response.json()["response"]
        try:

            # Create and save the file
            file_path = f"{os.path.dirname(os.path.abspath(__file__))}/exctraction_{formatted_datetime}"

            # Saving in json format
            with open(f"{file_path}.json", 'w') as file:
                json.dump(extracted_data, file, indent=4)

            df = pd.DataFrame(iterated_data)

            # Saving the csv
            df.to_csv(f"{file_path}.csv", index=False)

            # Save DataFrame to Excel file
            df.to_excel(f"{file_path}.xlsx", index=True)

        except json.JSONDecodeError:
            print(response.json())

        print("res nbr {}".format(len(json_content['response'])))
        if 'next' in json_content['meta']:
            next_set = json_content['meta']['next']
            print("run " + next_set)
            started += 1

        else:
            print("finished")
            break

    else:
        # Handle the case where the request was not successful
        print(f"Request failed with status code: {response.status_code}")
        print(response.content)

