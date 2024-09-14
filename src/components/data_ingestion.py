import logging
import sys
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constants import MONGO_DB_URL, MONGO_COLLECTION_NAME, MONGO_DATABASE_NAME, artifacts_folder
from src.exceptions import CustomException
from src.utils import main_utils
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifacts_folder)

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = main_utils()  # Assuming main_utils is a class and you need to instantiate it

    def export_collection_as_dataframe(self, collection_name, db_name) -> pd.DataFrame:
        """
        Exports a MongoDB collection as a pandas DataFrame.
        """
        try:
            # Initialize MongoDB client
            mongo_client = MongoClient(MONGO_DB_URL)
            
            # Access the collection
            collection = mongo_client[db_name][collection_name]
            
            # Convert the collection data to a DataFrame
            df = pd.DataFrame(list(collection.find()))

            # Drop the '_id' column if it exists
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
                
            # Replace 'na' strings with NaN
            df.replace({'na': np.nan}, inplace=True)
            
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_into_feature_store_file_path(self) -> str:
        """
        Exports data from MongoDB and saves it as a CSV file in the feature store path.
        """
        try:
            logging.info("Exporting data from MongoDB to Feature Store")
            
            # Define the raw file path
            raw_file_path = self.data_ingestion_config.artifact_folder

            # Create the directory if it doesn't exist
            os.makedirs(raw_file_path, exist_ok=True)

            # Fetch data from MongoDB as a DataFrame
            sensor_data = self.export_collection_as_dataframe(collection_name=MONGO_COLLECTION_NAME, 
                                                              db_name=MONGO_DATABASE_NAME)
            logging.info("Saving the exported data into feature store file path")

            # Define the full path for saving the CSV file
            feature_store_file_path = os.path.join(raw_file_path, "wafer_fault.csv")

            # Save the DataFrame to a CSV file
            sensor_data.to_csv(feature_store_file_path, index=False)
            
            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self) -> str:
        """
        Initiates the data ingestion process and returns the feature store file path.
        """
        logging.info("Initiating Data Ingestion")

        try:
            # Export data to the feature store file path
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            logging.info("Got the data from MongoDB and saved it into the feature store file path")

            logging.info("Exited the Data Ingestion")
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e, sys)
