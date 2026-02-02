from .authentication import MyIntegrationProvider, test_authentication
from common.types import InputType, InputParameter, DataType, OutputParameter

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
QUERY = InputParameter(
    "QUERY",
    description="Query",
    data_type=DataType.STRING,
    optional=True,
)
LIMIT = InputParameter(
    "LIMIT",
    description="Limit",
    data_type=DataType.INT,
    optional=True,
)
OFFSET = InputParameter(
    "OFFSET",
    description="Offset",
    data_type=DataType.INT,
    optional=True,
)


### Output Parameters
STATUS = OutputParameter(
    name="STATUS",
    description="Status of the skill execution",
    data_type=DataType.STRING,
)
LOGS = OutputParameter(
    name="LOGS",
    description="Logs generated during execution",
    data_type=DataType.JSON,
)
### End of Output Parameters


def run_skill(input_params, auth_params):
    """This will be called to run the skill"""
    integration = MyIntegrationProvider(auth_params)
    test_authentication(auth_params)
    ## Logic Starts Here

    try:
        url = f"{integration.token_url}/query"  # Using token_url as base URL
        headers = integration.get_headers()
        payload = {
            "query": QUERY.read_value(input_params),
            "limit": LIMIT.read_value(input_params),
            "offset": OFFSET.read_value(input_params),
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return {
            "STATUS": response.status_code,
            "LOGS": response.json(),
        }
    except Exception as e:
        return {
            "STATUS": 500,
            "LOGS": str(e),
        }
    ## Logic Ends Here
