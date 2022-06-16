from flask import Flask,request, url_for, redirect, render_template

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as gp


import os
import datetime
from datetime import datetime, timedelta
import calendar
import csv
import pandas as pd
app = Flask(__name__)
#model=pickle.load(open('Tmodel.pkl','rb'))

#days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
Maps=dict()
Maps={
    "URS":"https://www.google.com/maps/embed?pb=!1m26!1m12!1m3!1d3898.097907264606!2d76.64634986475333!3d12.309193132396771!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m11!3e0!4m5!1s0x3baf700df7b06beb%3A0x3ae264a585746609!2sD%20Devaraj%20Urs%20Rd%2C%20Subbarayanakere%2C%20Shivarampet%2C%20Mysuru%2C%20Karnataka%20570004!3m2!1d12.3087735!2d76.65268619999999!4m3!3m2!1d12.3095996!2d76.6443907!5e0!3m2!1sen!2sin!4v1651911525724!5m2!1sen!2sin",
    "MysRoad":"https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d7845.142029676378!2d76.89372222484934!3d12.529763354996428!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1s0x3bafa130360a345d%3A0x483b920029c1a7f5!2sGVC9%2BV96%20Mysour.benglor%20road%20kirgadnoor%20gate%2C%20Bannur%20-%20Mandya%20Rd%2C%20V%20V%20Nagar%2C%20Mandya%2C%20Karnataka%20571402!3m2!1d12.522154599999999!2d76.86840289999999!4m5!1s0x3bafa12c4d8d54af%3A0x2059712949feb66e!2zRmlyZSBTdGF0aW9uIE1BTkRZQSDgsqvgs4jgsrDgs40g4LK44LON4LKf4LOH4LK34LKo4LONIOCyruCyguCyoeCzjeCyrw!3m2!1d12.5364404!2d76.91458279999999!5e0!3m2!1sen!2sin!4v1652354777738!5m2!1sen!2sin"
          }

specialDays=dict()
specialDays={
    '2022-01-01':'New year',
    '2022-01-15':'Makar Sankranti',
    '2022-01-26':'Republic Day',
    '2022-03-01':'Maha Shivaratri',
    '2022-04-02':'Ugadi',
    '2022-08-08':'Muharram',
    '2022-08-15':'Independence Day',
    '2022-08-31':'Ganesh Chaturthi',
    '2022-09-25':'Mahalaya Amavasya',
    '2022-10-02':'Gandhi Jayanti',
    '2022-10-04':'Maha Navami',
    '2022-10-05':'Vijayadashami',
    '2022-10-09':'Maharshi Valmiki Jayanthi',
    '2022-10-24':'Naraka Chaturdashi',
    '2022-10-26':'Balipadyami / Deepavali',
    '2022-11-01':'Karnataka Rajyotsava',
    '2022-11-11':'Kanakadasa Jayanthi',
    '2022-12-25':'Chirstmas Day'
             }

csvFiles=dict()
csvFiles={
    "URS" : r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\dataSheetsCSV\Byappanahalli\camera1.csv',
    "Byyapanahalli" : r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\dataSheetsCSV\Byappanahalli\camera1.csv',
    "MysRoad": r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\dataSheetsCSV\Byappanahalli\camera1.csv'
    }

def removeImg():
    path=r'C:\Users\Shamanth kumar HP\Desktop\WebD\TrafficAnalysisProject\static\plot.jpg'
    os.remove(path)
    return

def findDay(date):
    d = datetime.strptime(date, '%Y-%m-%d').weekday()
    return (calendar.day_name[d])

def checkSpecialDay(localDate):
    if localDate in specialDays:
        return specialDays.get(localDate)
    
def graph(x,y,day,ts):
    xy = gp.figure(figsize=(14, 6))
    xy = gp.bar(x,y,width=0.9)
    gp.xlabel('Time-->',fontsize=16)
    gp.ylabel('Intensity-->',fontsize=16)
    i=0
    while i < len(y):
        if y[i]>4:
            xy[i].set_color('red')
        elif y[i]>3:
            xy[i].set_color('orange')
        elif y[i]>2:
            xy[i].set_color('gold')
        else:
            xy[i].set_color('yellow')
        i=i+1
    gp.title(day+" "+ts,fontsize=22)
    
    try:
        removeImg()
    except FileNotFoundError:
       pass
            
    gp.savefig('static\plot.jpg')
    gp.show()
    return

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
        
def getIntensity(day,csvpath):
    df = pd.read_csv(csvpath)
    df.drop(['Date','Comment'],axis=1,inplace=True)
    newdf = df.loc[df['Day']==day]
    gbc = newdf.groupby(['Time'])
    dd = pd.DataFrame(gbc.mean())
    intensity=[]
    intensity = dd['Intensity'].tolist()
    #print(intensity)
    return intensity

@app.route('/')
def hello_world():
    return render_template("firstPage.html")

@app.route('/Add',methods=['POST','GET'])
def Add():
    status = 0
    msg = ""
    int_features=[x for x in request.form.values()]
    print(int_features)
    road = int_features[0]
    dateVal = int_features[1] 
    if dateVal in specialDays:
        status = 1
    
    if status==1:
        holidayName = checkSpecialDay(dateVal)
        msg = "Traffic predictions may vary as it is " + holidayName
    else:
        msg = "Happy journey!"
    day  = findDay(dateVal)     
    route1 = Maps.get(road)
    csvPath = csvFiles.get(road)
    dts = [dt.strftime('%H:%M') for dt in 
    datetime_range(datetime(2016, 1, 1, 6), datetime(2016, 1, 1, 23), 
    timedelta(minutes=60))]
          
    intensityList=[]
    intensityList = getIntensity(day,csvPath)    
    graph(dts, intensityList, day, dateVal)
    
    return render_template('view.html',route1='{}'.format(route1),msg='{}'.format(msg))


if __name__ == '__main__':
    app.run(debug=False)


