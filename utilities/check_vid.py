import os
import cv2
import os
import datetime
import mediapipe as mp
import csv


# open the file
file_name = "test/vid_0.mp4"
cap = cv2.VideoCapture(file_name)

# create a new csv file
csv_file_name = "test/vid_0.csv"
# apply mediapipe to the video and get all the positions of the body
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# get the number of frames in the video
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(num_frames)

# get the fps of the video
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

# get the duration of the video
duration = num_frames / fps
print(duration)

# get the width and height of the video
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# get the resolution of the video
resolution = (width, height)
print(resolution)

# get the codec of the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
print(fourcc)

# create a new video file
out = cv2.VideoWriter('output.mp4', fourcc, fps, resolution)


# run through frames of the video

pos = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 'right_eye', 'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 'mouth_right', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist',
       'right_wrist', 'left_pinky', 'right_pinky', 'left_index', 'right_index', 'left_thumb', 'right_thumb', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle', 'left_heel', 'right_heel', 'left_foot_index', 'right_foot_index']
fieldnames = ['t',]
for p in pos:
    fieldnames.append(p + "_x")
    fieldnames.append(p + "_y")
    fieldnames.append(p + "_z")
    fieldnames.append(p + "_v")

with open(csv_file_name, 'w', newline='') as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    t = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
            results = pose.process(frame)
            dict = {'t': t, }
            for i in range(len(pos)):
                # append to dict
                if results.pose_landmarks is not None:
                    dict.update({(pos[i] + '_x'): results.pose_landmarks.landmark[i].x, (pos[i] + '_y'): results.pose_landmarks.landmark[i].y,
                                (pos[i] + '_z'): results.pose_landmarks.landmark[i].z, (pos[i] + '_v'): results.pose_landmarks.landmark[i].visibility})
            print(dict)
            writer.writerow(dict)
            t += 1
    input("Press Enter to continue...")
