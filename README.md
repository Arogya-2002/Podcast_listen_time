# 🎵 Podcast Listening Time Prediction

A machine learning-based system that predicts how long a user is likely to listen to a podcast episode, based on episode metadata. This project includes a complete pipeline from data ingestion to a deployable prediction API.

---

## 🧠 Objective

Build a regression model that estimates `Listening_Time_minutes` for podcast episodes using structured metadata like title, podcast ID, duration, and more.

---

## ⚙️ Features

* Modular, production-grade ML pipeline
* Structured exception handling
* Data preprocessing, cleaning, and transformation
* Prediction via REST API (FastAPI)
* CORS-enabled for integration with web frontends
* Well-organized project structure

---

## 📂 Pipeline Flow

```
Raw CSV File
    ↓
Data Ingestion
    ↓
Data Preprocessing (handle missing values, outliers, zero values)
    ↓
Data Transformation (encoding, scaling, dropping irrelevant features)
    ↓
Model Inference (prediction using trained model)
    ↓
Output: JSON with predicted listening time
```

---

## 🔺 Project Structure

```bash
src/
├── components/
│   ├── data_ingestion.py          # Loads and validates input data
│   ├── data_preprocessing.py      # Handles missing data, zero values, outliers
│   ├── data_transformation.py     # Encodes categorical variables, drops unnecessary columns
├── constants/
│   └── __init__.py                # Centralized constants for filenames, paths, etc.
├── entity/
│   ├── config_entity.py           # Pipeline configuration schema
│   ├── artifact_entity.py         # Artifact structures for component output
├── exceptions/
│   └── __init__.py                # Custom exception class with stack trace logging
├── logger.py                      # Configures logging for the pipeline
├── pipeline/
│   └── prediction_pipeline.py     # Runs full prediction pipeline on input data
app.py                             # FastAPI app for serving predictions
```

---

## 🔢 Key Components

### 1. `data_ingestion.py`

* Validates the existence of input CSV
* Returns a data artifact containing the file path

### 2. `data_preprocessing.py`

* `fill_missing_values()` - fills nulls with appropriate strategies
* `replace_zero_values()` - replaces invalid zero values
* `types_of_columns()` - detects numeric and categorical columns
* `remove_outliers()` - removes outliers using IQR

### 3. `data_transformation.py`

* `label_encoding()` - label encodes Title and Podcast columns
* `other_columns_encoding()` - encodes other categorical fields
* `drop_unwanted_columns()` - removes original string-based columns

### 4. `prediction_pipeline.py`

* Loads `model.pkl`
* Applies preprocessing and transformation on the uploaded file
* Makes predictions and maps them to the corresponding ID

### 5. `app.py`

* Exposes `/predict/` API endpoint
* Accepts CSV via `multipart/form-data`
* Returns top 10 predictions in JSON

---

## 🔢 Target Column

The model predicts:

```text
Listening_Time_minutes
```

---

## 🚨 Error Handling

* Custom error class `CustomException` is used across the codebase.
* Provides detailed traceback, filename, and line number for easier debugging.

---

## 🌐 API Endpoint

### Start the Server

```bash
uvicorn app:app --reload
```

### Prediction Endpoint

```
POST /predict/
```

* **Consumes:** CSV file (`multipart/form-data`)
* **Returns:** JSON with `ID` and predicted `Listening_Time_minutes`

---

## 📄 Input File Format

Required columns in CSV:

```
id, Podcast, Title, Duration, ...
```

---

## 🔧 Configuration & Constants

Defined in `src/constants/__init__.py`

Important Constants:

* `DATA_FILE_NAME`: input file name
* `SCHEMA_FILE_PATH`: path to schema YAML
* `SAVED_MODEL_DIR`: location where model is saved
* `MODEL_FILE_NAME`: trained model filename

---

## 📂 Requirements

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📧 Contact

**Author:** Vamshi
For queries or contributions, feel free to reach out.

---

## 🔹 Pipeline Diagram

```
+-------------------+
|  Raw Input CSV    |
+-------------------+
          |
          v
+------------------------------+
|     Data Ingestion           |
| (check file exists, load)    |
+------------------------------+
          |
          v
+------------------------------+
|    Data Preprocessing        |
| (fill missing, zero, outliers)|
+------------------------------+
          |
          v
+------------------------------+
|   Data Transformation        |
| (encode categorical vars)    |
+------------------------------+
          |
          v
+------------------------------+
|       Model Prediction       |
|   (load model.pkl & predict) |
+------------------------------+
          |
          v
+------------------------------+
|     Output JSON Response     |
|   [ID, Predicted Time]       |
+------------------------------+
```
