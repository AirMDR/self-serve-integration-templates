from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests


### Connection Parameters
OAUTH_TOKEN_URL = ConnectionParam(
    "OAUTH_TOKEN_URL",
    description="OAuth Token URL",
    input_type=InputType.TEXT,
)
CLIENT_ID = ConnectionParam(
    "CLIENT_ID",
    description="OAuth Client ID",
    input_type=InputType.PASSWORD,
)
CLIENT_SECRET = ConnectionParam(
    "CLIENT_SECRET",
    description="OAuth Client Secret",
    input_type=InputType.PASSWORD,
)
SCOPE = ConnectionParam(
    "SCOPE",
    description="OAuth Scope (space-separated)",
    input_type=InputType.TEXT,
)
### End of Connection Parameters


class MyIntegrationProvider:
    def __init__(self, auth_params):
        self.token_url = OAUTH_TOKEN_URL.read_value(auth_params)
        self.client_id = CLIENT_ID.read_value(auth_params)
        self.client_secret = CLIENT_SECRET.read_value(auth_params)
        self.scope = SCOPE.read_value(auth_params)
        self.access_token = None

    def get_headers(self):
        if not self.access_token:
            self._get_access_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get_access_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.scope,
        }
        response = requests.post(
            self.token_url,
            headers={"Content-Type": "application/json"},
            json=payload,
        )
        if response.status_code >= 200 and response.status_code < 300:
            self.access_token = response.json().get("access_token")


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = MyIntegrationProvider(auth_params)
        integration._get_access_token()
        if integration.access_token:
            return 200
        return 401
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
