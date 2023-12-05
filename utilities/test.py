# testing python file
# write 1, 2, .... 100

# import csv
# import cv2



# TechVidvan Human pose estimator
# import necessary packages

import cv2
import mediapipe as mp
# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# create capture object
cap = cv2.VideoCapture('vid_74_rotated.mp4')
out = cv2.VideoWriter("output1.mp4", cv2.VideoWriter_fourcc(*'XVID'), 30, (1280, 720))
# filename = 'savedImage.jpg'
count = 0
while cap.isOpened():
    # read frame from capture object
    ret, frame = cap.read()
    count += 1

    if ret == True:
        # convert the frame to RGB format
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   
        # process the RGB frame to get the result
        results = pose.process(RGB)
        print(results.pose_landmarks)

        # draw detected skeleton on the frame
        mp_drawing.draw_landmarks(
            frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # show the final output
        cv2.imshow('Output', frame)
        out.write(frame)
        if cv2.waitKey(1) == ord('q'):
            break  
cap.release()
cv2.destroyAllWindows()


