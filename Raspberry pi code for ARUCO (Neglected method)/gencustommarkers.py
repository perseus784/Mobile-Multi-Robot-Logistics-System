import numpy as np
import cv2
import cv2.aruco as ar

dict=ar.custom_dictionary(10,5)
print dict
img = ar.drawMarker(dict, 2, 700)
cv2.imwrite("gen_marker.jpg", img)

cv2.imshow('frame',img)
cv2.waitKey(0)
cv2.destroyAllWindows()