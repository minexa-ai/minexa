#!/bin/bash

url="https://api.minexa.ai/data/"
api_key='YOUR_API_KEY'  # free key.

# Your JSON data for the request body
output_format="json" #json/csv

data='{
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
}'

headers='{
    "Content-Type": "application/json",
    "api-key": "'"$api_key"'"
}'

next_set=""
started=0
iterated_data=()
extracted_data=()

formatted_datetime=$(date +"%Y_%m_%d_%H_%M")
while [[ $next_set != "" || $started == 0 ]]; do
    # Send a POST request with headers
    data=$(jq --arg next_set "$next_set" '.next = $next_set' <<< "$data")
    response=$(curl -s -X POST -H "Content-Type: application/json" -H "api-key: $api_key" -d "$data" "$url")

    # Check if the request was successful (status code 2xx)
    if [[ $(jq -r '.status_code' <<< "$response") == 200 ]]; then
        json_content=$(jq -r '.response' <<< "$response")

        while IFS= read -r extractions; do
            while IFS= read -r rows; do
                if [[ $(jq -r '.error' <<< "$rows") == "false" ]]; then
                    row=$(jq -r '. | to_entries | map("\(.key)=\(.value)") | join("&")' <<< "$rows")
                    iterated_data+=("$row")
                fi
            done <<< "$(jq -c '.results[]' <<< "$extractions")"
        done <<< "$(jq -c '.[]' <<< "$json_content")"

        extracted_data+=("$json_content")

        # Create and save the files
        file_path="$(dirname "$(realpath "$0")")/exctraction_${formatted_datetime}"

        # Saving in json format
        echo "$response" > "${file_path}.json"

        # Saving in csv format
        jq -r '.results | map([.col_1, .col_3] | join(",")) | join("\n")' <<< "$response" > "${file_path}.csv"

        # Saving in Excel format
        jq -r '.results | map([.col_1, .col_3])' <<< "$response" | jq -r '["col_1,col_3"] + (.[] | join(",")) | .[]' | sed 's/\"//g' | tr '\n' '\r' | tr '\r' '\n' > "${file_path}.xlsx"

        echo "Saved files at: ${file_path}.json, ${file_path}.csv, ${file_path}.xlsx"

        if [[ $(jq -r '.meta.next' <<< "$json_content") != "null" ]]; then
            next_set=$(jq -r '.meta.next' <<< "$json_content")
            echo "run $next_set"
            ((started++))
        else
            echo "finished"
            break
        fi

    else
        # Handle the case where the request was not successful
        echo "Request failed with status code: $(jq -r '.status_code' <<< "$response")"
        echo "$response"
        break
    fi
done
