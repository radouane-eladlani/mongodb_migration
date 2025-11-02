from pymongo import MongoClient

# -----------------------------
# 1. Connexion à MongoDB
# -----------------------------
# On se connecte au conteneur MongoDB sur le port 27017
# Adapter l'URL si l'authentification est activée
client = MongoClient("mongodb://data_engineer:password123@mongodb:27017/")
# Sélection de la base "hopital"
db = client["hopital"]
# Sélection de la collection "patients"
collection = db["patients"]

# -----------------------------
# 2. Vérification du nombre de documents
# -----------------------------
# On compte le nombre total de documents insérés
nb_docs = collection.count_documents({})
print(f"Nombre total de documents dans MongoDB : {nb_docs}")

# -----------------------------
# 3. Vérification des champs clés
# -----------------------------
# Exemple de document pour vérifier les colonnes
example = collection.find_one()

# Liste complète des colonnes du dataset
required_fields = [
    "Name", "Age", "Gender", "Blood Type", "Medical Condition",
    "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
    "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
    "Medication", "Test Results"
]

# Vérification de l'existence de tous les champs
missing_fields = [f for f in required_fields if f not in example]
if missing_fields:
    print(f"⚠️ Champs manquants : {missing_fields}")
else:
    print("✅ Tous les champs clés sont présents")

# -----------------------------
# 4. Détection des doublons
# -----------------------------
# On vérifie que chaque patient + date d'admission est unique
pipeline = [
    {"$group": {"_id": {"Name": "$Name", "Date of Admission": "$Date of Admission"}, "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]
duplicates = list(collection.aggregate(pipeline))
if duplicates:
    print(f"⚠️ Doublons détectés : {len(duplicates)}")
else:
    print("✅ Aucun doublon détecté")

# -----------------------------
# 5. Vérification des valeurs manquantes par champ
# -----------------------------
# On parcourt chaque champ clé et on compte les documents où il est absent
for field in required_fields:
    missing = collection.count_documents({field: {"$exists": False}})
    if missing:
        print(f"⚠️ Champ '{field}' manquant dans {missing} documents")
