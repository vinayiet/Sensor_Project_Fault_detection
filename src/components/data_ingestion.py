import logging
import sys 
import os
import numpy as np 
import pandas as pd

import pymongo as MongoClient
from zipfile import Path
from src.constants import *
from src.exceptions import CustomException
from src.utils import MainUtils
from dataclasses import dataclass



@dataclass
class  DataIngestionConfig:
    artifact_folder: str = os.path.join(artifacts_folder)


@dataclass
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_collection_as_dataframe(self, collection_name, db_name):
        try:
            mongo_client = MongoClient(MONGO_DB_URL)

            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis = 1)
            df.replace({'na': np.nan}, inplace = True)
            return df
        except Exception as e:
            raise CustomException(e,sys)
        
        def export_data_into_feature_store_file_path(self)->pd.DataFrame:

            try:
                logging.info("Exporting data from MongoDB to Feature Store")
                raw_file_path = self.data_ingestion_config.artifact_folder

                os.makedirs(raw_file_path, exist_ok=True)

                sensor_data = self.export_collection_as_dataframe(collection_name = MONGO_COLLECTION_NAME, db_name = MONGO_DATABASE_NAME)
                logging.info("Saving the exported data into feature store file path")

                feature_store_file_path = os.path.join(raw_file_path, "wafer_fault.csv")


                sensor_data.to_csv(feature_store_file_path, index = False)
            

            except Exception as e:
                raise CustomException(e,sys)
    
    def initiate_data_ingestion(self)->Path:
        logging.info("Initiating Data Ingestion")

        try:
            feature_store_file_path = self.export_data_into_feature_store_file_path()
            logging.info("Got the data from the mongodb and saved it into the feature store file path")

            logging.info('Exited the Data Ingestion')
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys)
        