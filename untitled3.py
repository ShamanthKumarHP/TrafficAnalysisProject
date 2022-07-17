
#time complexity = 0.15*T average
from itertools import count
import cv2
import numpy as np
import datetime
from datetime import datetime, timedelta
import csv
import time
import calendar
import matplotlib.pyplot as plt
from collections import Counter

days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
intensity={ 1:"very low",2:"low", 3:"moderate", 4:"high", 5:"very high" }

def generateDay():    
    #now = datetime.datetime.now()
    #day = now.strftime("%A")
    #date = now.strftime("%m/%d/%Y")
    date='25-05-2022'
    d = datetime.strptime(date, '%d-%m-%Y').weekday()
    day = calendar.day_name[d]
    return day,date

def feedDataset(data):
    #header = ['Date', 'Time','Day','Intensity','Comment']
    #with open(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\csvFiles\URS_road\camera1.csv', 'w', encoding='UTF8', newline='') as f:
        #writer = csv.writer(f)
        #writer.writerow(header)    
        #writer.writerows(data)       
        print("updated")

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

def frameOperation(f1,f2, blurThresh, minThresh):
    d = cv2.absdiff(f1,f2)
        
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
    #plt.imshow(grey, cmap = 'gray')
    #plt.title("RGB to Gray")
    #plt.show()
    
    blur = cv2.GaussianBlur(grey,(5,5),0)
    #plt.imshow(blur, cmap = 'gray')
    #plt.title("Gaussian blur")
    #plt.show()
    
    ret , th = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    #plt.imshow(th, cmap = 'gray')
    #plt.title("Thresholding")
    #plt.show()
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  
    closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)  # Fill any small holes
    plt.imshow(closing, cmap = 'gray')
    plt.title("Closing")
    plt.show()
    
    return closing

nn1 = time.time()
min_contour_width=40  #40
min_contour_height=40  #40
offset=4      #10
line_height=195#550
matches =[]
cnt=0
FPS = 30
#day
cropTop = 50
cropBottom = 50
cropLeft = 50
cropRight = 50
'''
#night
cropTop = 500
cropBottom = 1080
cropLeft = 500
cropRight = 950
'''
#cap = cv2.VideoCapture(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\shamanth\pes.mp4')
cap = cv2.VideoCapture(r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\videos\crop1.mp4')

if cap.isOpened():
    ret,frame0 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame2 = cap.read()

frame1 = frame1[cropTop:, cropLeft: ]
frame2 = frame2[cropTop:, cropLeft: ]
#originalPic=cv2.imread(r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\videos\emptyRoad.jpg') #frame1 if empty
originalPic = frame0[cropTop:, cropLeft: ]
len0, width0, _ = originalPic.shape
print(originalPic.shape)
dimension = len0 * width0 #1280*720

day, date = generateDay()
fcount=1
temp=1
totalList=[]
oneMinList=[]
oneHourList = []
feedList=[]
startHour=6
p=0
while fcount<100:    
    if fcount%300 ==0:
        
        p= cnt-p
        print(fcount,"-",p)

    if fcount % FPS == 0:
        t=0
        if temp<22:
            t=1
            #print("very low traffic")
        elif temp <70:
            t=2
            #print("low traffic")
        elif temp <150:
            t=3
            #print("moderate")
        elif temp <176:
            t=4
            #print("high traffic")
        else:
            t=5
            #print("very high traffic")
        temp=1
        oneMinList.append(t)
        
    if fcount % (FPS*6) == 0:
        #s = max(oneMinList, key = oneMinList.count)
        h = Counter(oneMinList).most_common(1)[0][0]
        feedList.append(date)
        feedList.append(startHour)
        feedList.append(day)
        feedList.append(h)
        intense = intensity.get(h)
        feedList.append(intense)
        print(feedList)
        totalList.append(feedList)
        
        oneMinList = []
        feedList = []
        startHour+=1
    
    numpyOnes=0
    t=False    
    
    '''dilated = frameOperation(frame1, frame2, 13, 25)
    for i in dilated:
        numpyOnes+=np.count_nonzero(i!=0)
            
    dens = int((numpyOnes / dimension)*1000)
    #cv2.imshow("dilated",dilated)
    '''
    dens = 0
    '''
    
    contours,h = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        contour_tempid = (w >= min_contour_width) and (h >= min_contour_height)
        if not contour_tempid:
            continue
        #cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
        
        cv2.line(frame1, (0, line_height), (1000, line_height), (0,255,0), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)          
        
        for (x,y) in matches:            
            if y<(line_height+offset) and y>(line_height-offset) :            
                matches.remove((x,y))                
                cnt=cnt+1
                temp=int(temp/2)
                t=True
      '''        
    if t==False:
        dilated0 = frameOperation(frame1, originalPic,11, 35)
        #cv2.imshow("dil0" , dilated0)
        #dilated0 = frameOperation(frame1, originalPic,41, 35)
        for i in dilated0:
            numpyOnes+=np.count_nonzero(i!=0)
           
        dens0 = int((numpyOnes / dimension)*1000) ##402*388  
        #print("frame:",str(fcount)," -density= ",dens0,"-",temp)
        if dens0>720:
            pass #error in frame
        elif dens0<7 and dens==0:
            originalPic = np.array(frame1)
        elif dens0>=320: #very high
            temp=temp+8
        elif dens0>=160: #high
            temp=temp+4
        elif dens0>=80: #moderate
            temp=temp+2
        elif dens0>=40: #low
            temp=temp+1
        elif dens0>=7: #very low
            pass
       
        #print("d frame:{0} temp={1}  dens={2} ".format(str(fcount),str(temp),str(dens0)))
        #cv2.imshow("dil0" , dilated0)
    #cv2.imshow("dil" , dilated)      
    #cv2.imshow("ref", originalPic)
    cv2.putText(frame1, "Vehicles passed:" + str(cnt), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    cv2.imshow("Original" , frame1)
    
    if cv2.waitKey(1) == 13:
        break
    
    frame1 = frame2
    ret , frame2 = cap.read()
    
    if ret!=False:
        frame2 = frame2[cropTop:, cropLeft: ]
        fcount+=1
    #print(fcount)
        
    time.sleep(0.005)
#cv2.imwrite(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\shamanth\emptyRoad.jpg',originalPic)    
print("total vehicles passed: ",cnt)   
print("total frames count: ",fcount)

#csv 
if oneMinList != []:
    feedList.append(date)
    feedList.append(startHour)
    feedList.append(day)
    #h = max(oneHourList, key = oneHourList.count) #for last remaining minutes != 60
    h = Counter(oneMinList).most_common(1)[0][0]
    feedList.append(h)
    intense = intensity.get(h)
    feedList.append(intense)

    totalList.append(feedList)   
feedDataset(totalList) 
#print(totalList)
#csvToExcel('vehiclesCount.csv')   
   
cv2.destroyAllWindows()
cap.release()
nn12 = time.time()
print("total time taken: ",nn12-nn1)

