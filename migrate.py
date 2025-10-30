# Import les bibliothèques necessaires
import pandas as pd            # Pandas pour lire et manipuler le fichier CSV
from pymongo import MongoClient  # pymongo Pour se connecter à MongoDB
import json                     # Pour convertir le DataFrame en dictionnaires JSON

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
# 3. Nettoyage des données
# -----------------------------
# On supprime toutes les lignes qui sont entièrement vides
# Cela évite d'insérer des documents vides dans MongoDB
donnees = donnees.dropna(how="all")

# -----------------------------
# 4. Conversion en JSON
# -----------------------------
# MongoDB travaille avec des documents JSON
# On transforme le DataFrame Pandas en liste de dictionnaires JSON
liste_documents = json.loads(donnees.to_json(orient="records"))

# -----------------------------
# 5. Insertion des données dans MongoDB
# -----------------------------
if liste_documents:
    # Si la liste n'est pas vide, on insère tous les documents dans la collection "patients"
    collection_patients.insert_many(liste_documents)
    print(f"{len(liste_documents)} documents insérés dans la collection 'patients'.")
else:
    # Si aucune donnée n'est trouvée, on affiche un message
    print("Aucune donnée à insérer.")

# -----------------------------
# 6. Vérification de l'insertion
# -----------------------------
# On récupère un document de la collection pour vérifier que l'insertion a fonctionné
print("Exemple de document inséré :")
print(collection_patients.find_one())
