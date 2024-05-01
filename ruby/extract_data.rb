require 'json'
require 'rest-client'
require 'date'
require 'csv'
require 'nokogiri'
require 'open-uri'

url = "https://api.minexa.ai/data/"
api_key = 'JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP'  # free key.

# Your JSON data for the request body
output_format = "json" #json/csv

data = {
  "batches": [
    {
      "robot_id": 103,
      "columns": [
        "col_1",
        "col_3"
      ],
      "urls": [
        "https://www.britannica.com/topic/list-of-herbs-and-spices-2024392"
      ]
    }
  ]
}

headers = {
    "Content-Type" => "application/json",
    "api-key" => api_key
}

next_set = nil
started = 0
iterated_data = []
extracted_data = []

formatted_datetime = DateTime.now.strftime("%Y_%m_%d_%H_%M")
while next_set || started == 0
    # Send a POST request with headers
    data['next'] = next_set
    response = RestClient.post(url, data.to_json, headers)

    # Check if the request was successful (status code 2xx)
    if response.code == 200
        json_content = JSON.parse(response.body)

        json_content["response"].each do |extractions|
            extractions["results"].each do |rows|
                next if rows.key?("error")
                row = {}
                rows.each do |col, value|
                    if value.is_a?(String)
                        row[col] = value
                    elsif value.is_a?(Array)
                        row[col] = value.map { |x| x["value"] }
                    end
                end
                iterated_data << row
            end
        end

        extracted_data += json_content["response"]

        begin
            # Create and save the file
            file_path = File.join(File.dirname(File.expand_path(__FILE__)), "exctraction_#{formatted_datetime}")

            # Saving in json format
            File.open("#{file_path}.json", 'w') do |file|
                file.write(JSON.pretty_generate(extracted_data))
            end

            # Convert data to DataFrame
            df = iterated_data.to_a

            # Print the DataFrame with borders
            puts df[0..4]

            # Saving the csv
            CSV.open("#{file_path}.csv", "wb") do |csv|
                csv << df[0].keys
                df.each { |row| csv << row.values }
            end

            # Save DataFrame to Excel file
            File.open("#{file_path}.xlsx", "wb") do |file|
                file.write(df.to_xlsx)
            end
        rescue JSON::JSONError => e
            puts e
        end

        puts "res nbr #{json_content['response'].length}"
        if json_content['meta'].key?('next')
            next_set = json_content['meta']['next']
            puts "run #{next_set}"
            started += 1
        else
            puts "finished"
            break
        end
    else
        # Handle the case where the request was not successful
        puts "Request failed with status code: #{response.code}"
        puts response.body
    end
end
