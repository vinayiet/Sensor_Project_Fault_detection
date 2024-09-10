import sys
from typing import Dict
import os
import pandas as pd 
import pickle
import yaml
import boto3

from src.contants import *
from src.exceptions import CustomException
from src.logger import logging


class MainUtils:
    def __init__(self):
        pass

    def read_yaml(self, file_path: str) -> Dict:
        """
        Read yaml file
        """
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            return data
        except Exception as e:
            error_message = f"Error occurred while reading yaml file: {file_path}"
            logging.error(error_message)
            raise CustomException(error_message, sys)

    def read_schema_config(self, file_path: str) -> Dict:
        """
        Read schema config file
        """
        try:
            schema_config = self.read_yaml(file_path)  # Fix: Pass the correct single file_path argument
            return schema_config
        except Exception as e:
            error_message = f"Error occurred while reading schema config file: {file_path}"
            logging.error(error_message)
            raise CustomException(error_message, sys)
        
    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        """
        Save a Python object to a file using pickle
        """
        logging.info(f"Saving object to file: {file_path}")

        try:
            with open(file_path, 'wb') as file:
                pickle.dump(obj, file)
            logging.info(f"Object saved successfully to file: {file_path}")
        except Exception as e:
            error_message = f"Error occurred while saving object to file: {file_path}"
            logging.error(error_message)
            raise CustomException(error_message, sys)

    @staticmethod
    def load_object(file_path: str) -> object:
        """
        Load a Python object from a pickle file
        """
        logging.info(f"Loading object from file: {file_path}")

        try:
            with open(file_path, 'rb') as file:
                obj = pickle.load(file)
            logging.info(f"Object loaded successfully from file: {file_path}")
            return obj
        except Exception as e:
            error_message = f"Error occurred while loading object from file: {file_path}"
            logging.error(error_message)
            raise CustomException(error_message, sys)
