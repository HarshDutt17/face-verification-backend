from deepface import DeepFace

import base64
from PIL import Image
import io
import numpy as np

def base64_to_numpy(base64_string):
    image_bytes = base64.b64decode(base64_string)

    image = Image.open(io.BytesIO(image_bytes))

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    numpy_array = np.array(image)

    return numpy_array

def verifyFace(faces, face):
    face_image = base64_to_numpy(face)

    for img in faces:    
        result = DeepFace.verify(
            img1_path = face_image,  # Assuming there's only one face detected
            img2_path = base64_to_numpy(img),  # Assuming verification against the same face
            model_name = "GhostFaceNet",
        )
        if result["verified"]:
            return result
    return result