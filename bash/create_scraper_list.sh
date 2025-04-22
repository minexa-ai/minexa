#!/bin/bash

url="https://api.minexa.ai/scraper/"
api_key="YOUR_API_KEY"

# Your JSON data for the request body
# In Look For Copy paste the data from the website directly without any modification to train the scraper
# or Write a short description of your required data, for example: "clinical trials study overview"

data='{
    "look_for": "
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
    Hualien, Taiwan",
    "urls": ["https://clinicaltrials.gov/search?page=1"],
    "mode": "list"
}'

headers=(
    "Content-Type: application/json"
    "api-key: $api_key"
)

echo "Creating Scraper.. This may take up to 2 minutes"

# Make the POST request
response=$(curl -s -X POST -H "${headers[@]}" -d "$data" "$url")

# Print the response
if [ $? -eq 0 ]; then
    container=$(echo "$response" | jq -r '.response.web_app')
    echo "Please confirm container is well located: $container"

    # Create and save the file
    scraper_id=$(echo "$response" | jq -r '.response.id')
    file_path="$(dirname "$(realpath "$0")")/scraper_id$scraper_id.json"

    # Save the scraper.json
    echo "$response" | jq '.' > "$file_path"
    echo "Full scraper json saved at: $file_path"
else
    echo "Error occurred while making the request"
    echo "$response"
fi
