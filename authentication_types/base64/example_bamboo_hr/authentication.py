from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
import base64


### Connection Parameters
API_KEY = ConnectionParam(
    "API_KEY",
    description="BambooHR API Key",
    input_type=InputType.PASSWORD,
)
COMPANY_DOMAIN = ConnectionParam(
    "COMPANY_DOMAIN",
    description="BambooHR Company Domain (e.g., company.bamboohr.com)",
    input_type=InputType.TEXT,
)
### End of Connection Parameters


class BambooHRAuthentication:
    def __init__(self, auth_params):
        self.api_key = API_KEY.read_value(auth_params)
        self.company_domain = COMPANY_DOMAIN.read_value(auth_params)
        self.base_url = f"https://{self.company_domain}/api/v1"

    def get_headers(self):
        credentials = f"{self.api_key}:x"  # BambooHR uses API key as username and 'x' as password
        base64_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/json",
        }


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = BambooHRAuthentication(auth_params)

        # Make a test API call to fetch minimal employee data
        url = f"{integration.base_url}/employees/0"
        headers = integration.get_headers()
        params = {
            "fields": "firstName,lastName",
            "onlyCurrent": "1",
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        return 200
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except requests.exceptions.HTTPError as e:
        print(f"Authentication failed: {str(e)}")
        return 401
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
