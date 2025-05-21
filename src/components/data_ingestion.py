from src.exceptions import CustomException
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from src.entity.artifact_entity import DataIngestionArtifact
import os
import sys



class DataIngestion:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig() 
        self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        self.data_ingestion_artifact = None


    def initiate_data_ingestion(self):
        try:
            logging.info("Data Ingestion started")

            # --- Validate source data file exists ---
            if not os.path.exists(self.data_ingestion_config.data_file_path):
                raise FileNotFoundError(f"Source data file not found at {self.data_ingestion_config.data_file_path}")

            logging.info(f"Data loaded successfully from {self.data_ingestion_config.data_file_path}")

            self.data_ingestion_artifact = DataIngestionArtifact(
                data_file_path=self.data_ingestion_config.data_file_path
            )

            logging.info("Data Ingestion completed successfully")
            return self.data_ingestion_artifact

        except Exception as e:
            logging.error(f"Error during data ingestion: {e}")
            raise CustomException(e, sys)


# if __name__ == "__main__":
    # data_ingestion = DataIngestion()
    # data_ingestion.initiate_data_ingestion()
    # print("Data ingestion completed successfully.")