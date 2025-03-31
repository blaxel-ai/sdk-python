from typing import Any, Dict, Optional, Type

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
            field_type = Optional[field_type]
        fields[field_name] = (
            field_type,
            Field(default_value, description=field_schema.get("description", "")),
        )
    return create_model(model_name, **fields)