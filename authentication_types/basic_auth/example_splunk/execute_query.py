from .authentication import SplunkAuthentication
from common.types import InputType, InputParameter, DataType, OutputParameter

# -----------------------------------------------------#
# Copy the code below and ignore the libraries above
# -----------------------------------------------------#

import requests
from datetime import datetime, timezone
import time
import random

### Input Parameters
INSTANCE = InputParameter(
    "INSTANCE",
    description="Instance to be used for fetching details",
    data_type=DataType.STRING,
)
QUERY = InputParameter(
    "QUERY",
    description="Query string to run in Splunk search language",
    data_type=DataType.STRING,
    optional=True,
)
START_TIME = InputParameter(
    "START_TIME",
    description="Start time in epoch format",
    data_type=DataType.STRING,
    optional=True,
)
END_TIME = InputParameter(
    "END_TIME",
    description="End time in epoch format",
    data_type=DataType.STRING,
    optional=True,
)
MAX_COUNT = InputParameter(
    "MAX_COUNT",
    description="Maximum number of results to retrieve",
    data_type=DataType.INT,
    optional=True,
)
### End of Input Parameters

### Output Parameters
STATUS = OutputParameter(
    name="STATUS",
    description="Status of the skill execution",
    data_type=DataType.STRING,
)
RESULTS = OutputParameter(
    name="RESULTS",
    description="Splunk search results",
    data_type=DataType.JSON,
)
### End of Output Parameters


def run_skill(input_params, auth_params):
    """
    This will be called to run the skill.
    Executes a Splunk search query and returns the results.
    """
    integration = SplunkAuthentication(auth_params)
    ## Logic Starts Here
    try:
        # Get input parameters
        query = QUERY.read_value(input_params)
        start_time = START_TIME.read_value(input_params)
        end_time = END_TIME.read_value(input_params)
        max_count = MAX_COUNT.read_value(input_params)

        # Set default times if not provided
        if not start_time:
            start_time = int(time.time()) - (5 * 60)  # 5 minutes ago
        if not end_time:
            end_time = int(time.time())  # current time

        # Step 1: Start the search job
        search_query = f"search {query}"
        api_start_time = time.time()

        data = {
            "search": search_query,
            "id": f"sid{random.randint(100000, 999999)}",
            "earliest_time": integration.format_time(
                datetime.fromtimestamp(start_time, tz=timezone.utc)
            ),
            "latest_time": integration.format_time(
                datetime.fromtimestamp(end_time, tz=timezone.utc)
            ),
            "max_count": max_count,
            "output_mode": "json",
        }

        search_url = f"{integration.base_url}/servicesNS/{integration.username}/search/search/jobs"

        # Start the search job
        response = requests.post(
            search_url,
            auth=integration.auth,
            data=data,
            headers=integration.get_headers(),
            verify=False,
        )
        response.raise_for_status()

        job_id = response.json().get("sid")

        # Step 2: Poll the search job status
        time_limit = 60 * 60  # 1 hour
        while True:
            if time.time() - api_start_time > time_limit:
                raise Exception("Search job exceeded time limit of 60 minutes")

            time.sleep(2)  # 2 seconds wait before checking status

            status_url = f"{integration.base_url}/servicesNS/{integration.username}/search/search/jobs/{job_id}"

            resp_job_status = requests.get(
                status_url,
                auth=integration.auth,
                headers=integration.get_headers(),
                params={"output_mode": "json"},
                verify=False,
            )
            resp_job_status.raise_for_status()

            is_job_completed = resp_job_status.json()["entry"][0]["content"][
                "dispatchState"
            ]

            if is_job_completed == "DONE":
                break
            elif is_job_completed == "FAILED":
                raise Exception("Search job failed")

        # Step 3: Retrieve the search results
        results_url = f"{integration.base_url}/servicesNS/{integration.username}/search/search/jobs/{job_id}/results"

        results_response = requests.get(
            results_url,
            auth=integration.auth,
            headers=integration.get_headers(),
            data={"output_mode": "json"},
            verify=False,
        )
        results_response.raise_for_status()

        results_json = results_response.json()

        return {
            "STATUS": results_response.status_code,
            "RESULTS": results_json,
        }
    except Exception as e:
        return {
            "STATUS": 500,
            "RESULTS": str(e),
        }
    ## Logic Ends Here
