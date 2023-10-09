import numpy as np

import matplotlib.pyplot as gp


import os
import datetime
from datetime import datetime, timedelta
import calendar
import csv
import pandas as pd


def graph(x,y,day,ts):
    xy = gp.figure(figsize=(14, 6))
    xy = gp.bar(x,y,width=0.9)
    gp.ylim(0,5)
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
    
    gp.savefig('Wednesday.jpg')
    
    return

def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta
        
dts = [dt.strftime('%H:%M') for dt in 
    datetime_range(datetime(2016, 1, 1, 6), datetime(2016, 1, 1, 23), 
    timedelta(minutes=60))]

ts = '2022-07-13'
day = 'Wednesday'
intensity = [1,1,2,3,3,3,4,4,4,3,4,4,4,4,4,3,3]
graph(dts,intensity, day, ts)
print(dts)