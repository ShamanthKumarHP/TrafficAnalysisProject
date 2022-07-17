import cv2
import matplotlib.pyplot as plt
pic1 = cv2.imread(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\shamanth\emptyRoad.jpg')
img1 = cv2.normalize(pic1,None, alpha=0,beta=1000, norm_type=cv2.NORM_MINMAX)

pic2 = cv2.imread(r'C:\Users\Shamanth kumar HP\Desktop\WebD\FinalYearProject\shamanth\emptyRoad5.jpg')
img2 = cv2.normalize(pic2,None, alpha=0,beta=1000, norm_type=cv2.NORM_MINMAX)

d = cv2.absdiff(img1,img2)    
grey = cv2.cvtColor(d,cv2.COLOR_BGR2GRAY)


plt.imshow(grey, cmap = 'gray')
plt.title("Original")
plt.show()
#cv2.imshow("Ori", originalPic)