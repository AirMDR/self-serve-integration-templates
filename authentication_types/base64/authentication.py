from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
import base64


### Connection Parameters
USERNAME = ConnectionParam(
    "USERNAME",
    description="Username (will be base64 encoded)",
    input_type=InputType.TEXT,
)
PASSWORD = ConnectionParam(
    "PASSWORD",
    description="Password (will be base64 encoded)",
    input_type=InputType.PASSWORD,
)
BASE_URL = ConnectionParam(
    "BASE_URL",
    description="Base URL",
    input_type=InputType.TEXT,
)
### End of Connection Parameters


class MyIntegrationProvider:
    def __init__(self, auth_params):
        self.username = USERNAME.read_value(auth_params)
        self.password = PASSWORD.read_value(auth_params)
        self.base_url = BASE_URL.read_value(auth_params)

    def get_headers(self):
        base64_credentials = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()
        return {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/json",
        }


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = MyIntegrationProvider(auth_params)
        url = f"{integration.base_url}/auth"
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
