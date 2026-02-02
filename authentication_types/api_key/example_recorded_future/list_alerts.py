from .authentication import RecordedFutureAuthentication
from common.types import InputParameter, DataType, OutputParameter

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
from datetime import datetime, timezone  # import extra libraries if needed
import time  # import extra libraries if needed

### Input Parameters
INSTANCE = InputParameter(
    "INSTANCE",
    description="Instance to be used for fetching details",
    data_type=DataType.STRING,
)
FROM_INDEX = InputParameter(
    "FROM_INDEX",
    description="Starting index for pagination",
    data_type=DataType.INT,
    optional=True,
)
LIMIT = InputParameter(
    "LIMIT",
    description="Maximum number of alerts to return",
    data_type=DataType.INT,
    optional=True,
)
START_TIME = InputParameter(
    "START_TIME",
    description="Start timestamp in epoch format",
    data_type=DataType.STRING,
    optional=True,
)
END_TIME = InputParameter(
    "END_TIME",
    description="End timestamp in epoch format",
    data_type=DataType.STRING,
    optional=True,
)
ASSIGNEE = InputParameter(
    "ASSIGNEE",
    description="Filter alerts by assignee",
    data_type=DataType.STRING,
    optional=True,
)
STATUS_IN_PORTAL = InputParameter(
    "STATUS_IN_PORTAL",
    description="Filter alerts by status in portal",
    data_type=DataType.STRING,
    optional=True,
)
ORDER_BY = InputParameter(
    "ORDER_BY",
    description="Field to order results by",
    data_type=DataType.STRING,
    optional=True,
)
DIRECTION = InputParameter(
    "DIRECTION",
    description="Sort direction ('asc' or 'desc')",
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
ALERTS = OutputParameter(
    name="ALERTS",
    description="List of Recorded Future alerts",
    data_type=DataType.JSON,
)
### End of Output Parameters


def run_skill(input_params, auth_params):
    """This will be called to run the skill"""
    integration = RecordedFutureAuthentication(auth_params)
    ## Logic Starts Here
    try:
        api_start_time = time.time()

        # Read all input parameters
        start_time = START_TIME.read_value(input_params)
        end_time = END_TIME.read_value(input_params)

        # Set end_time to current time if start_time provided but no end_time
        if start_time and not end_time:
            end_time = int(datetime.now().timestamp())

        # Build payload
        payload = {}

        # Handle time range
        if start_time and end_time:
            start_dt = datetime.fromtimestamp(
                start_time, timezone.utc
            ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
            end_dt = datetime.fromtimestamp(end_time, timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )
            payload["triggered"] = f"[{start_dt}, {end_dt}]"

        # Add optional parameters to payload
        optional_params = {
            "assignee": ASSIGNEE.read_value(input_params),
            "statusInPortal": STATUS_IN_PORTAL.read_value(input_params),
            "limit": LIMIT.read_value(input_params),
            "from": FROM_INDEX.read_value(input_params),
            "orderBy": ORDER_BY.read_value(input_params),
            "direction": DIRECTION.read_value(input_params),
        }

        # Add non-None values to payload
        payload.update(
            {k: v for k, v in optional_params.items() if v is not None}
        )

        url = f"{integration.api_url}/alert/v3"
        headers = integration.get_headers()

        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()

        alerts = response.json()
        print(
            f"Alerts fetched successfully, time_taken={time.time() - api_start_time}"
        )
        return {
            "STATUS": response.status_code,
            "ALERTS": alerts,
        }
    except Exception as e:
        return {
            "STATUS": 500,
            "ALERTS": str(e),
        }
    ## Logic Ends Here
