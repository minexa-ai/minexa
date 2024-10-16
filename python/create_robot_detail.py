import json
import os
import requests

url = "https://api.minexa.ai/robot/"
api_key = "YOUR_API_KEY"

# Your JSON data for the request body
data = {

    # what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page
    "look_for": "Features",

    # Provide 4 urls corresponding to a similarly structured page but with different data
    "urls":
    [
        "https://clinicaltrials.gov/study/NCT06382792",
        "https://clinicaltrials.gov/study/NCT06382779",
        "https://clinicaltrials.gov/study/NCT06382753",
        "https://clinicaltrials.gov/study/NCT06382727"

     ],

    # uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    #"reset": True,

    # Unocomment and set it when manaully detecting your container after first try
    # No need to use for creating robot for a particular page for the first time
    # "xpath": "/html/body/div/div/div[3]/div[1]/div[2]",

    # if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different
    # Use detail if the data is mixed and in a less structured format.
    "mode": "detail",
}

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

print("Creating Robot.. This may take up to 2 minutes")

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Please confirm container is well located:", response.json()['response']['web_app'])

    # Create and save the file
    robot_id = response.json()["response"]["id"]
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/robot_id_{robot_id}.json"

    # Save the robot.json
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=4)

    print("Full robot json saved at: {}".format(file_path))
else:
    print("Error status code {} occurred ".format(response.status_code))
    try:
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


