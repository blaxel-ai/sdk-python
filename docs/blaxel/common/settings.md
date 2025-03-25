Module blaxel.common.settings
=============================
This module defines the configuration management system for Blaxel applications using Pydantic.
It includes dataclasses for various configuration aspects, such as agents, authentication, and server settings.
The module provides functions to initialize settings, load configurations from YAML files, and customize settings sources.

Functions
---------

`get_settings() ‑> blaxel.common.settings.Settings`
:   Retrieves the current settings instance.
    
    Returns:
        Settings: The current settings configuration.

`init() ‑> blaxel.common.settings.Settings`
:   Initializes the settings by parsing the `blaxel.yaml` file and setting up logging.
    
    This function reads workspace configuration from the current context,
    initializes the global SETTINGS variable, and configures the logger based on the log level.
    
    Returns:
        Settings: The initialized settings configuration.

Classes
-------

`Settings(**data)`
:   Base class for settings, allowing values to be overridden by environment variables.
    
    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku and any 12 factor app design.
    
    All the below attributes can be set via `model_config`.
    
    Args:
        _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
            Defaults to `None`.
        _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
            Defaults to `False`.
        _env_prefix: Prefix for all environment variables. Defaults to `None`.
        _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
            means that the value from `model_config['env_file']` should be used. You can also pass
            `None` to indicate that environment variables should not be loaded from an env file.
        _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
        _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
        _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
        _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
            into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
        _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
        _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
            Otherwse, defaults to sys.argv[0].
        _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
            If set to `True`, defaults to sys.argv[1:].
        _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
        _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
            `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
            _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
        _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
        _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
        _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
        _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
            Defaults to `False`.
        _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
            Defaults to `True`.
        _cli_prefix: The root parser command line arguments prefix. Defaults to "".
        _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
        _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
            (e.g. --flag, --no-flag). Defaults to `False`.
        _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
        _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `agent: blaxel.common.settings.SettingsAgent`
    :

    `app_url: str`
    :

    `authentication: blaxel.common.settings.SettingsAuthentication`
    :

    `base_url: str`
    :

    `cloud: bool`
    :

    `deploy: bool`
    :

    `enable_opentelemetry: bool`
    :

    `log_level: str`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

    `name: str`
    :

    `registry_url: str`
    :

    `remote: bool`
    :

    `run_internal_hostname: str`
    :

    `run_url: str`
    :

    `server: blaxel.common.settings.SettingsServer`
    :

    `type: str`
    :

    `workspace: str`
    :

    ### Static methods

    `settings_customise_sources(settings_cls: Type[pydantic_settings.main.BaseSettings], init_settings: pydantic_settings.sources.PydanticBaseSettingsSource, env_settings: pydantic_settings.sources.PydanticBaseSettingsSource, dotenv_settings: pydantic_settings.sources.PydanticBaseSettingsSource, file_secret_settings: pydantic_settings.sources.PydanticBaseSettingsSource) ‑> Tuple[pydantic_settings.sources.PydanticBaseSettingsSource, ...]`
    :   Define the sources and their order for loading the settings values.
        
        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.
        
        Returns:
            A tuple containing the sources and their order for loading the settings values.

`SettingsAgent(**values: Any)`
:   Configuration settings for agents within Blaxel.
    
    Attributes:
        agent (Union[None, CompiledGraph]): The compiled agent graph.
        chain (Union[None, list[Agent]]): A list of agent chains.
        model (Union[None, Model]): The model configuration.
        functions (Union[None, list[Function]]): A list of functions available to agents.
        functions_directory (str): The directory path where agent functions are located.
        chat_model (Union[None, BaseChatModel]): The chat model used by agents.
        module (str): The module path to the main application.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `agent: langgraph.graph.graph.CompiledGraph | None`
    :

    `chain: list[blaxel.models.agent.Agent] | None`
    :

    `chat_model: langchain_core.language_models.chat_models.BaseChatModel | None`
    :

    `functions: list[blaxel.models.function.Function] | None`
    :

    `functions_directory: str`
    :

    `model: blaxel.models.model.Model | None`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

    `module: str`
    :

`SettingsAuthentication(**values: Any)`
:   Base class for settings, allowing values to be overridden by environment variables.
    
    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku and any 12 factor app design.
    
    All the below attributes can be set via `model_config`.
    
    Args:
        _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
            Defaults to `None`.
        _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
            Defaults to `False`.
        _env_prefix: Prefix for all environment variables. Defaults to `None`.
        _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
            means that the value from `model_config['env_file']` should be used. You can also pass
            `None` to indicate that environment variables should not be loaded from an env file.
        _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
        _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
        _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
        _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
            into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
        _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
        _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
            Otherwse, defaults to sys.argv[0].
        _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
            If set to `True`, defaults to sys.argv[1:].
        _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
        _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
            `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
            _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
        _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
        _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
        _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
        _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
            Defaults to `False`.
        _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
            Defaults to `True`.
        _cli_prefix: The root parser command line arguments prefix. Defaults to "".
        _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
        _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
            (e.g. --flag, --no-flag). Defaults to `False`.
        _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
        _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `apiKey: str | None`
    :

    `client: blaxel.common.settings.SettingsAuthenticationClient`
    :

    `jwt: str | None`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

