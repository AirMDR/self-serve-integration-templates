from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests

### Connection Parameters
API_URL = ConnectionParam(
    "API_URL",
    description="Base API URL (e.g. https://api.example.com)",
    input_type=InputType.TEXT,
)
API_KEY = ConnectionParam(
    "API_KEY",
    description="API Key/Token",
    input_type=InputType.PASSWORD,
)
### End of Connection Parameters


class MyIntegrationProvider:
    def __init__(self, auth_params):
        self.api_url = API_URL.read_value(auth_params)
        self.api_key = API_KEY.read_value(auth_params)

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = MyIntegrationProvider(auth_params)
        url = f"{integration.api_url}/auth"
        headers = integration.get_headers()
        response = requests.post(url, headers=headers, json={})
        if response.status_code >= 200 and response.status_code < 300:
            return 200
        return 401
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
