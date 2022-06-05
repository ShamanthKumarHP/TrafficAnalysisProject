import cv2
import numpy as np
from datetime import datetime
import csv
import pandas as pd
import time
import random
import matplotlib.pyplot as plt

def generateDay():    
    now = datetime.datetime.now()
    day = now.strftime("%A")
    return day

def csvToExcel(file1):
    df_new = pd.read_csv(file1)  
    GFG = pd.ExcelWriter('vehiclesCount.xlsx')
    df_new.to_excel(GFG, index = False)  
    GFG.save()
    print("csv to excel converted")
    
def intensity(n):
    if n<2:
        return 1
    elif n<=4:
        return 2
    else:
        return 3
    
def feedDataset(data):
    header = ['Date', 'Time','Day', 'Count','Intensity']
    with open('vehiclesCount.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)    
        writer.writerows(data)       
        print("updated")
        
        
min_contour_width=40  #40
min_contour_height=40  #40
offset=3      #10
line_height=250#550
matches =[]
cnt=0
def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1
    return cx,cy
        
#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('vehicles1.mp4')
cap = cv2.VideoCapture('videos/crop1.mp4')


#cap.set(3,1920)
#cap.set(4,1080)

if cap.isOpened():
    ret,frame1 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame1 = cap.read()
tempList=[]
totalList=[]
atZero = datetime.now()
cd = atZero.strftime("%m/%d/%Y")
ct = atZero.strftime("%H:%M:%S")
rd=generateDay()
tempList.append(cd)
tempList.append(ct)
tempList.append(rd)
tempList.append(cnt)
i=intensity(cnt)
tempList.append(i)
totalList.append(tempList)
cars=0   
cc=0 
#cv2.imwrite(r"C:\Users\Shamanth kumar HP\Desktop\WebD\testing\videos\\emptyRoad.jpg" , frame1)
originalPic=cv2.imread('videos/emptyRoad.jpg')
fcount=1
val=1
tempCount=0
tempTraffic=[]
trafficSix=[]
tsec=1
while ret:
    CountUnchanged=1
    countChanged=cnt
    numpyOnes=0
    t=False
    #time.sleep(0.2)
    d = cv2.absdiff(frame1,originalPic)
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
    #cv2.imshow('ori',grey)
    #blur = cv2.GaussianBlur(grey,(5,5),0)
    blur = cv2.GaussianBlur(grey,(5,5),0)
    #ret , th = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    ret , th = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(th,np.ones((3,3)))
    #print(len(dilated[0]))
    #print(sum(sum(dilated)))
    #print(dilated.ndim)
    if fcount%30==0:
        t=0
        #print()
        #print(fcount,"-",val)
        if val<40:
            t=1
            #print("low traffic")
        elif val <150:
            t=2
            #print("moderate")
        else:
            t=3
            #print("high")
        val=1
        tempTraffic.append(t)
    if fcount%180==0:
        print()
        print(tsec,"-",tempTraffic)
        trafficSix.append(max(tempTraffic))
        print(max(tempTraffic))
        tempTraffic=[]
        tsec+=1
    for i in dilated:
        numpyOnes+=np.count_nonzero(i==0)
    #print(numpyOnes)
    dens = int((numpyOnes/921600)*1000)
    #print("frame:",str(fcount)," -density= ",int(dens*1000))
    #plt.imshow(dilated, cmap = 'gray')
    #plt.title("frame:{0} density={1} val={2} ".format(str(fcount),str(dens),str(val)))
    #plt.show()
    densityStatus=""
    if dens<130:
        densityStatus="High"
    elif dens>129 and dens<160:
        densityStatus="Light"
    else:
        densityStatus="Low"
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))

        # Fill any small holes
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
    contours,h = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for(i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        contour_valid = (w >= min_contour_width) and (h >= min_contour_height)
        #cv2.imshow('ori',frame1)
        if not contour_valid:
            continue
        cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
        
        cv2.line(frame1, (0, line_height), (500, line_height), (0,255,0), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)
        cv2.circle(frame1,centroid, 5, (0,255,0), -1)
        cx,cy= get_centroid(x, y, w, h)
        
        
        for (x,y) in matches:
            
            if y<(line_height+offset) and y>(line_height-offset) :
            
                matches.remove((x,y))
                
                n = datetime.now()
                cdd = n.strftime("%m/%d/%Y")
                ctt = n.strftime("%H:%M:%S")
                
                cnt=cnt+1
                val=val/2
                tempCount=cnt
                t=True
                if totalList[-1][1]==ctt:
                    cars=cars+1
                    continue
                temp=[]
                temp.append(cdd)
                temp.append(ctt)
                temp.append(rd)
                temp.append(cars)
                i=intensity(cars)
                temp.append(i)
                #print(cars)
                cc=cc+cars
                cars=1
                #time.sleep(0.5)
                #print(temp)
                totalList.append(temp)
    if t==False:        
        CountUnchanged+=1
        if densityStatus=="High":
            val=val+8
        elif densityStatus=="Light":
            val=val+2
    
    tempCount=cnt            
    cv2.putText(frame1, "Total Cars Detected: " + str(cnt), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    #cv2.drawContours(frame1,contours,-1,(0,0,255),2)

    cv2.imshow("Original" , frame1)
    #cv2.imshow("Difference" , th)
    if cv2.waitKey(1) == 13:
        break
    #frame1 = frame2
    ret , frame1 = cap.read()
    if ret==False:
        print(fcount)
    #time.sleep(1)
    fcount+=1
print("total",cnt)   
print(trafficSix)
#veh count in last second
temp=[]
nlast = datetime.now()
dlast = nlast.strftime("%m/%d/%Y")
tlast = nlast.strftime("%H:%M:%S")
rd=generateDay()
temp.append(dlast)
temp.append(tlast)
temp.append(rd)
temp.append(cnt-cc) 
i=intensity(cnt-cc)
temp.append(i) 
totalList.append(temp) 

print(totalList)
#csv    
feedDataset(totalList) 

csvToExcel('vehiclesCount.csv')   
   
cv2.destroyAllWindows()
cap.release()
