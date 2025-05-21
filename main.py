from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataPreprocessing
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import TrainingPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.logger import logging
import os
import sys
from src.exceptions import CustomException
from src.constants import training_pipeline
import pandas as pd

data_ingestion = DataIngestion()
data_ingestion.initiate_data_ingestion()
print("Data ingestion completed successfully.")

data_preprocessing = DataPreprocessing()
data_preprocessing.initiate_data_preprocessing()
print("Data preprocessing completed successfully.")

data_transformation = DataTransformation()
data_transformation.initiate_data_transformation(pd.read_csv(data_transformation.data_file_path), data_transformation.columns_to_encode)
print("Data transformation completed successfully.")

model_trainer = ModelTrainer()
model_trainer.initiate_model_trainer()

