""" Để lưu encodings và tên của các faces trong dataset vào file encodings.pickle"""
# USAGE
# python encode_faces.py --dataset dataset --encodings encodings.pickle

from imutils import paths
import pickle
import cv2
import face_recognition
import sqlite3

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("dataSet"))

knownEncodings = []
knownNames = []

# duyệt qua các image paths
for (i, imagePath) in enumerate(imagePaths):
    name = getProfile(imagePath.split(".")[1])
    print(name)
    print(imagePath)

    image = cv2.imread(imagePath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    boxes = face_recognition.face_locations(rgb, model="cnn")    

    encodings = face_recognition.face_encodings(rgb, boxes)  

    for encoding in encodings:
        knownEncodings.append(encoding)
        knownNames.append(name)
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}

with open("encodings.pickle", "wb") as f:
    f.write(pickle.dumps(data))


    







