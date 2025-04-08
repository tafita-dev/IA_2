import base64
import cv2
import numpy as np
from flask import Flask, request, jsonify
from utils.extract_face_descriptor import extract_face_descriptor
from config import connect_to_database

client = connect_to_database()
if client:
    db = client["face_recognition_db"]
    collection = db["users"]
else:
    db = None
    collection = None


# Configuration Flask
app = Flask(__name__)


@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()

    name = data.get("name")
    age = data.get("age")
    image_data = data.get("image")

    if not name or not age or not image_data:
        return jsonify({"error": "All fields are required"}), 400

    # Convertir l'image en un tableau numpy
    try:
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Image decoding failed: {str(e)}"}), 400

    if img is None:
        return jsonify({"error": "Invalid image format"}), 400

    # Extraire le descripteur de visage
    face_descriptor = extract_face_descriptor(img)

    if face_descriptor is None:
        return jsonify({"error": "No face detected"}), 400

    # Enregistrer l'utilisateur dans MongoDB
    user = {
        "name": name,
        "age": age,
        "face_descriptor": face_descriptor.tolist() 
    }

    collection.insert_one(user)

    return jsonify({"message": "User created successfully"}), 201


@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    data = request.get_json()
    image_data = data.get("image")

    if not image_data:
        return jsonify({"error": "No image data provided"}), 400

    # Convertir l'image en un tableau numpy
    try:
        nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Image decoding failed: {str(e)}"}), 400

    if img is None:
        return jsonify({"error": "Invalid image format"}), 400

    # Extraire le descripteur de visage de l'image envoyée
    face_descriptor = extract_face_descriptor(img)

    if face_descriptor is None:
        return jsonify({"error": "No face detected"}), 400

    # Comparer avec les utilisateurs dans MongoDB
    all_users = collection.find()
    best_match = None
    best_similarity = float('inf')  # Utilisez un grand nombre au début

    for user in all_users:
        stored_descriptor = np.array(user["face_descriptor"])

        # Vérifier et ajuster les dimensions des descripteurs
        if face_descriptor.shape != stored_descriptor.shape:
            continue  # Ignore les descripteurs de formes incompatibles

        # Calcul de la similarité (on utilise ici la distance euclidienne)
        similarity = np.linalg.norm(face_descriptor - stored_descriptor)

        if similarity < best_similarity:
            best_similarity = similarity
            best_match = user

    if best_match and best_similarity < 0.6:  # Seuil de similarité
        return jsonify({
            "message": f"Face recognized: {best_match['name']}",
            "user_id": str(best_match["_id"]),
            "age": best_match["age"],
            "similarity": best_similarity
        }), 200

    return jsonify({"message": "Face not recognized"}), 404


if __name__ == '__main__':
    app.run(debug=True)
