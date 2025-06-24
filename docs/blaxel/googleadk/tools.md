Module blaxel.googleadk.tools
=============================

Functions
---------

`bl_tools(tools_names: list[str], **kwargs: Any) ‑> list[google.adk.tools.base_tool.BaseTool]`
:   

Classes
-------

`GoogleADKTool(tool: blaxel.core.tools.types.Tool)`
:   The base class for all tools.

    ### Ancestors (in MRO)

    * google.adk.tools.base_tool.BaseTool
    * abc.ABC

    ### Methods

    `run_async(self, *, args: dict[str, typing.Any], tool_context: google.adk.tools.tool_context.ToolContext) ‑> Any`
    :   Runs the tool with the given arguments and context.
        
        NOTE
        - Required if this tool needs to run at the client side.
        - Otherwise, can be skipped, e.g. for a built-in GoogleSearch tool for
          Gemini.
        
        Args:
          args: The LLM-filled arguments.
          tool_context: The context of the tool.
        
        Returns:
          The result of running the tool.