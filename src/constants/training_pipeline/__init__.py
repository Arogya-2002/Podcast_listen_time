import os


"""
defining common constant variable for training pipeline
"""

TARGET_COLUMN = "Listening_Time_minutes"
PIPELINE_NAME: str = "PocastListenTime"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "submission.csv"

DATA_FILE_NAME: str = "train.csv"
VALIDATION_FILE_NAME: str = "test.csv"


CLEANED_DATA_FILE_NAME: str = "cleaned_data.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

DATASET_DIR_PATH: str = os.path.join("dataset")


SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

SPLIT_RATIO = 0.2



"""
Data Ingestion  realated constanat start with DATA_INGESTION VAR NAME
"""


"""
Data Transformation related constants
"""
TITLE_ENCODER_PATH = os.path.join( "title_encoder.pkl")
PODCAST_ENCODER_PATH = os.path.join( "podcast_encoder.pkl")
OTHER_CAT_ENCODER_PATH = os.path.join( "other_cat_encoder.pkl")
STANDARSCALER_PATH = os.path.join( "standard_scaler.pkl")