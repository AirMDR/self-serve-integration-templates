from .authentication import BambooHRAuthentication
from common.types import InputParameter, DataType, OutputParameter

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests

### Input Parameters
INSTANCE = InputParameter(
    "INSTANCE",
    description="Instance to be used for fetching details",
    data_type=DataType.STRING,
)
EMAIL = InputParameter(
    "EMAIL",
    description="User's email address",
    data_type=DataType.STRING,
    optional=True,
)
NAME = InputParameter(
    "NAME",
    description="User's name (firstNameLastName)",
    data_type=DataType.STRING,
    optional=True,
)
EMPLOYEE_ID = InputParameter(
    "EMPLOYEE_ID",
    description="Employee ID",
    data_type=DataType.STRING,
    optional=True,
)
FILTER_KEY = InputParameter(
    "FILTER_KEY",
    description="Custom filter field",
    data_type=DataType.STRING,
    optional=True,
)
FILTER_VALUE = InputParameter(
    "FILTER_VALUE",
    description="Custom filter value",
    data_type=DataType.STRING,
    optional=True,
)
### End of Input Parameters

### Output Parameters
STATUS = OutputParameter(
    name="STATUS",
    description="Status of the skill execution",
    data_type=DataType.STRING,
)
EMPLOYEES = OutputParameter(
    name="EMPLOYEES",
    description="List of matched employees",
    data_type=DataType.JSON,
)
### End of Output Parameters


def run_skill(input_params, auth_params):
    """
    This will be called to run the skill.
    Gets user details from BambooHR using various filter criteria.
    """
    integration = BambooHRAuthentication(auth_params)
    ## Logic Starts Here
    try:
        # Get input parameters
        email = EMAIL.read_value(input_params)
        name = NAME.read_value(input_params)
        employee_id = EMPLOYEE_ID.read_value(input_params)
        filter_key = FILTER_KEY.read_value(input_params)
        filter_value = FILTER_VALUE.read_value(input_params)

        # Check if at least one search criteria is provided
        if not any([email, name, employee_id, filter_key]):
            raise ValueError(
                "At least one search criteria (email, name, employee_id, or filter_key) must be provided"
            )

        # Determine which filter to use
        if email:
            filter_key = "email"
            filter_value = email
        elif name:
            filter_key = "firstNameLastName"
            filter_value = name
        elif employee_id:
            filter_key = "eeid"
            filter_value = employee_id
        elif not filter_key or not filter_value:
            raise ValueError(
                "Both filter_key and filter_value must be provided when using custom filters"
            )

        # Define the fields we want to retrieve (simplified list)
        fields = [
            "firstName",
            "lastName",
            "email",
            "jobTitle",
            "department",
        ]

        # Prepare the request payload
        payload = {
            "fields": fields,
            "filters": {
                "match": "all",
                "filters": [
                    {
                        "field": filter_key,
                        "operator": "equal",
                        "value": filter_value,
                    }
                ],
            },
        }
        subdomain = integration.base_url.split("//")[1].split(".")[0]

        # Make the API request
        url = f"https://api.bamboohr.com/api/gateway.php/{subdomain}/v1/datasets/employee"
        headers = integration.get_headers()

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        response_json = response.json()

        # Check if we got any results
        if not response_json.get("data"):
            print(f"No user found with {filter_key}={filter_value}")
            return {}

        return {
            "STATUS": response.status_code,
            "EMPLOYEES": response_json,
        }
    except Exception as e:
        return {
            "STATUS": 500,
            "EMPLOYEES": str(e),
        }
    ## Logic Ends Here
