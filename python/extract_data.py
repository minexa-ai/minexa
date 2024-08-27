import pandas as pd
import json
import os
import requests
from datetime import datetime

url = "https://api.minexa.ai/data/"
api_key = 'YOUR_API_KEY'  # free key.

# Your JSON data for the request body
output_format = "json" #json/csv

data = {
  "batches": [
    {
      "robot_id": 103,
      "columns": [
        "col_1",
        "col_3"
      ],
      "urls": [
        "https://clinicaltrials.gov/search"
      ]
    }
  ]
}

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

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

            # Print the DataFrame with borders
            print(df.head())
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

