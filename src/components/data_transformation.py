import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler, FunctionTransformer, StandardScaler

from src.constants import *
from src.exceptions import CustomException
from src.utils import MainUtils
from dataclasses import dataclass
import logging


@dataclass
def DataTransformationConfig():
    artifact_dir = os.path.join(artifacts_folder)
    transformed_train_file_path = os.path.join(artifacts_folder, 'train.npy')
    transformed_test_file_path = os.path.join(artifacts_folder, 'test.npy')
    transformed_target_file_path = os.path.join(artifacts_folder, 'preprocessor.pkl')





class DataTransformation:
    def __init__(self, feature_store_file_path):
        self.feature_store_file_path = feature_store_file_path
        self.data_transformation_config = DataTransformationConfig()
        self.utils = MainUtils()

    @staticmethod
    def get_data(feature_store_file_path:str) -> pd.DataFrame:
        try:
            logging.info("Reading data from Feature Store")
            data = pd.read_csv(feature_store_file_path)
            data.rename(columns={'Good/Bad', TARGET_COLUMN}, inplace=True)
            return data
        except Exception as e:
            raise CustomException(e, sys)


    def get_data_transformer(self):
        try:
            imputer_step = ('imputer', SimpleImputer(strategy='constant', fill_value= 0))
            scaler_step = ('scaler', RobustScaler())

            preprocessor = Pipeline(steps=[imputer_step, scaler_step]) 
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_transfor(self):
        logging.info("Initiating Data Transformation of data transformation") 
        try:
            dataframe = self.get_data(feature_store_file_path = self.feature_store_file_path)
            X = dataframe.drop(columns=[TARGET_COLUMN])
            Y = np.where(dataframe[TARGET_COLUMN] == -1, 1, 0)

            X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            preprocessor = self.get_data_transformer()

            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.transformed_target_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)


            self.utils.save_object(preprocessor, preprocessor_path)
            train_arr = np.c[X_train_scaled, np.array(y_train)]
            test_arr = np.c[X_test_scaled, np.array(y_test)]


            return train_arr, test_arr, preprocessor_path
        
        except Exception as e:
            raise CustomException(e, sys)