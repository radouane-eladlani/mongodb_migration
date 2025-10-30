# On part de l'image  Python 3.9 slim (légère et adaptée aux conteneurs)
FROM python:3.9-slim

# On définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# On copie le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# On installe les dépendances Python nécessaires (pandas, pymongo, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# On copie tous les fichiers de notre projet dans le conteneur
COPY . .

# On définit la commande par défaut du conteneur : exécuter le script migrate.py
CMD ["python", "migrate.py"]
