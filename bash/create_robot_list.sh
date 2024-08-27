#!/bin/bash

url="https://api.minexa.ai/robot/"
api_key="YOUR_API_KEY"

# Your JSON data for the request body
data='{
    "look_for": "clinical trial search results",
    "urls": ["https://clinicaltrials.gov/search?page=1"],
    "mode": "list"
}'

headers=(
    "Content-Type: application/json"
    "api-key: $api_key"
)

echo "Creating Robot.. This may take up to 2 minutes"

# Make the POST request
response=$(curl -s -X POST -H "${headers[@]}" -d "$data" "$url")

# Print the response
if [ $? -eq 0 ]; then
    container=$(echo "$response" | jq -r '.response.web_app')
    echo "Please confirm container is well located: $container"

    # Create and save the file
    robot_id=$(echo "$response" | jq -r '.response.id')
    file_path="$(dirname "$(realpath "$0")")/robot_id_$robot_id.json"

    # Save the robot.json
    echo "$response" | jq '.' > "$file_path"
    echo "Full robot json saved at: $file_path"
else
    echo "Error occurred while making the request"
    echo "$response"
fi
