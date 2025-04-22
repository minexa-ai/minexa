require 'json'
require 'rest-client'

url = "https://api.minexa.ai/scraper/"
api_key = "YOUR_API_KEY"

# Your JSON data for the request body
data = {
    # Copy paste the data from the website directly without any modification to train the scraper
    # or Write a short description of your required data, for example: "clinical trials results"
    "look_for":  <<~TEXT
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
    Hualien, Taiwan
    TEXT,

    "urls" => [
        "https://clinicaltrials.gov/search?page=1"
    ],
    "mode" => "list"
}

headers = {
    "Content-Type" => "application/json",
    "api-key" => api_key
}

puts "Creating scraper.. This may take up to 2 minutes"

# Make the POST request
response = RestClient.post(url, data.to_json, headers)

# Print the response
if response.code == 200
    response_json = JSON.parse(response.body)
    puts "Please confirm container is well located: #{response_json['response']['web_app']}"

    # Create and save the file
    scraper_id = response_json["response"]["id"]
    file_path = File.join(File.dirname(File.expand_path(__FILE__)), "scraper_id_#{scraper_id}.json")

    # Save the scraper.json
    File.open(file_path, 'w') do |file|
        file.write(JSON.pretty_generate(response_json))
    end

    puts "Full scraper json saved at: #{file_path}"
else
    puts "Error status code #{response.code} occurred"
    begin
        puts JSON.parse(response.body)
    rescue StandardError => e
        puts "#{e} in showing error"
    end
end
