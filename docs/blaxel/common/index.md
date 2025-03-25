Module blaxel.common
====================

Sub-modules
-----------
* blaxel.common.error
* blaxel.common.instrumentation
* blaxel.common.logger
* blaxel.common.secrets
* blaxel.common.settings
* blaxel.common.utils

Functions
---------

`copy_folder(source_folder: str, destination_folder: str)`
:   Copies the contents of the source folder to the destination folder.
    
    This function recursively copies all files and subdirectories from the `source_folder` to the `destination_folder`.
    It ensures that existing files are only overwritten if they differ from the source.
    
    Parameters:
        source_folder (str): The path to the source directory.
        destination_folder (str): The path to the destination directory.
    
    Raises:
        FileNotFoundError: If the source folder does not exist.
        PermissionError: If the program lacks permissions to read from the source or write to the destination.

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

`init_logger(log_level: str)`
:   Initializes the logging configuration for Blaxel.
    
    This function clears existing handlers for specific loggers, sets up a colored formatter,
    and configures the root logger with the specified log level.
    
    Parameters:
        log_level (str): The logging level to set (e.g., "DEBUG", "INFO").

`slugify(name: str) ‑> str`
:   Converts a given string into a URL-friendly slug.
    
    This function transforms the input string by converting it to lowercase and replacing spaces and underscores with hyphens.
    
    Parameters:
        name (str): The string to slugify.
    
    Returns:
        str: The slugified version of the input string.

Classes
-------

`HTTPError(status_code: int, message: str)`
:   A custom exception class for HTTP errors.
    
    Attributes:
        status_code (int): The HTTP status code associated with the error.
        message (str): A descriptive message explaining the error.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`Secret()`
:   A utility class for managing environment secrets.
    
    Provides static methods to retrieve and set secret values, supporting both standard and
    prefixed environment variable naming conventions.

    ### Static methods

    `get(name: str)`
    :   Retrieves the value of a secret environment variable.
        
        This method first attempts to get the value using the standard name. If not found,
        it tries with a "bl_" prefix.
        
        Parameters:
            name (str): The name of the environment variable to retrieve.
        
        Returns:
            str: The value of the environment variable if found, otherwise an empty string.

    `set(name: str, value: str)`
    :   Sets the value of a secret environment variable.
        
        This method sets the value using the standard name, allowing for consistent secret management.
        
        Parameters:
            name (str): The name of the environment variable to set.
            value (str): The value to assign to the environment variable.

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