import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime
from datetime import date

path = "E:\ImagesAttendance"
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
  encodeList = []
  for img in images:
     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
     encode = face_recognition.face_encodings(img)[0]  
     encodeList.append(encode)
  return encodeList

global nameList
#ATTENDANCE BLOCK///////////////////////////////////
def markAttendance(name):
  with open('Attendanceclg.csv','r+') as f:
     myDataList = f.readlines()
     global nameList
     nameList = []
     for line in myDataList: 
       entry = line.split('-')
       ent= entry[0]
       entry2 = ent.split(',')
       global ct
       ct=entry2[0]+","+entry[2]  #entry2 contain date
       nameList.append(ct) 
     today= date.today()
     string=str(today)
     s1=string[8:10]
     name2=name+","+s1+'\n'
     global sh
     if name2 not in nameList: 
       sh = True
       time.sleep(4)
       now = datetime.now()
       dtString = now.strftime('%H:%M:%S')
       print(today)
       today= date.today()
       string1=str(today)
       f.writelines(f'{name},{dtString},{string1}\n')
       print ("Attendance has been Submitted sucessfully")
       return(True)
     else :
       sh = False
       print ("ERROR! (Today Attendance submitted)")
       return(False) 


  #PECENTAGE BLOCK////////////////////
def Attendanceper(name):
    datelist=[]
    namelist=[]
    for line in nameList:
      split=line.split('\n')
      split1=split[0]
      split2=split1.split(',')
      split3=split2[1]
      splitn=split2[0]
      namelist.append(splitn)
      datelist.append(split3)
    z=len(datelist)-1
    v=int(datelist[z])-int(datelist[0])+1
    x=name
    def countX(namelist,x):
        return namelist.count(x)
    m=countX(namelist,x)
    print(m)
    print(v)
    global Per
    per = float(m/v)*100
    return per
   
encodeListKnown = findEncodings(images)
print('Encoding Complete')
camera = "http://10.153.193.186:8080/video"
#camera = "http://192.168.166.137:8080/video"
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS,30)
cap.open(camera)
#print("check==",cap.isOpened())
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter("E:\\ouyput.avi",fourcc,20.0,(640,480))

while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
     
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
     
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
     matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
     faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
     print(faceDis)
     matchIndex = np.argmin(faceDis)
    
    
     if matches[matchIndex]:
          name = classNames[matchIndex].upper()
          y1,x2,y2,x1 = faceLoc
          y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
          cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
          cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
          cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
          date_data = "Date: "+str(datetime.now())
          cv2.putText(img,date_data,(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),1,cv2.LINE_AA)
          cv2.putText(img,"SMART ATTENDANCE WINDOW",(140,460),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1,cv2.LINE_AA)
          cv2.putText(img,"STATUS:-",(20,80),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1,cv2.LINE_AA)
          cv2.putText(img,"TOTAL ATTENDANCE:-",(20,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,0),1,cv2.LINE_AA)
          markAttendance(name)
          Attendanceper(name)
          num = Attendanceper(name)
          act=str(num)+"%"
          cv2.putText(img,act,(300,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(255,0,0),1,cv2.LINE_AA)
          if sh :
            cv2.putText(img,"Attendance Submitted...",(150,80),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(37,120,5),1,cv2.LINE_AA)
            
          else :
            cv2.putText(img,"Attendance already submitted...",(150,80),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,0,255),1,cv2.LINE_AA) 
            
          print(name)
          
     else:
          y1,x2,y2,x1 = faceLoc
          y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
          cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
          cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
          cv2.putText(img,"NOTmatch",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    img=cv2.copyMakeBorder(img,5,5,5,5,cv2.BORDER_CONSTANT,value=[196,29,29])      
    cv2.imshow('Webcam',img)
    if cv2.waitKey(25)==27:
         break
        
cap.release()   
cv2.destroyAllWindows() 