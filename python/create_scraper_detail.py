import json
import os
import requests

url = "https://api.minexa.ai/scraper/"
api_key = "YOUR_API_KEY"

# Your JSON data for the request body
data = {
    # Copy paste the data from the website directly without any modification to train the scraper
    # or Write a short description of your required data, for example: "clinical trials study overview"
    "look_for": """Study Overview
    Brief Summary
    The gold standard after shoulder resection for tumors is reconstruction by reverse prosthesis and allograft. This is an intervention also performed for more frequent etiologies (revisions of prosthesis, non cancerous humeral bone loss ...).

    The results in these etiologies are good, and do not find any particular mechanical complications (including no osteolysis of the graft). In the case of reconstruction for cancer, the numbers of patients are lower (rare pathologies) and some studies on small numbers found osteolysis of the allograft. The aim of this study is to analyze the presence or not osteolysis in these patients, and to quantify it precisely by scanner measurement (no data yet in the literature).

    Detailed Description
    quantify bone stock of the allograft by scanner measurement in post operative and in 6 month to 1 years after surgery.

    This is a retrospective study, and the scanner was performed routinely every 3 to 6 month, during 2 years, for oncological follow up.

    Official Title
    Results of Proximal Humeral Reconstruction With Allograft Prosthetic Composite After Resection for Tumors
    Conditions
    Shoulder Disease
    Intervention / Treatment
    Procedure: proximal humeral resection for tumor and allograft prosthetic composite reconstruction
    Other Study ID Numbers
    2024PI059""",

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
    # No need to use for creating scraper for a particular page for the first time
    # "xpath": "/html/body/div/div/div[3]/div[1]/div[2]",

    # if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different
    # Use detail if the data is mixed and in a less structured format.
    "mode": "detail",
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
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


