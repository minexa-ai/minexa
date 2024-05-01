require 'json'
require 'rest-client'

url = "https://api.minexa.ai/robot/"
api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"

# Your JSON data for the request body
data = {
    "look_for" => "clinical trial search results",
    "urls" => [
        "https://clinicaltrials.gov/search?page=1"
    ],
    "mode" => "list"
}

headers = {
    "Content-Type" => "application/json",
    "api-key" => api_key
}

# Make the POST request
response = RestClient.post(url, data.to_json, headers)

# Print the response
if response.code == 200
    response_json = JSON.parse(response.body)
    puts "Please confirm container is well located: #{response_json['response']['web_app']}"

    # Create and save the file
    robot_id = response_json["response"]["id"]
    file_path = File.join(File.dirname(File.expand_path(__FILE__)), "robot_id_#{robot_id}.json")

    # Save the robot.json
    File.open(file_path, 'w') do |file|
        file.write(JSON.pretty_generate(response_json))
    end

    puts "Full robot json saved at: #{file_path}"
else
    puts "Error status code #{response.code} occurred"
    begin
        puts JSON.parse(response.body)
    rescue StandardError => e
        puts "#{e} in showing error"
    end
end
