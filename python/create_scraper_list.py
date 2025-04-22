import json
import os
import requests

url = "https://api.minexa.ai/scraper/"
api_key = "YOUR_API_KEY"

# Your JSON data for the request body
data = {
    # Copy paste the data from the website directly without any modification to train the scraper
    # or Write a short description of your required data, for example: "clinical trials results"
    "look_for": """
    NCT06939504
    Not yet recruiting
    New
    A Trial of HRS-9813 Capsule and Tablet in Healthy Subjects
    Conditions
    Pulmonary Fibrosis
    Locations
    Shanghai, Shanghai, China


    NCT06939491
    Recruiting
    New
    Comparison of Ultrasound-guided Electrolysis Therapy vs. Sham Electrolysis in Patients With Patellar Tendinopathy: A Prospective Randomized Study Including MRI and Shear-wave Ultrasound Elastography Imaging
    Conditions
    Patellar Tendinopathy / Jumpers Knee
    Locations
    Bremen, Germany


    NCT06939478
    Not yet recruiting
    New
    AI Powered Mapping Technology for Identifying Arrhythmias
    Conditions
    Arrhythmias, Cardiac
    Locations
    Location not provided


    NCT06939465
    Recruiting
    New
    Esophageal Visceral Hypersensitivity and Hypervigilance in Disorders of Gut-brain Interaction: the Roles of Cognitive-behavioral Therapy
    Conditions
    GERD Without Erosive Esophagitis
    Gut-Brain Disorders
    Locations
    Hualien, Taiwan""",

    # Provide a single url corresponding to pages with listed data
    "urls":
    [
    "https://clinicaltrials.gov/search?page=1"
    ],

    # uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    #"reset": True,

    # Unocomment and set it when manaully detecting your container after first try
    # No need to use for creating scraper for a particular page for the first time
    # "xpath": "/html/body/div/div/div[3]/div[1]/div[2]",

    "mode": "list" #  Use list if the data you're scraping is in form of an itemized collection
}



headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

print("Creating scraper.. This may take up to 2 minutes")

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Please confirm container is well located:", response.json()['response']['web_app'])

    # Create and save the file
    scraper_id = response.json()["response"]["id"]
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/scraper_id_{scraper_id}.json"

    # Save the scraper.json
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=4)

    print("Full scraper json saved at: {}".format(file_path))
else:
    print("Error status code {} occurred ".format(response.status_code))
    try:
        print(response.status_code)
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


