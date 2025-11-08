# Diabetes Prediction API - Quick Start Guide

## 📋 Overview
This API provides diabetes mellitus predictions using trained Machine Learning models (Logistic Regression and Random Forest).

## 🚀 Starting the API

### Step 1: Activate virtual environment (optional)

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 2: Start the API server

```powershell
python api_fastapi.py
```

The API will start on: `http://localhost:8000`

---

## 📡 Available Endpoints

### 1. **GET /** - API Information
Get complete API documentation and usage examples.

```powershell
curl http://localhost:8000/
```

### 2. **GET /health** - Health Check
Check if the API is running and models are loaded.

```powershell
curl http://localhost:8000/health
```

### 3. **GET /models** - Model Information
Get details about loaded models.

```powershell
curl http://localhost:8000/models
```

---

## 🔮 Making Predictions

### 4. **POST /predict** - Single Prediction
Make a prediction for one patient using pre-loaded models.

**Using curl:**
```powershell
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d '{
    "model": "logreg",
    "features": {
      "age": 65,
      "height": 170,
      "weight": 75,
      "aids": 0,
      "cirrhosis": 0,
      "hepatic_failure": 0,
      "immunosuppression": 0,
      "leukemia": 0,
      "lymphoma": 0,
      "solid_tumor_with_metastasis": 0
    }
  }'
```

**Using Python:**
```python
import requests

data = {
    "model": "logreg",
    "features": {
        "age": 65,
        "height": 170,
        "weight": 75,
        "aids": 0,
        "cirrhosis": 0,
        "hepatic_failure": 0,
        "immunosuppression": 0,
        "leukemia": 0,
        "lymphoma": 0,
        "solid_tumor_with_metastasis": 0
    }
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

---

### 5. **POST /predict/batch** - Batch Predictions
Make predictions for multiple patients at once.

**Using Python:**
```python
import requests

data = {
    "model": "rf",
    "samples": [
        {
            "age": 65,
            "height": 170,
            "weight": 75,
            "aids": 0,
            "cirrhosis": 0,
            "hepatic_failure": 0,
            "immunosuppression": 0,
            "leukemia": 0,
            "lymphoma": 0,
            "solid_tumor_with_metastasis": 0
        },
        {
            "age": 45,
            "height": 165,
            "weight": 68,
            "aids": 0,
            "cirrhosis": 1,
            "hepatic_failure": 0,
            "immunosuppression": 0,
            "leukemia": 0,
            "lymphoma": 0,
            "solid_tumor_with_metastasis": 0
        }
    ]
}

response = requests.post("http://localhost:8000/predict/batch", json=data)
print(response.json())
```

---

### 6. **POST /predict/file** - Predictions from JSON File or Dictionary

This endpoint is the **most flexible** and supports:
- ✅ JSON file uploads
- ✅ JSON dictionaries in request body
- ✅ Custom model loading with `joblib.load()`
- ✅ Single or batch predictions

#### Option A: Using a JSON Dictionary

**Using Python:**
```python
import requests

data = {
    "model": "logreg",
    "data": {
        "age": 72,
        "height": 175,
        "weight": 85,
        "aids": 0,
        "cirrhosis": 0,
        "hepatic_failure": 0,
        "immunosuppression": 1,
        "leukemia": 0,
        "lymphoma": 0,
        "solid_tumor_with_metastasis": 1
    }
}

response = requests.post("http://localhost:8000/predict/file", json=data)
print(response.json())
```

#### Option B: Uploading a JSON File

**Create a file: `patient.json`**
```json
{
  "model": "logreg",
  "data": {
    "age": 65,
    "height": 170,
    "weight": 75,
    "aids": 0,
    "cirrhosis": 0,
    "hepatic_failure": 0,
    "immunosuppression": 0,
    "leukemia": 0,
    "lymphoma": 0,
    "solid_tumor_with_metastasis": 0
  }
}
```

**Using Python:**
```python
import requests

