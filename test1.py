import cv2
import time

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv

cap = cv2.VideoCapture(0)
t=0
while(t<5):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    cv2.imshow('frame', rgb)
    out1 = cv2.imwrite('image/'+str(t)+'.jpg', frame)
    t+=1
    time.sleep(3)
    print (t)


cap.release()
cv2.destroyAllWindows()