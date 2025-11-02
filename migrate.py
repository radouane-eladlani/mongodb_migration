import pandas as pd
from pymongo import MongoClient
import json

# -----------------------------
# 1. Connexion à MongoDB
# -----------------------------
# Ici, on se connecte au serveur qui tourne sur le conteneur Docker nommé "mongodb"
# Port 27017 par défaut pour MongoDB
client = MongoClient("mongodb://mongodb:27017/")
# Creation et sélection de la base de données "hopital"
base_de_donnees = client["hopital"]

# Creation et sélection de la collection "patients" dans cette base
collection_patients = base_de_donnees["patients"]

# -----------------------------
# 2. Lecture du fichier CSV
# -----------------------------
# On lit le fichier CSV contenant les données médicales
# Pandas crée un DataFrame, c'est comme un tableau en mémoire
donnees = pd.read_csv("healthcare_dataset.csv")

# -----------------------------
# 3. Vérification et test d'intégrité AVANT migration
# -----------------------------
print("\n------------------------------")
print("🔍 TEST D’INTÉGRITÉ AVANT MIGRATION")
print("------------------------------")
print("Nombre total de lignes :", len(donnees))
print("Colonnes disponibles :", list(donnees.columns))
print("Valeurs manquantes par colonne :")
print(donnees.isnull().sum())
print("Nombre de doublons :", donnees.duplicated().sum())
print("Types de variables :")
print(donnees.dtypes)

# -----------------------------
# 4. Nettoyage des données
# -----------------------------
# On supprime toutes les lignes qui sont entièrement vides
# Cela évite d'insérer des documents vides dans MongoDB
donnees = donnees.dropna(how="all")

# -----------------------------
# 5. Conversion en JSON
# -----------------------------
# MongoDB travaille avec des documents JSON
# On transforme le DataFrame Pandas en liste de dictionnaires JSON
liste_documents = json.loads(donnees.to_json(orient="records"))

# -----------------------------
# 6. Insertion des données dans MongoDB
# -----------------------------
if liste_documents:
    # Si la liste n'est pas vide, on insère tous les documents dans la collection "patients"
    collection_patients.insert_many(liste_documents)
    print(f"\n{len(liste_documents)} documents insérés dans la collection 'patients'.")
else:
    # Si aucune donnée n'est trouvée, on affiche un message
    print("\n⚠️ Aucune donnée à insérer.")

# -----------------------------
# 7. Vérification de l'insertion
# -----------------------------
# On récupère un document de la collection pour vérifier que l'insertion a fonctionné
print("\nExemple de document inséré :")
print(collection_patients.find_one())

# -----------------------------
# 8. Vérification et test d'intégrité APRÈS migration
# -----------------------------
print("\n------------------------------")
print("🔍 TEST D’INTÉGRITÉ APRÈS MIGRATION")
print("------------------------------")
nb_docs = collection_patients.count_documents({})
print(f"Nombre total de documents dans MongoDB : {nb_docs}")

# Vérification de cohérence simple
if nb_docs == len(donnees):
    print("Intégrité respectée : le nombre de lignes CSV = nombre de documents MongoDB")
else:
    print("⚠️ Alerte : incohérence détectée entre CSV et MongoDB")