`SettingsAuthenticationClient(**values: Any)`
:   Configuration settings for authentication clients.
    
    Attributes:
        credentials (Union[None, str]): Client credentials for authentication.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `credentials: str | None`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

`SettingsServer(**values: Any)`
:   Base class for settings, allowing values to be overridden by environment variables.
    
    This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose),
    Heroku and any 12 factor app design.
    
    All the below attributes can be set via `model_config`.
    
    Args:
        _case_sensitive: Whether environment and CLI variable names should be read with case-sensitivity.
            Defaults to `None`.
        _nested_model_default_partial_update: Whether to allow partial updates on nested model default object fields.
            Defaults to `False`.
        _env_prefix: Prefix for all environment variables. Defaults to `None`.
        _env_file: The env file(s) to load settings values from. Defaults to `Path('')`, which
            means that the value from `model_config['env_file']` should be used. You can also pass
            `None` to indicate that environment variables should not be loaded from an env file.
        _env_file_encoding: The env file encoding, e.g. `'latin-1'`. Defaults to `None`.
        _env_ignore_empty: Ignore environment variables where the value is an empty string. Default to `False`.
        _env_nested_delimiter: The nested env values delimiter. Defaults to `None`.
        _env_parse_none_str: The env string value that should be parsed (e.g. "null", "void", "None", etc.)
            into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.
        _env_parse_enums: Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.
        _cli_prog_name: The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`.
            Otherwse, defaults to sys.argv[0].
        _cli_parse_args: The list of CLI arguments to parse. Defaults to None.
            If set to `True`, defaults to sys.argv[1:].
        _cli_settings_source: Override the default CLI settings source with a user defined instance. Defaults to None.
        _cli_parse_none_str: The CLI string value that should be parsed (e.g. "null", "void", "None", etc.) into
            `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to "null" if
            _cli_avoid_json is `False`, and "None" if _cli_avoid_json is `True`.
        _cli_hide_none_type: Hide `None` values in CLI help text. Defaults to `False`.
        _cli_avoid_json: Avoid complex JSON objects in CLI help text. Defaults to `False`.
        _cli_enforce_required: Enforce required fields at the CLI. Defaults to `False`.
        _cli_use_class_docs_for_groups: Use class docstrings in CLI group help text instead of field descriptions.
            Defaults to `False`.
        _cli_exit_on_error: Determines whether or not the internal parser exits with error info when an error occurs.
            Defaults to `True`.
        _cli_prefix: The root parser command line arguments prefix. Defaults to "".
        _cli_flag_prefix_char: The flag prefix character to use for CLI optional arguments. Defaults to '-'.
        _cli_implicit_flags: Whether `bool` fields should be implicitly converted into CLI boolean flags.
            (e.g. --flag, --no-flag). Defaults to `False`.
        _cli_ignore_unknown_args: Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.
        _secrets_dir: The secret files directory or a sequence of directories. Defaults to `None`.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `directory: str`
    :

    `host: str`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

    `module: str`
    :

    `port: int`
    :