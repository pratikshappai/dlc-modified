import os
import cv2
import os
import datetime
import mediapipe as mp
import csv
import numpy as np

script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

now = datetime.datetime.now()
date_folder = now.strftime("%Y-%m-%d")
test_folder = "testing_one_camera"
os.makedirs(date_folder, exist_ok=True)
os.makedirs(os.path.join(date_folder, test_folder), exist_ok=True)
check_num_files = os.path.join(date_folder, test_folder)
file_count = len(
    [
        name
        for name in os.listdir(check_num_files)
        if os.path.isfile(os.path.join(check_num_files, name))
    ]
)
print("number of vids already recorded = " + str(file_count))

cap0 = cv2.VideoCapture(2)  
# 0 - dart
# 1 - left camera
# 2 - right camera
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps0 = cap0.get(cv2.CAP_PROP_FPS)
print("fps0: ", fps0)


# Define the resolution of the video
width0 = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
height0 = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
resolution0 = (height0, width0)
def_frame_rate = 25

# Create the video writer objects
video_writer0 = cv2.VideoWriter(
    os.path.join(date_folder, test_folder, f"raw", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution0,
)

count = 0
t = 0

while True:
    ret0, frame0 = cap0.read()
    print('ret0 ',ret0)
    rotated_frame0 = frame0
    #cv2.rotate(frame0, cv2.ROTATE_90_CLOCKWISE)
    # video_writer0.write(rotated_frame0)
    cv2.imshow("Camera 0", rotated_frame0)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the resources
cap0.release()
video_writer0.release()
cv2.destroyAllWindows()