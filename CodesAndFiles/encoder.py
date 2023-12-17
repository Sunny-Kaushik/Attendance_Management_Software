import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databaseURL':"https://faceattendancerealtime-df07b-default-rtdb.firebaseio.com/",
                                   'storageBucket':"faceattendancerealtime-df07b.appspot.com" })


#importing the student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
#the storage is not real time
#this will send the data to the storage, create a folder named images and then put all the images
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)



#creating encodings for each image
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        #openCV library uses RGB color pattern but the face_recognition library uses BGR hence converting
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #here we are extracting the number associated with each of the image
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
#find the image and it will store heree
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

#here creating a file to dump all the encodings created
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")