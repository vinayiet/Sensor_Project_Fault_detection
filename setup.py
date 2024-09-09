from setuptools import  find_packages, setup
from typing import List


def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace('\n', '') for requirement in requirements]
    return requirements


setup(
    name= 'fault_detection',
    version= '0.1',
    author='Vinay',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages(),
)

