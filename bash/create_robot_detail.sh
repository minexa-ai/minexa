#!/bin/bash

url="https://api.minexa.ai/robot/"
api_key="YOUR_API_KEY"

# Your JSON data for the request body
data='{
    "look_for": "Features",
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

echo "Creating Robot.. This may take up to 2 minutes"

# Make the POST request
response=$(curl -s -X POST -H "Content-Type: application/json" -H "api-key: $api_key" -d "$data" "$url")

# Print the response
if [[ $(echo "$response" | jq -r '.status_code') == 200 ]]; then
    echo "Please confirm container is well located: $(echo "$response" | jq -r '.response.web_app')"

    # Create and save the file
    robot_id=$(echo "$response" | jq -r '.response.id')
    file_path="$(dirname "$(realpath "$0")")/robot_id_${robot_id}.json"

    # Save the robot.json
    echo "$response" > "$file_path"

    echo "Full robot json saved at: $file_path"
else
    echo "Error status code $(echo "$response" | jq -r '.status_code') occurred"
    echo "$response"
fi
