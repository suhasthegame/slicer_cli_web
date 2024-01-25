from .utils import generate_image_name_for_singularity
class SingularityCommands:
    @staticmethod
    def singularity_version():
        '''
        This method is used to check whether singularity is currently installed on the system.
        '''
        return ['singularity','--version']
    
    @staticmethod
    def singularity_pull(name:str, uri:str='docker'):
        '''
        This method is used to generate the command for the singualrity pull function for pulling images from online.
        Args:
        name(str.required) - Takes in a string that should specify the image name and tag as a single string '<image_name>:<tag>' 
        uri(str, optional) - If you want to pull the images from other that Dockerhub, you need to pass in that uri as a string

        Returns:
        A list of strings formatted to be supplied to the subprocess module of python that handles singularity pull. 
        '''
        sif_name = generate_image_name_for_singularity(name)
        return ['singularity','pull',sif_name,f'{uri}://{name}']
    