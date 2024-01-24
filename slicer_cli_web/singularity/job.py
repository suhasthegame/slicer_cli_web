import os
from girder import logger
import subprocess
from .commands import SingularityCommands

def is_valid_path(path):
    """
    Check if the provided path is a valid and accessible path in the file system.

    Parameters:
    path (str): The path to check.

    Returns:
    bool: True if the path is valid and accessible, False otherwise.
    """
    return os.path.exists(path) and os.access(path, os.R_OK)


def is_singularity_installed(path=None):
    """This function is used to check whether singularity is availble on the target system. 
    This function is useful to make sure that singularity is accessible from a SLURM job submitted to HiperGator

    Args:
        path (str, optional): If the user wants to provide a specific path where singularity is installed, you can provide that path. Defaults to None.

    Returns:
    bool: True if singualrity is successfully accessible on the target system. False otherwise
    """
    try:
        if path and is_valid_path(path):
            os.chdir(path)
    except Exception:
        logger.exception(f'{path} is not a valid path')
        raise Exception(
            f'{path} is not a valid path'   
        )
    try:
        
    