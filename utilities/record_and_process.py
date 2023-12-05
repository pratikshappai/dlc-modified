import os
import cv2
import datetime
import mediapipe as mp
import csv
import numpy as np

script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)
now = datetime.datetime.now()
date_folder = now.strftime("%Y-%m-%d")
camera1_folder = "body_tracking/camera_1"
camera2_folder = "body_tracking/camera_2"

os.makedirs(date_folder, exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, "raw"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, "processed"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, "csv"), exist_ok=True)

os.makedirs(os.path.join(date_folder, camera2_folder, "raw"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera2_folder, "processed"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera2_folder, "csv"), exist_ok=True)

file_count = len([name for name in os.listdir(os.path.join(date_folder, camera1_folder, "raw")) if os.path.isfile(os.path.join(os.path.join(date_folder, camera1_folder, "raw"), name))])
print("number of vids already recorded = " + str(file_count))

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps1 = cap1.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

width1, height1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
width2, height2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

video_writer1 = cv2.VideoWriter(os.path.join(date_folder, camera1_folder, "raw", f"vid_{file_count}.mp4"), fourcc, fps1, (width1, height1))
video_writer2 = cv2.VideoWriter(os.path.join(date_folder, camera2_folder, "raw", f"vid_{file_count}.mp4"), fourcc, fps2, (width2, height2))

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

pos = ["nose", "left_eye_inner", "left_eye", "left_eye_outer", "right_eye_inner", "right_eye", "right_eye_outer", "left_ear", "right_ear", "mouth_left", "mouth_right", "left_shoulder", "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_pinky", "right_pinky", "left_index", "right_index", "left_thumb", "right_thumb", "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle", "left_heel", "right_heel", "left_foot_index", "right_foot_index"]

fieldnames = ["t"]
for p in pos:
    fieldnames.extend([f"{p}_x", f"{p}_y", f"{p}_z", f"{p}_v"])

csv_file_path1 = os.path.join(date_folder, camera1_folder, "csv", f"vid_{file_count}.csv")
csv_file_path2 = os.path


# Create the CSV file for camera 1
csv_file_path1 = os.path.join(
    date_folder, camera1_folder, "csv", f"vid_{file_count}.csv"
)
with open(csv_file_path1, mode="w") as csv_file:
    writer1 = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer1.writeheader()

# Create the CSV file for camera 2
csv_file_path2 = os.path.join(
    date_folder, camera2_folder, "csv", f"vid_{file_count}.csv"
)
with open(csv_file_path2, mode="w") as csv_file:
    writer2 = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer2.writeheader()

writer1 = csv.DictWriter(open(csv_file_path1, mode="a"), fieldnames=fieldnames)
writer2 = csv.DictWriter(open(csv_file_path2, mode="a"), fieldnames=fieldnames)
count = 0
t = 0

while True:
    # Read the frames from the cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        if count != 50:
            print("ret1 ret2", ret1, ret2)
            print("the number of frames captured is {}".format(count))
            print("Video ended unexpectedly")
        break

    # Write the frames to the video files
    rotated_frame1 = cv2.rotate(frame1, cv2.ROTATE_90_CLOCKWISE)
    rotated_frame2 = cv2.rotate(frame2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    video_writer1.write(rotated_frame1)
    video_writer2.write(rotated_frame2)

    # Process camera 1 using Mediapipe
    image1 = cv2.cvtColor(rotated_frame1, cv2.COLOR_BGR2RGB)
    results1 = pose.process(image1)

    image2 = cv2.cvtColor(rotated_frame2, cv2.COLOR_BGR2RGB)
    results2 = pose.process(image2)

    # Display the frames
    frame1_resized = cv2.resize(rotated_frame1, (int(height1/2), int(width1/2)))
    frame2_resized = cv2.resize(rotated_frame2, (int(height2/2), int(width2/2)))

    # # Create a blank image to hold the composite image - place it in the top left corner
    # composite = np.zeros((width1+width2, height1+height2, 3), dtype=np.uint8)
    # composite[0:width1, 0:height1] = rotated_frame1
    # composite[0:width2, height1:height1+height2] = rotated_frame2
    # cv2.imshow('Composite Image', composite)

    # Display the frames
    cv2.imshow("Camera 1", frame1)
    cv2.imshow("Camera 2", frame2)


    # Wait for the ESC key to be pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the resources
cap1.release()
cap2.release()


video_writer1.release()
video_writer2.release()
cv2.destroyAllWindows()
