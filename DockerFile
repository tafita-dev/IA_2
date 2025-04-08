# Utiliser une image de base Python
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 5000 pour l'application Flask
EXPOSE 5000

# Démarrer l'application Flask avec Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
