from .authentication import MicrosoftGraphAuthentication
from common.types import InputParameter, DataType, OutputParameter

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
import time

### Input Parameters
INSTANCE = InputParameter(
    "INSTANCE",
    description="Instance to be used for fetching details",
    data_type=DataType.STRING,
)
USER_ID = InputParameter(
    "USER_ID",
    description="The ID of the specific user to fetch",
    data_type=DataType.STRING,
    optional=True,
)
EMAIL = InputParameter(
    "EMAIL",
    description="Email address to filter users by",
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
USER_DETAILS = OutputParameter(
    name="USER_DETAILS",
    description="User details from Microsoft Azure",
    data_type=DataType.JSON,
)
### End of Output Parameters


def run_skill(input_params, auth_params):
    """This will be called to run the skill"""
    integration = MicrosoftGraphAuthentication(auth_params)
    ## Logic Starts Here
    try:
        api_start_time = time.time()

        # Read all input parameters
        user_id = USER_ID.read_value(input_params)
        email = EMAIL.read_value(input_params)

        # Get headers with authentication token
        headers = integration.get_headers()

        # Construct URL
        url = f"{integration.base_url}/v1.0/users"

        if user_id:
            url = url + "/" + user_id
        elif email:
            url = (
                url
                + f"?$filter=mail eq '{email}' or userPrincipalName eq '{email}'"
            )

        # Make the API request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        user_details = response.json()
        print(
            f"User Details fetched successfully, time_taken={time.time() - api_start_time}"
        )
        return {
            "STATUS": response.status_code,
            "USER_DETAILS": user_details,
        }
    except Exception as e:
        return {
            "STATUS": 500,
            "USER_DETAILS": str(e),
        }
    ## Logic Ends Here
