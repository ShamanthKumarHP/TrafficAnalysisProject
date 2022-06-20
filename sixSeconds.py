import cv2
import numpy as np
import datetime
import csv
import time
import matplotlib.pyplot as plt

days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
def generateDay():    
    now = datetime.datetime.now()
    #day = now.strftime("%A")
    #date = now.strftime("%m/%d/%Y")
    day = days[2]
    date= '06/07/2022'
    return day,date

'''def csvToExcel(file1):
    df_new = pd.read_csv(file1)  
    GFG = pd.ExcelWriter('vehiclesCount.xlsx')
    df_new.to_excel(GFG, index = False)  
    GFG.save()
    print("csv to excel converted")
'''
    
def feedDataset(data):
    #header = ['Date', 'Time','Day','Intensity','Comment']
    with open(r'C:\Users\Shamanth kumar HP\Desktop\WebD\trafficAnalysis\dataSheetsCSV\Byappanahalli\camera1.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        #writer.writerow(header)    
        writer.writerows(data)       
        print("updated")

def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

nn1 = time.time()
min_contour_width=40  #40
min_contour_height=40  #40
offset=3      #10
line_height=200#550
matches =[]
cnt=0

cropTop = 50
cropBottom = 50
cropLeft = 50
cropRight = 50

intensity={ 1:"very low",2:"low", 3:"moderate", 4:"high", 5:"very high" }  
#cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('vehicles1.mp4')
cap = cv2.VideoCapture('videos/crop1.mp4')


#cap.set(3,1920)
#cap.set(4,1080)

if cap.isOpened():
    ret,frame0 = cap.read()
else:
    ret = False
ret,frame1 = cap.read()
ret,frame2 = cap.read()

frame1 = frame1[cropTop:, cropLeft: ]
frame2 = frame2[cropTop:, cropLeft: ]
#cv2.imwrite(r"C:\Users\Shamanth kumar HP\Desktop\WebD\testing\videos\\emptyRoad.jpg" , frame1)
#originalPic=cv2.imread('videos/emptyRoad.jpg') #frame1 if empty

originalPic = frame0[cropTop:, cropLeft: ]
len0,width0,_ = originalPic.shape

dimension = len0 * width0 #1280*720
#print(originalPic.shape)

day, date = generateDay()

fcount=1
val=1
totalList=[]
tempTraffic=[]
trafficSix=[]
feedList=[]
#tsec=1
startHour=6

def frameOperation(f1,f2):
    d = cv2.absdiff(f1,f2)    
    grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(9,9),0)
    ret , th = cv2.threshold(blur,25,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(th,np.ones((3,3)))
    return dilated

while ret:
    
    if fcount%30==0:
        t=0
        #print()
        #print(fcount,"-",val)
        if val<30:
            t=1
            #print("very low traffic")
        elif val <100:
            t=2
            #print("low traffic")
        elif val <200:
            t=3
        #print("moderate")
        elif val <224:
            t=4
        #print("high traffic")
        else:
            t=5
            #print("very high traffic")
        val=1
        tempTraffic.append(t)
        
    if fcount%180==0:
        #print(tsec,"-",tempTraffic)
        #trafficSix.append(max(tempTraffic))
        #print(max(tempTraffic))
        m = max(tempTraffic)
        feedList.append(date)
        feedList.append(startHour)
        feedList.append(day)
        feedList.append(m)
        intense = intensity.get(m)
        feedList.append(intense)
        
        totalList.append(feedList)
        
        tempTraffic=[]
        feedList=[]
        #tsec+=1
        startHour+=1
    
    numpyOnes=0
    t=False    
    
    dilated = frameOperation(frame1,frame2)
    #print(len(dilated[0]))
    #print(len(dilated))
    #print(dilated.ndim)   
    #print(dilated)    
    
        #print(len(i))
    #print(numpyOnes)
    #print(len(dilated))
    
    
    #plt.imshow(dilated, cmap = 'gray')
    #plt.title("frame:{0} density={1} val={2} ".format(str(fcount),str(dens),str(val)))
    #plt.show()
    
    
    
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
        #cv2.rectangle(frame1,(x-10,y-10),(x+w+10,y+h+10),(255,0,0),2)
        
        #cv2.line(frame1, (0, line_height), (500, line_height), (0,255,0), 2)
        centroid = get_centroid(x, y, w, h)
        matches.append(centroid)  
        #cv2.circle(frame1,centroid, 3, (0,255,0), -1)
        #cx,cy= get_centroid(x, y, w, h)
        
        
        for (x,y) in matches:            
            if y<(line_height+offset) and y>(line_height-offset) :            
                matches.remove((x,y))                
                cnt=cnt+1
                val=int(val/2)
                t=True
              
    if t==False:
        dilated0 = frameOperation(frame1, originalPic)
        
        
    
        for i in dilated0:
            numpyOnes+=np.count_nonzero(i!=0)
            
        dens = int((numpyOnes / dimension)*1000) ##402*388  
        #print("frame:",str(fcount)," -density= ",dens,"-",val)
        if dens>750 or dens<50:
            pass #error in frame or very low density
        elif dens>=400: #very high
            val=val+8
        elif dens>=200: #high
            val=val+4
        elif dens>=100: #moderate
            val=val+2
        elif dens>=50: #low
            val=val+1
        else:
            pass
        plt.imshow(dilated0, cmap = 'gray')
        plt.title("frame:{0} density={1} val={2} ".format(str(fcount),str(dens),str(val)))
        plt.show()
         
    #cv2.putText(frame1, "Vehicles passed:" + str(cnt), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 170, 0), 2)
    #cv2.drawContours(frame1,contours,-1,(0,0,255),2)

    #cv2.imshow("Original" , frame1)
    #cv2.imshow("Difference" , dilated)
    
    if cv2.waitKey(1) == 13:
        break
    frame1 = frame2
    ret , frame2 = cap.read()
    
    if ret!=False:
        frame2 = frame2[cropTop:, cropLeft: ]
        fcount+=1
    #print(fcount)
        
    #time.sleep(1)
    
print("total",cnt)   

print(totalList)
#csv    
feedDataset(totalList) 

#csvToExcel('vehiclesCount.csv')   
   
cv2.destroyAllWindows()
cap.release()
nn12 = time.time()
print(nn12-nn1)
