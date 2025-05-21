from src.exceptions import CustomException
from src.logger import logging


import os
import sys
import numpy as np
import pandas as pd
from src.entity.config_entity import DataPreprocessingConfig, TrainingPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataPreprocessingArtifact


class DataPreprocessing:

    def __init__(self):
            training_pipeline_config = TrainingPipelineConfig()
            self.data_preprocessing_config = DataPreprocessingConfig(training_pipeline_config=training_pipeline_config)

            # 👇 Create DataIngestionArtifact INTERNALLY
            data_ingestion_artifact = DataIngestionArtifact(data_file_path=self.data_preprocessing_config.data_file_path)

            self.data_file_path = data_ingestion_artifact.data_file_path
            self.data_preprocessing_artifact = None

            logging.info(f"DataPreprocessing initialized with data file at: {self.data_file_path}")


    def fill_missing_values(self, dataframe: pd.DataFrame):
        try:
            logging.info("Filling missing values")
            logging.info("Filling missing values in the dataset")
            dataframe['Episode_Length_minutes'] = dataframe['Episode_Length_minutes'].fillna(dataframe['Episode_Length_minutes'].median())
            dataframe['Guest_Popularity_percentage'] = dataframe['Guest_Popularity_percentage'].fillna(dataframe['Guest_Popularity_percentage'].median())
            dataframe['Number_of_Ads'] = dataframe['Number_of_Ads'].fillna(dataframe['Number_of_Ads'].median())
            logging.info("completed Filling missing values")

            return dataframe

        except Exception as e:
            logging.error(f"Error during filling missing values: {e}")
            raise CustomException(e, sys)
    
    def replace_zero_values(self, dataframe: pd.DataFrame):
        try:
            logging.info("Replacing zero values in the dataset")

            # Define columns where 0 likely means missing
            cols_to_replace = ['Episode_Length_minutes', 'Host_Popularity_percentage', 
                            'Guest_Popularity_percentage', 'Listening_Time_minutes']

            # Keep only those columns which are present in the DataFrame
            existing_cols = [col for col in cols_to_replace if col in dataframe.columns]

            # Replace 0s with NaNs
            dataframe[existing_cols] = dataframe[existing_cols].replace(0, np.nan)

            # Impute NaNs with mean
            for col in existing_cols:
                dataframe[col] = dataframe[col].fillna(dataframe[col].mean())

            logging.info("Replaced zero values successfully with mean in the dataset")

            return dataframe

        except Exception as e:
            logging.error(f"Error during replacing zero values: {e}")
            raise CustomException(e, sys)

        

    def types_of_columns(self, dataframe: pd.DataFrame):
        try:
            logging.info("Identifying types of columns")
            # define numerical & categorical columns
            numeric_features = [feature for feature in dataframe.columns if dataframe[feature].dtype != 'O']
            categorical_features = [feature for feature in dataframe.columns if dataframe[feature].dtype == 'O']

            # print columns
            logging.info('We have {} numerical features : {}'.format(len(numeric_features), numeric_features))
            logging.info('\nWe have {} categorical features : {}'.format(len(categorical_features), categorical_features))


            return numeric_features, categorical_features

        except Exception as e:
            logging.error(f"Error during identifying types of columns: {e}")
            raise CustomException(e, sys)
        
    def remove_outliers(self, dataframe: pd.DataFrame, columns: list):
        try:
            logging.info("Removing outliers from the dataset")
            for col in columns:
                Q1 = dataframe[col].quantile(0.25)
                Q3 = dataframe[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                dataframe = dataframe[(dataframe[col] >= lower_bound) & (dataframe[col] <= upper_bound)]
                logging.info(f"Outliers removed from {col} using IQR method")
            return dataframe

        except Exception as e:
            logging.error(f"Error during removing outliers: {e}")
            raise CustomException(e, sys)
        


    def initiate_data_preprocessing(self):
        try:
            logging.info("Data Preprocessing started")

            # --- Load Data ---
            df = pd.read_csv(self.data_file_path)
            logging.info(f"Data loaded successfully from {self.data_file_path}")

            # --- Fill Missing Values ---
            df = self.fill_missing_values(df)

            # --- Replace Zero Values ---
            df = self.replace_zero_values(df)

            # --- Identify Types of Columns ---
            numeric_features, categorical_features = self.types_of_columns(df)

            # --- Remove Outliers ---
            df = self.remove_outliers(df, numeric_features)


            # --- Validate and Create Directory if not exists ---
            os.makedirs(os.path.dirname(self.data_preprocessing_config.cleaned_data_file_path), exist_ok=True)

            # --- Save Cleaned Data ---
            df.to_csv(self.data_preprocessing_config.cleaned_data_file_path, index=False)
            logging.info(f"Cleaned data saved at {self.data_preprocessing_config.cleaned_data_file_path}")

            self.data_preprocessing_artifact = DataPreprocessingArtifact(
                cleaned_data_file_path=self.data_preprocessing_config.cleaned_data_file_path
            )

            return self.data_preprocessing_artifact

        except Exception as e:
            logging.error(f"Error during data preprocessing: {e}")
            raise CustomException(e, sys)
        

