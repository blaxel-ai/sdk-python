Module blaxel.common.utils
==========================
This module provides utility functions for file operations within Blaxel.
It includes functions to copy folders and synchronize directory contents efficiently.

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