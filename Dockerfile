# Utiliser une image Python slim
FROM python:3.10-slim



# Définir le répertoire de travail à /app
WORKDIR /app

# Copier les fichiers du projet dans l'image Docker
COPY . /app

# Installer pip et les dépendances Python
RUN pip install --upgrade pip


# Installer les autres dépendances Python
RUN pip install -r requirements.txt


# Lancer l'application
CMD ["python", "app.py"]
