from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests


### Connection Parameters
API_URL = ConnectionParam(
    "API_URL",
    description="Base API URL for Recorded Future",
    input_type=InputType.TEXT,
)
API_KEY = ConnectionParam(
    "API_KEY",
    description="API Key for Recorded Future",
    input_type=InputType.PASSWORD,
)
### End of Connection Parameters


class RecordedFutureAuthentication:
    def __init__(self, auth_params):
        self.api_url = API_URL.read_value(auth_params)
        self.api_key = API_KEY.read_value(auth_params)

    def get_headers(self):
        return {
            "X-RFToken": self.api_key,
            "accept": "application/json",
        }


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = RecordedFutureAuthentication(auth_params)
        url = f"{integration.api_url}/alert/v3"
        headers = integration.get_headers()
        payload = {"limit": 1}
        response = requests.get(url, headers=headers, json=payload)
        if response.status_code == 200:
            return 200
        return 401
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
