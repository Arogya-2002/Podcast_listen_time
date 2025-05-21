from src.exceptions import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, ModelTrainerConfig
from src.components.data_preprocessing import DataPreprocessing
from src.components.data_transformation import DataTransformation

import os
import sys
import pandas as pd
import joblib
import pickle
import numpy as np

class PredictionPipeline:
    def __init__(self):
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
        self.validation_file_path = data_ingestion_config.validation_file_path

        model_trainer_config = ModelTrainerConfig(training_pipeline_config=TrainingPipelineConfig())
        self.model_file_path = model_trainer_config.model_file_path
        self.data_preprocessing = DataPreprocessing()
        self.data_transformation = DataTransformation()
    def initiate_prediction(self,valid_df: pd.DataFrame)-> pd.DataFrame:

        try:

            logging.info("Loading the Validation file for prediction") 

            # valid_df = pd.read_csv(self.validation_file_path)



            logging.info("Loading the Validation file for prediction") 

            # --- Fill Missing Values ---
            valid_df = self.data_preprocessing.fill_missing_values(valid_df)

                        # --- Replace Zero Values ---
            valid_df = self.data_preprocessing.replace_zero_values(valid_df)

                        # --- Identify Types of Columns ---
            numeric_features, categorical_features = self.data_preprocessing.types_of_columns(valid_df)

                        # --- Remove Outliers ---
            valid_df = self.data_preprocessing.remove_outliers(valid_df, numeric_features)


            valid_df = self.data_transformation.label_encoding(valid_df)
            valid_df = self.data_transformation.other_columns_encoding(valid_df)

            # Validate new columns before dropping originals
            if not all(col in valid_df.columns for col in ['Podcast_ID', 'Title_ID']):
                raise CustomException("Label encoding failed, 'Podcast_ID' or 'Title_ID' missing.", sys)


            if 'id' not in valid_df.columns:
                raise CustomException("ID column not found in validation data.", sys)

            id_column = valid_df['id'].copy()

            valid_df = self.data_transformation.drop_unwanted_columns(valid_df)
            # valid_df = data_transformation.standardize_data(valid_df)



            with open(self.model_file_path, "rb") as f:
                model = pickle.load(f)

            predictions = model.predict(valid_df)
            logging.info("Prediction completed.")

            rounded_predictions = np.round(predictions.flatten(), 3)

            results_df = pd.DataFrame({
                'ID': id_column,
                'Predicted_Listening_Time': rounded_predictions  
            })

            # Save predictions to CSV
            # results_df.to_csv("predictions.csv", index=False)
            # logging.info("Predictions saved to predictions.csv")

            


            # print(predictions)



            return results_df
        
        
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise CustomException(e, sys)
