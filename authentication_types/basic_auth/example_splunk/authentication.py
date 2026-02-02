from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

### Connection Parameters
USERNAME = ConnectionParam(
    "USERNAME",
    description="Splunk Username",
    input_type=InputType.TEXT,
)
PASSWORD = ConnectionParam(
    "PASSWORD",
    description="Splunk Password",
    input_type=InputType.PASSWORD,
)
BASE_URL = ConnectionParam(
    "BASE_URL",
    description="Splunk Base URL",
    input_type=InputType.TEXT,
)
### End of Connection Parameters


class SplunkAuthentication:
    def __init__(self, auth_params):
        self.username = USERNAME.read_value(auth_params)
        self.password = PASSWORD.read_value(auth_params)
        self.base_url = BASE_URL.read_value(auth_params)
        self.auth = HTTPBasicAuth(self.username, self.password)

    def get_headers(self):
        return {
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def format_time(self, dt: datetime) -> str:
        """Format the datetime object to RFC 3339 compliant string"""
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = SplunkAuthentication(auth_params)

        # Simple test query
        test_query = "search index=_internal | head 5"

        payload = {
            "search": test_query,
        }

        search_url = f"{integration.base_url}/services/search/v2/jobs"

        # Attempt to start a search job
        response = requests.post(
            search_url,
            headers=integration.get_headers(),
            auth=integration.auth,
            data=payload,
            verify=False,
        )

        if response.status_code in [
            201,
            200,
        ]:  # Successfully started a search job
            return 200
        else:
            print(
                f"Failed to verify authentication with Splunk: {response.status_code}, {response.text}"
            )
            return 401
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except requests.exceptions.HTTPError as e:
        print(f"Authentication failed: {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            print(
                f"Response status: {e.response.status_code}, {e.response.text}"
            )
        return 401
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
