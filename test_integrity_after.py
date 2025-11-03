import pytest
from pymongo import MongoClient

client = MongoClient("mongodb://data_engineer:password123@mongodb:27017/")
db = client["hopital"]
collection = db["patients"]

REQUIRED_FIELDS = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results"
]

def test_documents_count():
    nb_docs = collection.count_documents({})
    assert nb_docs > 0, "Aucun document dans MongoDB !"

def test_required_fields():
    example = collection.find_one()
    missing_fields = [f for f in REQUIRED_FIELDS if f not in example]
    assert not missing_fields, f"Champs manquants : {missing_fields}"

def test_no_duplicates():
    pipeline = [
        {"$group": {"_id": {"Name": "$Name", "Date of Admission": "$Date of Admission"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(collection.aggregate(pipeline))
    assert not duplicates, f"Doublons détectés : {len(duplicates)}"

def test_no_missing_values():
    for field in REQUIRED_FIELDS:
        missing = collection.count_documents({field: {"$exists": False}})
        assert missing == 0, f"Champ '{field}' manquant dans {missing} documents"
