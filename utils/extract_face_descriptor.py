# utils/extract_face_descriptor.py
import face_recognition


def extract_face_descriptor(image):
    # Détecter les visages dans l'image
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    if len(face_encodings) == 0:
        return None

    return face_encodings[0]  


