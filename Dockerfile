# Utiliser l'image Python 3.10-slim comme base
FROM python:3.10-slim

# Mettre à jour les paquets et installer cmake
RUN apt-get update && apt-get install -y cmake

# Définir le répertoire de travail
WORKDIR /app

# Copier le contenu du répertoire local dans le répertoire de travail
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port (si nécessaire)
EXPOSE 5000

# Commande pour démarrer l'application (ajuste en fonction de ton application)
CMD ["python", "app.py"]
