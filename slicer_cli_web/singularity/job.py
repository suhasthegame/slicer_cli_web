import os
from girder import logger
import subprocess
from .commands import SingularityCommands
from .utils import generate_image_name_for_singularity
from ..models import DockerImageNotFoundError

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
        subprocess.run(SingularityCommands.singularity_version(), check=True)
    except Exception as e:
        logger.exception(f"Exception {e} occured")
        raise Exception(f"Exception {e} occured")

def find_local_singularity_image(name:str,path=''):
    '''
    Check if the image is present locally on the system in a specified path. For our usecase, we insall the images to a specific path on /blue directory, which can be modified 
    via the argument to the function

    Args:
        name(str, required) - The name of the docker image with the tag <image>:<tag>.
        path(str, optional) - This path refers to the path on the local file system designated for placing singularity images after they are pulled from the interweb. 
    Returns:
    bool: True if the singularity image is avaialble on the given path on the local host system. False otherwise.

    '''
    try:
        sif_name = generate_image_name_for_singularity(name)
    except Exception:
        logger.exception("There's an error with the image name. Please check again and try")
        raise Exception("There's an error with the image name. Please check again and try")
    if not path:
        path = os.getenv('SIF_IMAGE_PATH', '')
        if not is_valid_path(path):
            logger.exception('Please provide a valid path or set the environment variable "SIF_IMAGE_PATH" and ensure the path has appropriate access')
            raise Exception('Please provide a valid path or set the environment variable "SIF_IMAGE_PATH" and ensure the path has appropriate access')
    return os.path.exists(path + sif_name)

def pull_image_and_convert_to_sif(names):
    '''
    This is the function similar to the pullDockerImage function that pulls the image from Dockerhub or other instances if it's supported in the future
    Args:
    names(List(str), required) -> The list of image names of the format <img>:<tag> provided as a string

    Raises:
    If pulling of any of the images fails, the function raises an error with the list of images that failed. 
    '''
    failedImageList  = []
    for name in names:
        try:
            logger.info(f"Starting to pull image {name}")
            pull_cmd = SingularityCommands.singularity_pull(name)
            subprocess.run(pull_cmd,check=True)
        except:
            failedImageList.append(name)
    if len(failedImageList) != 0:
        raise DockerImageNotFoundError('Could not find multiple images ',
                                       image_name=failedImageList)
    
