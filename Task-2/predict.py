import cv2
import numpy as np


face_model = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def get_face(image_path):

    img = cv2.imread(image_path)

    if img is None:
        return None, None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_model.detectMultiScale(
        gray,
        1.3,
        5
    )

    if len(faces) == 0:
        return None, None

    x, y, w, h = faces[0]

    face = gray[y:y+h, x:x+w]

    face = cv2.resize(face, (100, 100))

    return face, [int(x), int(y), int(w), int(h)]


def verify_faces(img1, img2):

    face1, box1 = get_face(img1)
    face2, box2 = get_face(img2)

    if face1 is None or face2 is None:
        return {
            "error": "Face not detected"
        }

    difference = np.mean(cv2.absdiff(face1, face2))

    similarity = 100 - difference

    result = (
        "same person"
        if similarity > 60
        else "different person"
    )

    return {
        "verification_result": result,
        "similarity_score": round(float(similarity), 2),
        "face1_bbox": box1,
        "face2_bbox": box2
    }