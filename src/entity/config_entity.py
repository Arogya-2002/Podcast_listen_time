from datetime import datetime
import os
from src.constants import training_pipeline

print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp
        

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: training_pipeline):
        self.data_file_path: str = os.path.join(training_pipeline.DATASET_DIR_PATH, training_pipeline.DATA_FILE_NAME)
        self.validation_file_path: str = os.path.join(training_pipeline.DATASET_DIR_PATH, training_pipeline.VALIDATION_FILE_NAME)

class DataPreprocessingConfig:
    def __init__(self, training_pipeline_config: training_pipeline):
        self.data_file_path: str = os.path.join(training_pipeline.DATASET_DIR_PATH, training_pipeline.DATA_FILE_NAME)
        self.cleaned_data_file_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.CLEANED_DATA_FILE_NAME)
       
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: training_pipeline):
        self.cleaned_data_file_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.CLEANED_DATA_FILE_NAME)
        self.split_ratio: float = training_pipeline.SPLIT_RATIO
        self.train_file_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.TRAIN_FILE_NAME)
        self.test_file_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.TEST_FILE_NAME)
        self.title_encoder_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.TITLE_ENCODER_PATH)
        self.podcast_encoder_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.PODCAST_ENCODER_PATH)
        self.other_encoder_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.OTHER_CAT_ENCODER_PATH)
        self.standard_scaler_path: str = os.path.join(training_pipeline.ARTIFACT_DIR, training_pipeline.STANDARSCALER_PATH)
        self.columns_to_encode: list= ["Genre", "Publication_Day", "Publication_Time","Episode_Sentiment"]
        self.columns_to_drop: list = ["Podcast_Name", "Episode_Title"]

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: training_pipeline):
        self.cleaned_data_file_path: str = DataTransformationConfig(training_pipeline_config).cleaned_data_file_path
        self.model_file_path: str = os.path.join(training_pipeline.SAVED_MODEL_DIR, training_pipeline.MODEL_FILE_NAME)
        