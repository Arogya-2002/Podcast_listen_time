# 🎵 Podcast Listening Time Prediction

This project is built to **predict how long a user is likely to listen to a podcast episode** using metadata as input. It encapsulates the full lifecycle of a machine learning project: from ingestion to deployment.

---

## 🧠 Objective

To develop a robust and production-ready ML system that:

* Takes structured metadata of podcast episodes
* Cleans, encodes, and processes the data
* Predicts user listening time (in minutes)
* Serves predictions via a FastAPI endpoint

---

## ⚙️ Key Features

* Modular pipeline design with reusable components
* Custom error handling for robustness
* FastAPI backend with CORS support
* Scalable and cloud-deployable via Docker + GitHub Actions + AWS ECR

---

## 📂 Project Structure

```text
src/
├── components/
│   ├── data_ingestion.py         # Loads input CSV
│   ├── data_preprocessing.py     # Missing values, outliers, zeros
│   ├── data_transformation.py    # Encodes, scales, drops cols
├── constants/
│   └── __init__.py               # Constants (paths, schema)
├── entity/
│   ├── config_entity.py          # Config definitions
│   ├── artifact_entity.py        # Artifact definitions
├── exceptions/
│   └── __init__.py               # Custom exception class
├── logger.py                     # Logging support
├── pipeline/
│   └── prediction_pipeline.py    # Pipeline controller
app.py                            # FastAPI backend
```

---

## 🔄 End-to-End Flow

```text
CSV Input File
   ↓
Data Ingestion
   ↓
Data Preprocessing (nulls, zeros, outliers)
   ↓
Data Transformation (encode, scale)
   ↓
Prediction (model.pkl)
   ↓
Output: Listening Time (minutes)
```

---

## 🔹 Detailed Module Descriptions

### 1. `data_ingestion.py`

* Verifies and loads CSV file
* Returns ingestion artifact with file path

### 2. `data_preprocessing.py`

* Handles:

  * Missing values
  * Zero replacements
  * Outlier removal (IQR-based)

### 3. `data_transformation.py`

* Label encodes categorical variables (e.g., Podcast, Title)
* Drops irrelevant columns post-encoding

### 4. `prediction_pipeline.py`

* Loads trained model (`model.pkl`)
* Applies full transformation to new data
* Returns predictions

### 5. `app.py`

* FastAPI service that:

  * Accepts CSV via `/predict/`
  * Applies prediction pipeline
  * Returns top 10 predictions in JSON

---

## 📈 Target Variable

**`Listening_Time_minutes`** - predicted total user listening time for an episode.

---

## ⛨️ Error Handling

Errors across all components are caught using a custom exception class `CustomException`, which includes tracebacks and debug info.

---

## 📊 API Usage

### Start the API Server:

```bash
uvicorn app:app --reload or python app.py
```

### Endpoint:

```
POST /predict/
```

### Request:

* Content-Type: multipart/form-data
* Input: CSV file

### Response:

* JSON array of top 10 predictions

```json
[
  {
    "id": 123,
    "Listening_Time_minutes": 28.4
  },
  ...
]
```

---

## 📄 Input File Format

```csv
id,Podcast,Title,Duration,...
1,"The Tech Pod","AI Trends",34,...
```

Ensure all required features are present and clean.

---

## ⚖️ Configuration & Constants

Defined in: `src/constants/__init__.py`

| Constant           | Description                  |
| ------------------ | ---------------------------- |
| `DATA_FILE_NAME`   | CSV input file name          |
| `SCHEMA_FILE_PATH` | Path to schema JSON          |
| `MODEL_FILE_NAME`  | Path to trained model        |
| `SAVED_MODEL_DIR`  | Directory to save/load model |

---

## 🚀 Docker Deployment

### Dockerfile:

```dockerfile
FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app
RUN apt update -y && apt install awscli -y
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

### Build & Run:

```bash
docker build -t podcast-predictor .
docker run -p 8000:8000 podcast-predictor
```
### Buiding an docker image manually is optional as the action will do it for you.

---

## 📦 CI/CD with GitHub Actions

### File: `.github/workflows/main.yaml`

### Workflow Stages:

1. **Integration**

   * Installs dependencies
   * Placeholder for linting & unit tests

2. **Delivery**

   * Builds Docker image
   * Pushes to Amazon ECR

3. **Deployment**

   * Self-hosted EC2 runner
   * Pulls latest image
   * Runs container on port `8000`

### Secrets Required:

| Secret Key              | Description         |
| ----------------------- | ------------------- |
| `AWS_ACCESS_KEY_ID`     | AWS credentials     |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials     |
| `AWS_REGION`            | AWS region          |
| `AWS_ECR_LOGIN_URI`     | ECR login URI       |
| `ECR_REPOSITORY`        | ECR repository name |

---

## 🌐 API Flowchart

```text
+---------------------+
|   Input CSV Upload  |
+---------------------+
           |
           v
+---------------------+
|  Data Ingestion     |
+---------------------+
           |
           v
+---------------------+
| Preprocessing       |
| (missing, outliers) |
+---------------------+
           |
           v
+---------------------+
| Transformation      |
| (label encode)      |
+---------------------+
           |
           v
+---------------------+
| Model Prediction    |
+---------------------+
           |
           v
+---------------------+
| JSON Output         |
+---------------------+
```

---

## 🚚 Install Requirements

```bash
pip install -r requirements.txt
```

---

## 📧 Contact

**Author:** Vamshi
For queries or collaborations, feel free to reach out.


For setting up AWS and Git Hub actions please follow the below document

[text](https://docs.google.com/document/d/1AgYis5BDO1UQcvgdYWF5rbcHFOOBXmHIrPfO31nuxYs/edit?usp=sharing)