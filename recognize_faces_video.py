from os import write
import face_recognition
import pickle
import cv2
import time
import imutils
import datetime 

print("[INFO] loading encodings...")    
data = pickle.load(open("encodings.pickle","rb"))     
tenfile=0
print("[INFO] starting video stream...")
writer = None
frame_rate = 10
prev = 0
while True:
    print("Ready!...")
    print(3)
    time.sleep(1)
    print(2)
    time.sleep(1)
    print(1)
    time.sleep(1)
    video = cv2.VideoCapture(0)    
    time_elapsed = time.time() - prev
    ret, frame = video.read()
    video.release()

    print("Taken success!...")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb = imutils.resize(rgb, width=750)
    r = frame.shape[1] / float(rgb.shape[1])


    print("Recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model="cnn")
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"   

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]

            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]     
                counts[name] = counts.get(name, 0) + 1  
            name = max(counts, key=counts.get)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        """ Do đang làm việc với rgb đã resize rồi nên cần rescale về ảnh gốc (frame), nhớ chuyển về int """
        top = int(top * r)
        right = int(right * r)
        bottom = int(bottom * r)
        left = int(left * r)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15

        cv2.putText(frame, str(name), (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1)
        print(name)
        tenfile+=1
    cv2.imwrite("inputImage/"+str(datetime.datetime.now().strftime("%m_%d_%Y %H_%M_%S"))+ ".jpg", img=frame)
                            

cv2.destroyAllWindows() 

