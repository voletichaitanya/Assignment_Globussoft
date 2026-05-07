from fastapi import FastAPI, UploadFile, File
import shutil

from predict import verify_faces


app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Face Authentication API"
    }


@app.post("/verify")
async def verify(
    image1: UploadFile = File(...),
    image2: UploadFile = File(...)
):

    path1 = image1.filename
    path2 = image2.filename

    with open(path1, "wb") as buffer:
        shutil.copyfileobj(image1.file, buffer)

    with open(path2, "wb") as buffer:
        shutil.copyfileobj(image2.file, buffer)

    result = verify_faces(path1, path2)

    return result