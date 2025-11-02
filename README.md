# Projet : Migration des données médicales vers MongoDB

## 1. Contexte
Ce projet a pour objectif de migrer le dataset médical `healthcare_dataset.csv` vers MongoDB afin de faciliter la gestion et l’analyse des données patients.

## 2. Rôle du script `migrate.py`
Le script Python `migrate.py` :
1. Se connecte à MongoDB via `pymongo`.  
2. Crée (ou sélectionne) la base de données `hopital` et la collection `patients`.  
3. Lit le fichier CSV et transforme chaque ligne en document JSON.  
4. Supprime les lignes vides pour éviter les documents vides.  
5. Insère tous les documents dans la collection `patients`.  
6. Affiche un exemple de document et le nombre total de documents insérés.

## 3. Installation des modules Python
1. Vérifier que Python 3 est installé.  
2. Installer les modules requis avec pip3 :
pip3 install -r requirements.txt

## 4. Lancer MongoDB avec Docker

### 4.1 Méthode simple (conteneur unique)
Lancer MongoDB sur le port 27017 :
docker exec -it mongodb_local mongosh

### 4.2 Vérifier que le conteneur est actif :
docker ps

### 4.3 Avec Docker Compose (automatiser la migration)
Exemple docker-compose.yml utilisé :
version: "3.8"  

services:
  # Conteneur MongoDB
  mongodb:
    image: mongo:6.0       
    container_name: mongodb_local
    ports:
      - "27017:27017"
    environment:
      # Variables d'environnement pour créer un utilisateur sécurisé
      MONGO_INITDB_ROOT_USERNAME: data_engineer
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: hopital
    volumes:
      - mongo_data:/data/db          # Volume pour persister les données MongoDB
      - csv_data:/data/csv           # Volume pour stocker les CSV
    restart: unless-stopped           # Redémarre automatiquement sauf si on l'arrête manuellement

  # Conteneur pour exécuter la migration
  migration:
    build: .                         # Construire l'image depuis le Dockerfile
    container_name: migration_app    # Nom du conteneur
    volumes:
      - ./healthcare_dataset.csv:/data/csv/healthcare_dataset.csv  # Monter le CSV dans le conteneur
    depends_on:
      - mongodb                      # Attend que MongoDB soit démarré avant d'exécuter
    command: >
      sh -c "
        echo 'Attente du démarrage de MongoDB...' &&
        sleep 10 &&
        echo 'Lancement du script de migration...' &&
        python migrate.py
      "

  # Conteneur pour automatiser le test d'intégrité
  tests:
    build: .                         # Construire l'image depuis le Dockerfile
    container_name: test_app         # Nom du conteneur
    depends_on:
      - mongodb
      - migration                     # Attend que MongoDB et la migration soient terminés
    command: python test_integrity.py # Script de test d’intégrité

# Définition des volumes persistants
volumes:
  mongo_data:
  csv_data:

### 4.4 Système d’authentification et rôles utilisateurs
Pour sécuriser l’accès à la base MongoDB, un utilisateur est créé automatiquement via Docker Compose :

Nom d’utilisateur : data_engineer
Mot de passe : password123
Rôle : root (accès complet à la base hopital)
Cette configuration est définie dans le docker-compose.yml :

environment:
  MONGO_INITDB_ROOT_USERNAME: data_engineer
  MONGO_INITDB_ROOT_PASSWORD: password123
  MONGO_INITDB_DATABASE: hopital
Cela permet de protéger la base et de créer facilement d’autres utilisateurs avec des droits limités (lecture seule, lecture/écriture sur certaines collections, etc.).

## 5. Lancer l’ensemble 
docker-compose up --build

## 6. Vérifier les logs pour s’assurer que la migration s’est bien déroulée :
docker-compose logs migration

## 6.1 lancer un test :
docker-compose run --rm tests

## 7. Exécuter la migration (conteneur ou script local)
Placer healthcare_dataset.csv dans le dossier du projet.

Lancer le script Python :
python3 migrate.py
Le script insère tous les documents dans la collection patients de la base hopital.

## 8. Vérifier la base et la collection
### 8.1 Lister les bases de données
docker exec -it mongodb_local mongosh --eval "show dbs"

### 8.2 Sélectionner la base et lister les collections
docker exec -it mongodb_local mongosh --eval "db = db.getSiblingDB('hopital'); db.getCollectionNames()"

### 8.3 Compter le nombre de documents
docker exec -it mongodb_local mongosh --eval "db = db.getSiblingDB('hopital'); db.patients.countDocuments()"

### 8.4 Voir un exemple de document
docker exec -it mongodb_local mongosh --eval "db = db.getSiblingDB('hopital'); db.patients.findOne()"

## 9. Notes et bonnes pratiques
-> La base hopital et la collection patients sont créées automatiquement par MongoDB lors de l’insertion.

-> Utilisation des volumes Docker pour persistance des données et accès au CSV depuis les conteneurs.

-> Docker Compose facilite le déploiement multi-conteneurs et garantit que MongoDB est lancé avant le script de migration.

-> Toujours vérifier les logs pour détecter les erreurs de connexion ou d’insertion.