import json
import re
import requests
from datetime import datetime

class ExtractDataClass():
  """Class for the extract data methods"""

  def __init__(self, api_key, data) -> None:
      self.extract_url = "https://api.minexa.ai/data/"
      self.create_robot_url = "https://api.minexa.ai/robot/"
      self.api_key = api_key

  def post_API(self,next_set):
      """Method for API calling"""
      headers = {
                  "Content-Type": "application/json",
                  "api-key": self.api_key
                }
      response = requests.post(self.extract_url, json=self.extract_payload, headers=headers)
      return response

  def fetch_data(self):
    """Method to fetch all the data iteratively"""
    next_set = None # Initializing the next_set as None
    # Initialized as 0 for start, increaments for next iterations
    started = 0
    extracted_data = {}
    while next_set or started == 0:
        # Send a POST request with headers
        self.extract_payload['next'] = next_set
        response = self.post_API(next_set)
        # Check if the request was successful (status code 2xx)
        if response.status_code == 200:
            json_content = response.json()
            extracted_data.update(json_content)
            # with open("cleaned_filename.json", 'w') as file:
            #         json.dump(response.json(), file, indent=4)
            print("res nbr {}".format(len(json_content['response'])))

            if 'next' in json_content['meta']:
                next_set = json_content['meta']['next']
                print("run " + next_set)
                started += 1
            else:
                print("finished")
                return extracted_data

        else:
            # Handle the case where the request was not successful
            print(f"Request failed with status code: {response.status_code}")
            print(response.content)
            return None

  def print_and_save_data(self, json_content, cleaned_filename=False,msg=None):
      if cleaned_filename == False:
        formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M")
        cleaned_filename = f"extract_data_{formatted_datetime}.json"

      try:
          with open(cleaned_filename, 'w') as file:
              json.dump(json_content, file)

          # utils.write_json_logs(PATH_LOGS + "/", 'extract_data_with_next_{}.json'.format(next_set), response.json(),
          #                       ['ensure_ascii'])
      except json.JSONDecodeError:
          print(json_content)

  def extract_data(self, extract_payload):
      """Extract data"""

      self.extract_payload = extract_payload
      # Get the extracted data from the robot
      extracted_data = self.fetch_data()

      # Save the extracted data
      self.print_and_save_data(extracted_data)

  def create_robot(self,robot_payload, cleaned_filename=False):
    """Method to handle robot creation"""
    self.robot_payload = robot_payload
    if cleaned_filename == False:
      formatted_datetime = datetime.now().strftime("%Y%m%d_%H%M")
      # Create the file name
      cleaned_filename = f"create_robot_{formatted_datetime}.json"

    # Make the POST request
    response = requests.post(self.create_robot_url, json=data, headers=self.headers)
    # Print the response
    if response.status_code == 200:
        print("Please confirm container is well located:", response.json()['response']['web_app'])
        # Write the JSON content to the file
        with open(cleaned_filename, 'w') as file:
            json.dump(response.json(), file)
        print("Full robot json saved at: {}".format(cleaned_filename))
    else:
        print("Error status code {} occurred ".format(response.status_code))
        try:
            print(response.json())
        except Exception as e:
            print("{} in showing error".format(e))




api_key = 'JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP'  # free key.
data = {
  "batches": [
    {
      "robot_id": 58,
      "columns": [
        "col_18",
        "col_29",
        "col_14"
      ],
      "urls": [
        "https://www.flipkart.com/search?q=smartphones"
      ]
    }
  ]
}

extract_data_object = ExtractDataClass(api_key)

extract_data_object.extract_data(data)



"""
### 1 Class 1 File with all the methods


### 1. create_robot_list.py
    2. create_robot_detail.py
    3. extract_data.py
    4. public_robots.py (GET /robot?params )
    (Keep excel available to the clients)
    5. Ability of output in CSV format
    saving the data for both create_robot and extract data needs to be saved in a folder

    Test It out


"""
