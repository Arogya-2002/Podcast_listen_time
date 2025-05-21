from src.exceptions import CustomException
from src.logger import logging
import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
from typing import List, Tuple
from src.entity.config_entity import DataTransformationConfig, TrainingPipelineConfig
from src.entity.artifact_entity import DataPreprocessingArtifact, DataTransformationArtifact

from sklearn.preprocessing import StandardScaler


class DataTransformation:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.data_transformation_config = DataTransformationConfig(training_pipeline_config=training_pipeline_config)

        data_preprocessing_artifact = DataPreprocessingArtifact(    
            cleaned_data_file_path=self.data_transformation_config.cleaned_data_file_path
        )

        self.data_file_path = data_preprocessing_artifact.cleaned_data_file_path
        self.data_transformation_artifact = None    

        # Move hardcoded columns into init for clean reference
        self.columns_to_encode = self.data_transformation_config.columns_to_encode
        self.columns_to_drop = self.data_transformation_config.columns_to_drop

    def label_encoding(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Starting label encoding for Podcast_Name and Episode_Title.")

            podcast_le = LabelEncoder()
            title_le = LabelEncoder()

            podcast_le.fit(dataframe['Podcast_Name'])
            title_le.fit(dataframe['Episode_Title'])

            dataframe['Podcast_ID'] = podcast_le.transform(dataframe['Podcast_Name'])
            dataframe['Title_ID'] = title_le.transform(dataframe['Episode_Title'])

            os.makedirs(os.path.dirname(self.data_transformation_config.podcast_encoder_path), exist_ok=True)
            os.makedirs(os.path.dirname(self.data_transformation_config.title_encoder_path), exist_ok=True)

            with open(self.data_transformation_config.podcast_encoder_path, "wb") as f:
                pickle.dump(podcast_le, f)
            with open(self.data_transformation_config.title_encoder_path, "wb") as f:
                pickle.dump(title_le, f)

            logging.info("Label encoders saved successfully.")

            return dataframe
        except Exception as e:
            logging.error(f"Error during label encoding: {e}")
            raise CustomException(e, sys)

    def other_columns_encoding(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Starting encoding for other categorical columns.")

            encoders = {}

            for col in self.columns_to_encode:
                cat_encoder = LabelEncoder()
                dataframe[col] = cat_encoder.fit_transform(dataframe[col])
                encoders[col] = cat_encoder

            os.makedirs(os.path.dirname(self.data_transformation_config.other_encoder_path), exist_ok=True)
            with open(self.data_transformation_config.other_encoder_path, "wb") as f:
                pickle.dump(encoders, f)

            logging.info("Other column encoders saved successfully.")

            return dataframe
        except Exception as e:
            logging.error(f"Error during other columns encoding: {e}")
            raise CustomException(e, sys)

    def drop_unwanted_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info(f"Dropping unwanted columns: {self.columns_to_drop}")
            dataframe.drop(columns=self.columns_to_drop, inplace=True)
            return dataframe
        except Exception as e:
            logging.error(f"Error during dropping unwanted columns: {e}")
            raise CustomException(e, sys)

    # def split_data_as_train_test(self, dataframe: pd.DataFrame) -> DataTransformationArtifact:
    #     try:
    #         logging.info("Splitting dataframe into train and test sets.")

    #         train_df, test_df = train_test_split(
    #             dataframe,
    #             test_size=self.data_transformation_config.split_ratio,
    #             random_state=42
    #         )

    #         os.makedirs(os.path.dirname(self.data_transformation_config.train_file_path), exist_ok=True)
    #         os.makedirs(os.path.dirname(self.data_transformation_config.test_file_path), exist_ok=True)

    #         train_df.to_csv(self.data_transformation_config.train_file_path, index=False)
    #         test_df.to_csv(self.data_transformation_config.test_file_path, index=False)

    #         logging.info(f"Train and test files saved successfully.")

    #         return DataTransformationArtifact(
    #             train_file_path=self.data_transformation_config.train_file_path,
    #             test_file_path=self.data_transformation_config.test_file_path
                
    #         )
    #     except Exception as e:
    #         logging.error(f"Error during train-test split: {e}")
    #         raise CustomException(e, sys)


    def standardize_data(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        try:
            logging.info("Standardizing data.")
            numeric_cols = dataframe.select_dtypes(include=['float64', 'int64']).columns
            
            sc = StandardScaler()
            dataframe[numeric_cols] = sc.fit_transform(dataframe[numeric_cols])
            os.makedirs(os.path.dirname(self.data_transformation_config.standard_scaler_path), exist_ok=True)
            with open(self.data_transformation_config.standard_scaler_path, "wb") as f:
                            pickle.dump(sc, f)

            logging.info("Other column encoders saved successfully.")


            return dataframe
        except Exception as e:
            logging.error(f"Error during data standardization: {e}")
            raise CustomException(e, sys)

    def initiate_data_transformation(self, dataframe: pd.DataFrame, columns: List[str]) -> DataTransformationArtifact:
        try:
            logging.info("Initiating complete data transformation pipeline.")

            dataframe = self.label_encoding(dataframe)
            dataframe = self.other_columns_encoding(dataframe)

            # Validate new columns before dropping originals
            if not all(col in dataframe.columns for col in ['Podcast_ID', 'Title_ID']):
                raise CustomException("Label encoding failed, 'Podcast_ID' or 'Title_ID' missing.", sys)

            dataframe = self.drop_unwanted_columns(dataframe)
            # dataframe = self.standardize_data(dataframe)


            logging.info("Data transformation pipeline completed successfully.")

            # --- Validate and Create Directory if not exists ---
            os.makedirs(os.path.dirname(self.data_transformation_config.cleaned_data_file_path), exist_ok=True)

            # --- Save Cleaned Data ---
            dataframe.to_csv(self.data_transformation_config.cleaned_data_file_path, index=False)
            logging.info(f"Cleaned data saved at {self.data_transformation_config.cleaned_data_file_path}")

            self.data_transformation_artifact = DataTransformationArtifact(
                cleaned_data_file_path=self.data_transformation_config.cleaned_data_file_path
            )

            return self.data_transformation_artifact
        except Exception as e:
            logging.error(f"Error in data transformation pipeline: {e}")
            raise CustomException(e, sys)




# if __name__ == "__main__":
#     # Example usage
#     data_transformation = DataTransformation()
#     data_transformation.initiate_data_transformation(pd.read_csv(data_transformation.data_file_path), data_transformation.columns_to_encode)
#     print("Data transformation completed successfully.")