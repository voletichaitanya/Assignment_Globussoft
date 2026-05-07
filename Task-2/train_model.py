import cv2

# load haarcascade model
face_model = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

print("Model loaded successfully")