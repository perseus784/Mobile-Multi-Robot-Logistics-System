import numpy as np
import cv2
import cv2.aruco as aruco
#import serial,time

cap = cv2.VideoCapture(0)
aru_size=132 #mm
focal_len=815.885212121
#arduino = serial.Serial('/dev/ttyACM1',115200,timeout=5)
#time.sleep(1)
while(True):
    flagfile=open('flag.txt','w+')
    flagfile.write('0')
    flagfile.close()
    # Capture frame-by-frame
    ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_50)
    #print aruco_dict
    parameters=aruco.DetectorParameters_create()

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)


    frame = aruco.drawDetectedMarkers(frame, corners)

    if len(corners):
        #print(corners)
        corners = corners[0][0]
        tl=corners[0]
        bl=corners[3]
        cv2.circle(frame,tuple(corners[0]),4,color=(255,0,0))
        cv2.circle(frame, tuple(corners[3]), 4, color=(0, 255, 0))
        #print tl,bl
        dist_px=np.linalg.norm(tl-bl)
        #print dist_px
        distance=(aru_size*focal_len)/dist_px
        print distance
        '''pixel/focal=actual/dist'''
        

        if distance<500:
            if ids==1 or 2 or 3 or 4:
                #arduino.flush()
                #arduino.write('4')
                flagfile=open('flag.txt','w+')
                flagfile.write('1')
                flagfile.close()
                print("found id no : {} \n in distance of : {}".format(ids,distance))
                #time.sleep(1)
                #arduino.write('1')
            cv2.putText(frame,str(ids),tuple(corners[2]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                
       
    #print(rejectedImgPoints)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()