with open('patient.json', 'rb') as f:
    files = {'file': ('patient.json', f, 'application/json')}
    response = requests.post("http://localhost:8000/predict/file", files=files)
    print(response.json())
```

**Using curl:**
```powershell
curl -X POST http://localhost:8000/predict/file `
  -F "file=@example_patient_data.json"
```

#### Option C: Using a Custom Model

Load any `.pkl` model file using `joblib.load()`:

```python
import requests

data = {
    "model_path": "model_random_forest.pkl",  # Custom model path
    "data": {
        "age": 58,
        "height": 168,
        "weight": 72,
        "aids": 0,
        "cirrhosis": 0,
        "hepatic_failure": 0,
        "immunosuppression": 0,
        "leukemia": 0,
        "lymphoma": 0,
        "solid_tumor_with_metastasis": 0
    }
}

response = requests.post("http://localhost:8000/predict/file", json=data)
print(response.json())
```

#### Option D: Batch Predictions from JSON File

**Create a file: `patients_batch.json`**
```json
{
  "model": "rf",
  "data": [
    {
      "age": 65,
      "height": 170,
      "weight": 75,
      "aids": 0,
      "cirrhosis": 0,
      "hepatic_failure": 0,
      "immunosuppression": 0,
      "leukemia": 0,
      "lymphoma": 0,
      "solid_tumor_with_metastasis": 0
    },
    {
      "age": 45,
      "height": 165,
      "weight": 68,
      "aids": 0,
      "cirrhosis": 1,
      "hepatic_failure": 0,
      "immunosuppression": 0,
      "leukemia": 0,
      "lymphoma": 0,
      "solid_tumor_with_metastasis": 0
    }
  ]
}
```

---

## 🧪 Testing with Example Files

Three example files are included:

1. **`api_usage_examples.py`** - Complete Python script with all examples
2. **`example_patient_data.json`** - Single patient JSON file
3. **`example_batch_patients.json`** - Multiple patients JSON file

### Run all examples:
```powershell
python api_usage_examples.py
```

**Note:** Make sure the API is running first!

---

## 📊 Required Features

All predictions require these 10 features:

| Feature | Type | Values |
|---------|------|--------|
| `age` | float | Any positive number |
| `height` | float | Height in cm |
| `weight` | float | Weight in kg |
| `aids` | int | 0 or 1 |
| `cirrhosis` | int | 0 or 1 |
| `hepatic_failure` | int | 0 or 1 |
| `immunosuppression` | int | 0 or 1 |
| `leukemia` | int | 0 or 1 |
| `lymphoma` | int | 0 or 1 |
| `solid_tumor_with_metastasis` | int | 0 or 1 |

---

## 🎯 Response Format

All prediction endpoints return:

```json
{
  "model_used": "Logistic Regression",
  "prediction": {
    "class": 0,
    "probability": {
      "no_diabetes": 0.7234,
      "diabetes": 0.2766
    },
    "confidence": 0.7234
  },
  "input_features": {...}
}
```

- **class**: `0` = No diabetes, `1` = Has diabetes
- **probability**: Probability for each class (sums to 1.0)
- **confidence**: Highest probability (model certainty)

---

## 🛠️ Troubleshooting

### API won't start
- Check if models exist: `model_logistic_regression.pkl` and `model_random_forest.pkl`
- Run: `python generate_pickle_file.py` to create models

### Port already in use
- Stop other processes using port 8000
- Or change port in `api.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

### Module not found errors
- Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- Install requirements: `pip install flask joblib requests pandas numpy scikit-learn`

---

## 📚 Additional Resources

- **API Documentation**: Visit `http://localhost:8000/` when API is running
- **Model Information**: `http://localhost:8000/models`
- **Health Check**: `http://localhost:8000/health`

---

## ✅ Complete Workflow

```powershell
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Generate pickle models (first time only)
python generate_pickle_file.py

# 3. Start the API
python api_fastapi.py

# 4. In a new terminal, test the API
python api_usage_examples.py