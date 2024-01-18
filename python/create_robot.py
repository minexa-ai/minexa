import json
import re
import requests
from datetime import datetime

url = "https://api.minexa.ai/robot/"
api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"

# Your JSON data for the request body
data = {
    "look_for": "real estate listings 2", # what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page
    "urls": ['https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%5E87490&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare='], # if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different.
    #"mode": ("list" or "detail") - highly recommended to set to avoid unexpected data mining. help:
    #"reset": True - uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    "xpath": "/html/body/div[1]/div[2]/div[1]/div[2]/div[5]/div[1]/div",
    "mode": "list"
}
#cleaned_filename = re.sub(r'[^\w]', '', '_'.join([str(value) for key, value in data.items() if key in ["look_for", "urls"]]))[0:50]+".json"
#cleaned_filename = re.sub(r'[^\w]', '', '_'.join([str(value) for key, value in data.items() if key in ["look_for", "urls"]]))[0:50]+".json"



formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M")
# Create the file name
cleaned_filename = f"create_robot_{formatted_datetime}.json"


headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)
# Print the response
if response.status_code == 200:
    print("Please confirm container is well located:", response.json()['response']['web_app'])
    # Write the JSON content to the file
    with open(cleaned_filename, 'w') as file:
        json.dump(response.json(), file)
    print("Full robot json saved at: {}".format(cleaned_filename))
else:
    print("Error status code {} occurred ".format(response.status_code))
    try:
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


