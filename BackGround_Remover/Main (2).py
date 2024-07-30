import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
segmentor = SelfiSegmentation()

listImg = os.listdir("Images")
imglist = []
for imgPath in listImg:
    img = cv2.imread(f'Images/{imgPath}')
    img = cv2.resize(img, (640, 480))  
    imglist.append(img)
print(len(imglist))

indexImg = 0

while True:
    success, img = cap.read()
    if not success:
        break

    imgOut = segmentor.removeBG(img, imglist[indexImg], cutThreshold=0.8)  # for images

    imgStacked = cvzone.stackImages([img, imgOut], 2, 1)
    cv2.imshow("image", imgStacked)
    key = cv2.waitKey(1)
    print(indexImg)
    if key == ord('a'):
        if indexImg > 0:
            indexImg -= 1
    elif key == ord('d'):
        if indexImg < len(imglist) - 1:
            indexImg += 1
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
