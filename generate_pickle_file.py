"""
Script to train ML models and save them as pickle files
"""
import subprocess
import sys

# Install/upgrade the process_data package from GitHub
# Commented out to use local editable install instead
# print("Installing/upgrading process_data package...")
# subprocess.check_call([
#     sys.executable, "-m", "pip", "install", "--upgrade",
#     "git+https://github.com/ElvisCasco/process_data.git"
# ])
# print("Package installed successfully!\n")

import os
import joblib
import process_data as pdlib

# Get working directory
wd = os.getcwd()
print(f"Working directory: {wd}")

# Load and prepare data
print("\n" + "=" * 60)
print("Loading and preparing data...")
print("=" * 60)

csv_path = os.path.join(wd, "data", "sample_diabetes_mellitus_data.csv")
train_df, test_df = pdlib.data_split(csv_path, test_size=0.3, random_state=42)

# Clean data
cols_nan = ["age", "gender", "ethnicity"]
train_df = pdlib.data_remove_nans(train_df, columns=cols_nan)
test_df = pdlib.data_remove_nans(test_df, columns=cols_nan)

cols_fill = ["height", "weight"]
train_df = pdlib.data_fill_nans(train_df, columns=cols_fill)
test_df = pdlib.data_fill_nans(test_df, columns=cols_fill)

# Encode data
train_df = pdlib.data_encoding(train_df, columns=["ethnicity"])
test_df = pdlib.data_encoding(test_df, columns=["ethnicity"])

train_df = pdlib.data_binary(train_df, column="gender")
test_df = pdlib.data_binary(test_df, column="gender")

# Define features and target
FEATURES = [
    "age", "height", "weight",
    "aids", "cirrhosis", "hepatic_failure",
    "immunosuppression", "leukemia", "lymphoma",
    "solid_tumor_with_metastasis",
]
TARGET = "diabetes_mellitus"

X_train = train_df[FEATURES]
y_train = train_df[TARGET]

# Train models
print("\n" + "=" * 60)
print("Training models...")
print("=" * 60)

model_lr = pdlib.model_train_models(X_train, y_train, model_type="logreg")
model_rf = pdlib.model_train_models(X_train, y_train, model_type="rf")

print(f"Trained: {type(model_lr).__name__}")
print(f"Trained: {type(model_rf).__name__}")

# Save models as pickle files
print("\n" + "=" * 60)
print("Saving trained models as pickle files")
print("=" * 60)

model_lr_path = os.path.join(wd, "model_logistic_regression.pkl")
model_rf_path = os.path.join(wd, "model_random_forest.pkl")

joblib.dump(model_lr, model_lr_path)
joblib.dump(model_rf, model_rf_path)

print(f"\nModels saved successfully:")
print(f"  1. Logistic Regression: {model_lr_path}")
print(f"  2. Random Forest: {model_rf_path}")

# Verify file sizes
lr_size = os.path.getsize(model_lr_path) / 1024  # KB
rf_size = os.path.getsize(model_rf_path) / 1024  # KB

print(f"\nFile sizes:")
print(f"  Logistic Regression: {lr_size:.2f} KB")
print(f"  Random Forest: {rf_size:.2f} KB")

# Test loading the saved model
print(f"\nVerifying saved models...")
loaded_model_lr = joblib.load(model_lr_path)
X_test = test_df[FEATURES]
test_prediction = loaded_model_lr.predict_proba(X_test)[:5, 1]

print(f"  Loaded model type: {type(loaded_model_lr).__name__}")
print(f"  Test prediction sample: {test_prediction}")
print(f"\nModels successfully saved and verified!")
print("=" * 60)