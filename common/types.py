from enum import Enum
from typing import Dict, Any
import json


class DataType(Enum):
    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    JSON = "json"


class InputType(Enum):
    TEXT = "text"
    PASSWORD = "password"
    URL = "url"
    NUMBER = "number"
    BOOLEAN = "boolean"
    TIMESTAMP = "timestamp"
    LIST = "list"
    OAUTH_URL = "oauth_url"
    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"


def convert_value(value: any, data_type: DataType) -> Any:
    try:
        if data_type == DataType.INT:
            return int(value)
        elif data_type == DataType.FLOAT:
            return float(value)
        elif data_type == DataType.BOOL:
            if isinstance(value, str):
                return value.lower() == "true"
            else:
                return bool(value)
        elif data_type == DataType.JSON:
            if isinstance(value, str):
                return json.loads(value)
        return value
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Could not convert value {value} to {data_type}: {str(e)}"
        )


class ConnectionParam:
    def __init__(
        self,
        name: str,
        description: str = "",
        label: str = "",
        optional: bool = False,
        data_type: DataType = DataType.STRING,
        input_type: str = InputType.TEXT,
    ):
        self.name = name
        self.description = description
        self.label = label
        self.optional = optional
        self.data_type = data_type
        self.input_type = input_type

    def read_value(self, input_params: Dict[str, Any]) -> Any:
        if self.name not in input_params:
            if not self.optional:
                raise ValueError(f"Missing required parameter: {self.name}")
            return None
        return convert_value(input_params[self.name], self.data_type)


class InputParameter:
    def __init__(
        self,
        name: str,
        description: str = "",
        label: str = "",
        default_value: any = None,
        optional: bool = False,
        data_type: DataType = DataType.STRING,
        input_type: str = InputType.TEXT,
    ):
        self.name = name
        self.description = description
        self.label = label
        self.default_value = default_value
        self.optional = optional
        self.data_type = data_type
        self.input_type = input_type

    def read_value(self, input_params: Dict[str, Any]) -> str:
        if self.name not in input_params:
            if not self.optional:
                raise ValueError(f"Missing required parameter: {self.name}")
            return None
        return convert_value(input_params[self.name], self.data_type)


class OutputParameter:
    def __init__(
        self,
        name: str,
        data_type: DataType = DataType.STRING,
        description: str = "",
    ):
        self.name = name
        self.data_type = data_type
        self.description = description
