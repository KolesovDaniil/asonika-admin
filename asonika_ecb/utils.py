from jsonschema import validate
from jsonschema.exceptions import ValidationError as JsonSchemaValidationError

from .exceptions import InvalidJSONSchema


def validate_schema(data: dict, schema: dict) -> None:
    try:
        validate(instance=data, schema=schema)
    except JsonSchemaValidationError as e:
        raise InvalidJSONSchema(e.message)
