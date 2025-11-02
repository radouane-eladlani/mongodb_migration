import pandas as pd
from pymongo import MongoClient
import json

# -----------------------------
# 1. Connexion à MongoDB
# -----------------------------
client = MongoClient("mongodb://data_engineer:password123@mongodb:27017/")
db = client["hopital"]
collection_patients = db["patients"]

# -----------------------------
# 2. Lecture du fichier CSV
# -----------------------------
donnees = pd.read_csv("healthcare_dataset.csv")

# -----------------------------
# 3. Nettoyage des données
# -----------------------------
# Supprime les lignes entièrement vides
donnees = donnees.dropna(how="all")

# -----------------------------
# 4. Conversion en JSON
# -----------------------------
liste_documents = json.loads(donnees.to_json(orient="records"))

# -----------------------------
# 5. Insertion dans MongoDB
# -----------------------------
if liste_documents:
    collection_patients.insert_many(liste_documents)
    print(f"{len(liste_documents)} documents insérés dans la collection 'patients'.")
else:
    print("⚠️ Aucune donnée à insérer.")

# -----------------------------
# 6. Vérification simple
# -----------------------------
print("Exemple de document inséré :")
print(collection_patients.find_one())