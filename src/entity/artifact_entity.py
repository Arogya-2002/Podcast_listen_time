from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
   data_file_path: str

@dataclass
class DataPreprocessingArtifact:
   cleaned_data_file_path: str

@dataclass
class DataTransformationArtifact:
   cleaned_data_file_path: str

class ModelTrainerArtifact:
   model_save_path: str
   model_accuracy: float