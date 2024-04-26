## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

To install the necessary dependencies, you can use pip with the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

1. Use the `create_robot_list.py` if the data being scraped is in form of an itemized collection and `create_robot_detail.py` if the data is mixed and in a less structured format.
2. Go through the webapp to confirm or modigy the selected container
   a. If the selected container is located appropriately move ahead
   b. Else select the appropriate container get the new robot.json and again create a robot with these updated settings
3. Extract data from the created robot using `extract_data.py`.
