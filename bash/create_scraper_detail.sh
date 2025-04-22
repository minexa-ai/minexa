#!/bin/bash

url="https://api.minexa.ai/scraper/"
api_key="YOUR_API_KEY"

# Your JSON data for the request body

# In Look For Copy paste the data from the website directly without any modification to train the scraper
# or Write a short description of your required data, for example: "clinical trials study overview"
data='{
    "look_for": "Study Overview
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
    2024PI059",
    "urls": [
        "https://clinicaltrials.gov/study/NCT06382792",
        "https://clinicaltrials.gov/study/NCT06382779",
        "https://clinicaltrials.gov/study/NCT06382753",
        "https://clinicaltrials.gov/study/NCT06382727"
    ],
    "mode": "detail"
}'

headers='{
    "Content-Type": "application/json",
    "api-key": "'"$api_key"'"
}'

echo "Creating Scraper.. This may take up to 2 minutes"

# Make the POST request
response=$(curl -s -X POST -H "Content-Type: application/json" -H "api-key: $api_key" -d "$data" "$url")

# Print the response
if [[ $(echo "$response" | jq -r '.status_code') == 200 ]]; then
    echo "Please confirm container is well located: $(echo "$response" | jq -r '.response.web_app')"

    # Create and save the file
    scraper_id=$(echo "$response" | jq -r '.response.id')
    file_path="$(dirname "$(realpath "$0")")/scraper_id_${scraper_id}.json"

    # Save the scraper.json
    echo "$response" > "$file_path"

    echo "Full scraper json saved at: $file_path"
else
    echo "Error status code $(echo "$response" | jq -r '.status_code') occurred"
    echo "$response"
fi
