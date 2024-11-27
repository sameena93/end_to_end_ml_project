from setuptools import find_packages, setup
from typing import List


#funtion to get the packages
def get_requirements(file_path:str)->List[str]:
    """
    This function will return the list of requirements"""

    requirements =[]
    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.replace('\n',"") for req in requirements]

        if "-e ." in requirements:
            requirements.remove("-e .")
    return requirements



setup(
    name="mlproject",
    version='0.0.1',
    author='Sameena',
    author_email='Sameenamujawar101@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)