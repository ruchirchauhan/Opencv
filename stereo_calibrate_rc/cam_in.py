#!/usr/bin/python
import numpy as np
import cv2
import sys

args = sys.argv
del args[0]

def capture(cam_l, cam_r):
    cap_l = cv2.VideoCapture(cam_l)
    cap_r = cv2.VideoCapture(cam_r)
    debug_dir = 'data/'
    capture_counter = 0

    while(True):

        #Capture frame-by-frame
        ret1, frame_l = cap_l.read()
        ret2, frame_r = cap_r.read()

        #Operations on the frame
        out_frame_l = cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY)
        out_frame_r = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)

        #Display the resulting frame
        cv2.imshow('Left camera', out_frame_l)
        cv2.imshow('Right camera', out_frame_r)

        key_press = cv2.waitKey(1)
        if key_press & 0xFF == ord('q'):
            break
        if key_press & 0xFF == ord('c'):
            capture_counter += 1
            print 'capture: ', capture_counter
            linfile = debug_dir + 'left0' + str(capture_counter) + '.jpg'
            rinfile = debug_dir + 'right0' + str(capture_counter) + '.jpg'
            cv2.imwrite(linfile, out_frame_l)
            cv2.imwrite(rinfile, out_frame_r)
            if capture_counter == 20:
                print '20 images captures. Enough for calibration, press q to stop taking images'

    #When everything done, release the capture
    cap_l.release()
    cap_r.release()
    cv2.destroyAllWindows()

###############
# Main
###############

# Take user input
if not args:
    print 'Please select a camera'
    exit(1)
cam_l = args[0]
cam_r = args[1]

#print 'User selected camera no: ', cam_no
capture(int(cam_l), int(cam_r))

exit(0)
