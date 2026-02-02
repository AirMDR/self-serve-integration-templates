from common.types import InputType, ConnectionParam

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

from typing import Dict, Any
import requests


### Connection Parameters
CLIENT_ID = ConnectionParam(
    "CLIENT_ID",
    description="Microsoft Graph API Client ID",
    input_type=InputType.PASSWORD,
)
CLIENT_SECRET = ConnectionParam(
    "CLIENT_SECRET",
    description="Microsoft Graph API Client Secret",
    input_type=InputType.PASSWORD,
)
TENANT_ID = ConnectionParam(
    "TENANT_ID",
    description="Microsoft Azure Tenant ID",
    input_type=InputType.TEXT,
)
### End of Connection Parameters


class MicrosoftGraphAuthentication:
    def __init__(self, auth_params):
        self.client_id = CLIENT_ID.read_value(auth_params)
        self.client_secret = CLIENT_SECRET.read_value(auth_params)
        self.tenant_id = TENANT_ID.read_value(auth_params)
        self.auth_url = "https://login.microsoftonline.com"
        self.base_url = "https://graph.microsoft.com"
        self.auth_token_url = (
            f"{self.auth_url}/{self.tenant_id}/oauth2/v2.0/token"
        )
        self.access_token = None

    def get_headers(self):
        """Get headers with bearer token"""
        if not self.access_token:
            auth_response = self._get_graph_auth_token()
            self.access_token = auth_response.get("access_token")
            if not self.access_token:
                raise ValueError("Failed to obtain bearer token")

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get_graph_auth_token(self) -> Dict[str, Any]:
        """Get authentication token from Microsoft Graph API"""
        auth_scope = "https://graph.microsoft.com/.default"
        grant_type = "client_credentials"

        payload = (
            f"client_id={self.client_id}"
            f"&client_secret={self.client_secret}"
            f"&scope={auth_scope}"
            f"&grant_type={grant_type}"
        )

        response = requests.post(
            url=self.auth_token_url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()


def test_authentication(auth_params):  # must have function
    """This will be called to verify authentication from UI"""
    try:
        integration = MicrosoftGraphAuthentication(auth_params)
        auth_scope = "https://graph.microsoft.com/.default"
        grant_type = "client_credentials"

        payload = (
            f"client_id={integration.client_id}"
            f"&client_secret={integration.client_secret}"
            f"&scope={auth_scope}"
            f"&grant_type={grant_type}"
        )

        url = (
            f"{integration.auth_url}/{integration.tenant_id}/oauth2/v2.0/token"
        )
        response = requests.post(url=url, data=payload)
        response.raise_for_status()

        if response.json().get("access_token"):
            return 200
        return 401
    except ValueError as e:
        print(f"Missing required parameter: {str(e)}")
        return 400
    except requests.exceptions.HTTPError as e:
        print(f"Authentication failed: {str(e)}")
        return 401
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return 401
