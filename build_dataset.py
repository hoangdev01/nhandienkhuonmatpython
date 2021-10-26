# USAGE
# python build_dataset.py --output dataset/huy
""" Xây dựng dataset bằng cách chụp webcam """
import argparse
import cv2 
import os
import sqlite3
# ap = argparse.ArgumentParser()
# ap.add_argument("-o", "--output", required=True, help="path to output directory")
# args = vars(ap.parse_args())

#insert/update data to sqlite
def insertOrUpdate(Id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID='"+str(Id)+"'"
    print(cmd)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name='"+str(Name)+"' WHERE ID='"+str(Id)+"'"
    else:
        cmd="INSERT INTO People(Id,Name) Values('"+str(Id)+"','"+str(Name)+"')"
    print(cmd)
    conn.execute(cmd)
    conn.commit()
    conn.close()

video = cv2.VideoCapture(0)
total = 0

id=input('enter your id: ')
name=input('enter your name: ')
insertOrUpdate(id,name)
sampleNum=0
while True:
    ret, frame = video.read()

    cv2.imshow("video", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("k"):
        cv2.imwrite("dataSet/User."+id +'.'+ str(sampleNum) + ".jpg", img=frame)
        # p = os.path.sep.join([args["output"], "{}.png".format(str(total).zfill(5))])    # điền thêm số 0 bên trái cho đủ 5 kí tự
        # cv2.imwrite(p, frame)
        sampleNum=sampleNum+1
        total += 1
	# nhấn q để thoát
    elif key == ord("q"):
	    break

print("[INFO] {} face images stored".format(total))
video.release()
cv2.destroyAllWindows()