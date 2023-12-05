import os
import cv2
import os
import datetime
import mediapipe as mp
import csv
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or '3' to suppress all logs including INFO


script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

# Create the directories
now = datetime.datetime.now()
date_folder = now.strftime("%Y-%m-%d")
camera0_folder = "dart_tracking"
camera1_folder = "body_tracking/camera_1"
camera2_folder = "body_tracking/camera_2"

check_num_files = os.path.join(date_folder, camera0_folder, f"raw")
file_count = len(
    [
        name
        for name in os.listdir(check_num_files)
        if os.path.isfile(os.path.join(check_num_files, name))
    ]
)
print("number of vids already recorded = " + str(file_count))

# create folder with camera 0, 1, 2
os.makedirs(date_folder, exist_ok=True)
os.makedirs(os.path.join(date_folder, camera0_folder), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera0_folder, f"raw"), exist_ok=True)

os.makedirs(os.path.join(date_folder, camera1_folder), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, f"raw"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, f"processed"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera1_folder, f"csv"), exist_ok=True)

os.makedirs(os.path.join(date_folder, camera2_folder), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera2_folder, f"raw"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera2_folder, f"processed"), exist_ok=True)
os.makedirs(os.path.join(date_folder, camera2_folder, f"csv"), exist_ok=True)

# count file that keeps track of the number of videos already taken for the day


# create a new video file for camera 1 and camera 2
cap0 = cv2.VideoCapture(2)  # mappings for dart is 2 
cap1 = cv2.VideoCapture(0)  # body_0 - the one looking at you from your left 
cap2 = cv2.VideoCapture(1)  # body_1 - the one looking at you from your right


# 0 - dart
# 1 - left camera
# 2 - right camera

# Define the video codecs and fps
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# fps = 60
fps0 = cap0.get(cv2.CAP_PROP_FPS)
# cap1.set(cv2.CAP_PROP_FPS, 60)
fps1 = cap1.get(cv2.CAP_PROP_FPS)
# cap2.set(cv2.CAP_PROP_FPS, 60)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

print("fps0: ", fps0)
print("fps1: ", fps1)
print("fps2: ", fps2)

# Define the resolution of the video
width0 = int(cap0.get(cv2.CAP_PROP_FRAME_WIDTH))
height0 = int(cap0.get(cv2.CAP_PROP_FRAME_HEIGHT))
resolution0 = (height0, width0)

width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
resolution1 = (height1, width1)

width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
resolution2 = (height2, width2)


print("height1 = {}, width1 = {}".format(height1, width1))
def_frame_rate = 25

# Create the video writer objects
video_writer0 = cv2.VideoWriter(
    os.path.join(date_folder, camera0_folder, f"raw", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution0,
)

video_writer1 = cv2.VideoWriter(
    os.path.join(date_folder, camera1_folder, f"raw", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution1,
)
video_writer1_processed = cv2.VideoWriter(
    os.path.join(date_folder, camera1_folder, f"processed", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution1,
)

video_writer2 = cv2.VideoWriter(
    os.path.join(date_folder, camera2_folder, f"raw", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution2,
)
video_writer2_processed = cv2.VideoWriter(
    os.path.join(date_folder, camera2_folder, f"processed", f"vid_{file_count}.mp4"),
    fourcc,
    def_frame_rate,
    resolution2,
)

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

"""
record video for camera 1 and camera 2
process video for camera 1 using mediapipe, dump the original video and the processed video into the folder
for camera 1 create a csv file with name of the video.
add header processing time, x, y, z, visibility
dump the coordinates of the body parts
process video for camera 2, dump the original video into the folder 
"""

pos = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
]
fieldnames = [
    "t",
]
for p in pos:
    fieldnames.append(p + "_x")
    fieldnames.append(p + "_y")
    fieldnames.append(p + "_z")
    fieldnames.append(p + "_v")


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
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    # # show the frames
    # print("ret0 ret1 ret2", ret0, ret1, ret2)
    # cv2.imshow("frame0", frame0)
    # cv2.imshow("frame1", frame1)
    # cv2.imshow("frame2", frame2)


    if not ret0 or not ret1 or not ret2:
        if count != 50:
            print("ret0 ret1 ret2", ret0, ret1, ret2)
            print("the number of frames captured is {}".format(count))
            print("Video ended unexpectedly")
        break

    # Write the frames to the video files
    rotated_frame0 = cv2.rotate(frame0, cv2.ROTATE_90_CLOCKWISE)
    rotated_frame1 = cv2.rotate(frame1, cv2.ROTATE_90_CLOCKWISE)
    rotated_frame2 = cv2.rotate(frame2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    video_writer0.write(rotated_frame0)
    video_writer1.write(rotated_frame1)
    video_writer2.write(rotated_frame2)

    # Process camera 1 using Mediapipe
    image1 = cv2.cvtColor(rotated_frame1, cv2.COLOR_BGR2RGB)
    results1 = pose.process(image1)

    image2 = cv2.cvtColor(rotated_frame2, cv2.COLOR_BGR2RGB)
    results2 = pose.process(image2)

    # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    if results1.pose_landmarks is not None:
        dict1 = dict(
            {
                "t": t,
            }
        )
        for i in range(len(pos)):
            dict1.update(
                {
                    (pos[i] + "_x"): results1.pose_landmarks.landmark[i].x,
                    (pos[i] + "_y"): results1.pose_landmarks.landmark[i].y,
                    (pos[i] + "_z"): results1.pose_landmarks.landmark[i].z,
                    (pos[i] + "_v"): results1.pose_landmarks.landmark[i].visibility,
                }
            )
        writer1.writerow(dict1)
        mp_drawing.draw_landmarks(
            rotated_frame1, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    if results2.pose_landmarks is not None:
        dict2 = dict(
            {
                "t": t,
            }
        )
        for i in range(len(pos)):
            dict2.update(
                {
                    (pos[i] + "_x"): results2.pose_landmarks.landmark[i].x,
                    (pos[i] + "_y"): results2.pose_landmarks.landmark[i].y,
                    (pos[i] + "_z"): results2.pose_landmarks.landmark[i].z,
                    (pos[i] + "_v"): results2.pose_landmarks.landmark[i].visibility,
                }
            )
        writer2.writerow(dict2)
        mp_drawing.draw_landmarks(
            rotated_frame2, results2.pose_landmarks, mp_pose.POSE_CONNECTIONS
        )

    t += 1
    video_writer1_processed.write(rotated_frame1)
    video_writer2_processed.write(rotated_frame2)

    # Display the frames
    frame0_resized = cv2.resize(rotated_frame0, (int(height0/2), int(width0/2)))
    frame1_resized = cv2.resize(rotated_frame1, (int(height1/2), int(width1/2)))
    frame2_resized = cv2.resize(rotated_frame2, (int(height2/2), int(width2/2)))

    # # # Create a blank image to hold the composite image - place it in the top left corner
    # composite = np.zeros((width1+width2, height1+height2, 3), dtype=np.uint8)
    # composite[0:width1, 0:height1] = rotated_frame1
    # composite[0:width2, height1:height1+height2] = rotated_frame2
    # composite[width1: width1+width2, 0:height1] = rotated_frame0
    # cv2.imshow('Composite Image', composite)


    cv2.imshow("frame0", frame0_resized)
    cv2.imshow("frame1", frame1_resized)
    cv2.imshow("frame2", frame2_resized)

    # Wait for the ESC key to be pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the resources
cap0.release()
cap1.release()
cap2.release()

video_writer0.release()
video_writer1.release()
video_writer1_processed.release()
video_writer2.release()
video_writer2_processed.release()

cv2.destroyAllWindows()
