import pandas as pd

df = pd.read_csv("healthcare_dataset.csv")

REQUIRED_FIELDS = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results"
]

def test_columns_present():
    missing = [f for f in REQUIRED_FIELDS if f not in df.columns]
    assert not missing, f"Champs manquants dans CSV : {missing}"

def test_no_missing_values():
    missing_count = df[REQUIRED_FIELDS].isna().sum().sum()
    assert missing_count == 0, f"Valeurs manquantes : {missing_count}"

def test_no_duplicates():
    duplicates = df.duplicated(subset=["Name", "Date of Admission"]).sum()
    assert duplicates == 0, f"Doublons détectés : {duplicates}"
