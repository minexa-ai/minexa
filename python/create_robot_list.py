import json
import os
import requests
from datetime import datetime

url = "https://api.minexa.ai/robot/"
api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"

# Your JSON data for the request body
data = {
    # what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page
    "look_for": "names list", # what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page

    # Provide a single url corresponding to pages with listed data
    "urls":
    [
    "https://www.britannica.com/topic/list-of-herbs-and-spices-2024392"
    ],

    # uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    #"reset": True,

    # "xpath": "/html/body/div/div/div[3]/div[1]/div[2]",

    "mode": "list" # Choices are list or detail
}



headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Please confirm container is well located:", response.json()['response']['web_app'])

    # Create and save the file
    robot_id = response.json()["response"]["id"]
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/robot_id_{robot_id}.json"

    # Save the robot.json
    with open(file_path, 'w') as file:
        json.dump(response.json(), file, indent=4)
    print("Full robot json saved at: {}".format(file_path))
else:
    print("Error status code {} occurred ".format(response.status_code))
    try:
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


