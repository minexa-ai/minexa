import json
import os
import requests
from datetime import datetime

url = "https://api.minexa.ai/robot/"
api_key = "JtAdCU14pFksHYrkKzCiVoNIrKX8ZCbLOmwtCKYQsXx57ivIsP"

# Your JSON data for the request body
data = {

    # what part of the page you want to extract - free form - write a descriptive text so that we can better locate the right part of the page
    "look_for": "Features",

    # Provide 4 urls corresponding to pages with similiar structers
    # if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different.
    "urls":
    [
        "https://www.flipkart.com/poco-c55-power-black-64-gb/p/itme567bcd596fe9?pid=MOBGMXSW9PHJVQCA&lid=LSTMOBGMXSW9PHJVQCALTZQ3D&marketplace=FLIPKART&q=smartphones&store=tyy%2F4io&srno=s_1_1&otracker=search&iid=c94adc80-db28-4f7e-b937-89b19b183c9d.MOBGMXSW9PHJVQCA.SEARCH&ssid=pyee4mlzm80000001711995480426&qH=6ea4465d0add4685",
        "https://www.flipkart.com/vivo-t3-5g-crystal-flake-128-gb/p/itm69b3c5633378f?pid=MOBGYT3VN2J3GM45&lid=LSTMOBGYT3VN2J3GM45SGB0DT&marketplace=FLIPKART&q=smartphones&store=tyy%2F4io&srno=s_1_2&otracker=search&iid=c94adc80-db28-4f7e-b937-89b19b183c9d.MOBGYT3VN2J3GM45.SEARCH&ssid=pyee4mlzm80000001711995480426&qH=6ea4465d0add4685",
        "https://www.flipkart.com/motorola-g24-power-ink-blue-128-gb/p/itmecab4a01b8aaf?pid=MOBGUFK4UBP7ZTXJ&lid=LSTMOBGUFK4UBP7ZTXJ6TV61J&marketplace=FLIPKART&q=smartphones&store=tyy%2F4io&srno=s_1_3&otracker=search&iid=c94adc80-db28-4f7e-b937-89b19b183c9d.MOBGUFK4UBP7ZTXJ.SEARCH&ssid=pyee4mlzm80000001711995480426&qH=6ea4465d0add4685",        "https://www.flipkart.com/oneplus-nord-ce-3-lite-5g-pastel-lime-128-gb/p/itm2cd5a4e659035?pid=MOBGZJ3WM5SGTGVZ&lid=LSTMOBGZJ3WM5SGTGVZ8XUVDF&marketplace=FLIPKART&q=smartphones&store=tyy%2F4io&srno=s_1_4&otracker=search&iid=c94adc80-db28-4f7e-b937-89b19b183c9d.MOBGZJ3WM5SGTGVZ.SEARCH&ssid=pyee4mlzm80000001711995480426&qH=6ea4465d0add4685"

     ],

    # uncomment if you need to recrawl the HTML again from scratch by ignoring cached data (like its the first time you scrape it)
    #"reset": True,

    # "xpath": "/html/body/div/div/div[3]/div[1]/div[2]",

    # if you want to extract detail data, we advise not to use a simple domain name but try to find pages that are different
    "mode": "detail", # Choices are list or detail
}

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Make the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
if response.status_code == 200:
    print("Please confirm container is well located:", response.json()['response']['web_app'])

    # Create and save the file
    robot_id = response.json()["response"]["id"]
    file_path = f"{os.path.dirname(os.path.abspath(__file__))}/robot_id_{robot_id}.json"

    # Save the robot.json
    with open(file_path, 'w') as file:
        json.dump(response.json(), file, indent=4)

    print("Full robot json saved at: {}".format(file_path))
else:
    print("Error status code {} occurred ".format(response.status_code))
    try:
        print(response.json())
    except Exception as e:
        print("{} in showing error".format(e))


