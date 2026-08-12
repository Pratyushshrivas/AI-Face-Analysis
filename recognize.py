from deepface import DeepFace

result = DeepFace.find(
    img_path="face.jpg",
    db_path="database",
    enforce_detection=False
)

print(result)