from deepface import DeepFace

import base64
from PIL import Image
import io
import numpy as np

def verifyFace(faces, face):
    face_image = np.array(Image.open(io.BytesIO(base64.b64decode(face))))

    for img in faces:
        decoded_data = base64.b64decode(img)

        # Convert to PIL Image
        image = Image.open(io.BytesIO(decoded_data))
        result = DeepFace.verify(
            img1_path = np.array(image),
            img2_path = face_image,
            model_name = "GhostFaceNet",
            )
        if result["verified"]:
            return result
    return result