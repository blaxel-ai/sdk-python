Module blaxel.core.tools.common
===============================

Functions
---------

`create_model_from_json_schema(schema: Dict[str, Any], model_name: str = 'DynamicModel') ‑> Type[pydantic.main.BaseModel]`
:   To create a Pydantic model from the JSON Schema of MCP tools.
    
    Args:
        schema: A JSON Schema dictionary containing properties and required fields.
        model_name: The name of the model.
    
    Returns:
        A Pydantic model class.