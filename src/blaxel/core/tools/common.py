from typing import Any, Dict, List, Optional, Type, TypedDict

from pydantic import BaseModel, Field, create_model

# Map JSON Schema types to Python types
json_type_mapping: Dict[str, Type] = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


class FunctionSchema(TypedDict, total=False):
    """Function schema type definition."""

    # List of schemas that this schema extends
    allOf: List[Any] | None
    # List of possible schemas, any of which this schema could be
    anyOf: List[Any] | None
    # Description of the schema
    description: str | None
    # Enum values
    enum: List[str] | None
    # Format of the schema
    format: str | None
    # Items schema for array types
    items: Optional["FunctionSchema"]
    # Maximum length for string types
    maxLength: int | None
    # Maximum value for number types
    maximum: float | None
    # Minimum length for string types
    minLength: int | None
    # Minimum value for number types
    minimum: float | None
    # Schema that this schema must not be
    not_: Dict[str, Any] | None
    # List of schemas, one of which this schema must be
    oneOf: List[Any] | None
    # Pattern for string types
    pattern: str | None
    # Properties of the schema
    properties: Dict[str, "FunctionSchema"] | None
    # Required properties of the schema
    required: List[str] | None
    # Title of the schema
    title: str | None
    # Type of the schema
    type: str | None

def create_model_from_json_schema(
    schema: Dict[str, Any], model_name: str = "DynamicModel"
) -> Type[BaseModel]:
    """
    To create a Pydantic model from the JSON Schema of MCP tools.

    Args:
        schema: A JSON Schema dictionary containing properties and required fields.
        model_name: The name of the model.

    Returns:
        A Pydantic model class.
    """
    properties = schema.get("properties", {})
    required_fields = set(schema.get("required", []))
    fields = {}

    for field_name, field_schema in properties.items():
        json_type = field_schema.get("type", "string")
        field_type = json_type_mapping.get(json_type, str)
        if field_name in required_fields:
            default_value = ...
        else:
            default_value = None
            field_type = field_type | None
        fields[field_name] = (
            field_type,
            Field(default_value, description=field_schema.get("description", "")),
        )
    return create_model(model_name, **fields)