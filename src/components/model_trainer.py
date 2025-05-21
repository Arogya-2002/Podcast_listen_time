from src.exceptions import CustomException
from src.logger import logging

from src.entity.config_entity import TrainingPipelineConfig, ModelTrainerConfig
# from src.entity.artifact_entity import DataPreprocessingArtifact, DataTransformationArtifact, ModelTrainerArtifact
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import pickle


import os
import sys


class ModelTrainer:
    def __init__(self):
        training_pipeline_config = TrainingPipelineConfig()
        self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        self.clean_data_file_path = self.model_trainer_config.cleaned_data_file_path
        self.model_save_path = self.model_trainer_config.model_file_path


    def load_data(self):
        try:
            df = pd.read_csv(self.clean_data_file_path)
            X = df.drop(columns=["Listening_Time_minutes"])
            y = df["Listening_Time_minutes"]

            logging.info("splitting the data into X_train, X_val, y_train, y_val")
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
            logging.info("Data loaded and split successfully")
            return X_train, X_val, y_train, y_val
        except Exception as e:
            logging.error(f"Error during data loading: {e}")
            raise CustomException(e, sys)

    def create_model(self,input_dim):
        model = Sequential()
        model.add(Dense(128, activation='relu', input_shape=(input_dim,)))
        model.add(Dropout(0.3))

        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.3))

        model.add(Dense(1))  # Output layer

        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        
        return model
    
    def initiate_model_trainer(self):
        try:
            logging.info("Model Trainer initiated")
            logging.info("Loading the data")
            logging.info("Splitting the data into X_train, X_val, y_train, y_val")
            # Load and split the data
            X_train, X_val, y_train, y_val = self.load_data()
            logging.info("Data loaded and split successfully")

            logging.info("Creating the model")
            # Create the model
            model = self.create_model(input_dim=X_train.shape[1])
            logging.info("Model created successfully")

            logging.info("Fitting the model")

            early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
            )

            history = model.fit(
            X_train, y_train,
            epochs=2,
            validation_data=(X_val, y_val),
            callbacks=[early_stopping],
            batch_size=32
            )

            logging.info(f"Model trained successfully. Final validation loss: {history.history['val_loss'][-1]}")

            model_path = self.model_save_path
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            logging.info(f"Model saved at {model_path}")


            # Fit the model
            logging.info(f"Model trained successfully. Final validation loss: {history.history['val_loss'][-1]}")
        except Exception as e:
            raise CustomException(e, sys)
        

 
# if __name__ == "__main__":
#     model_trainer = ModelTrainer()
#     model_trainer.initiate_model_trainer()