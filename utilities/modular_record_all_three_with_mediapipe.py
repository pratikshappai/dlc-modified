import os
import datetime
import csv
import cv2
import mediapipe as mp

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Initialization
script_path = os.path.abspath(__file__)
date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
camera0_folder, camera1_folder, camera2_folder = "dart_tracking", "body_tracking/camera_1", "body_tracking/camera_2"

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

file_count = get_file_count(os.path.join(date_folder, camera0_folder, "raw"))
print(f"number of vids already recorded = {file_count}")

# Pose landmarks
pos = [ ... ]  # Same as before

# Initialize directories and CSV
def init_structure():
    for cam, folders in {'dart_tracking': ['raw'], 'body_tracking/camera_1': ['raw', 'processed', 'csv'],
                          'body_tracking/camera_2': ['raw', 'processed', 'csv']}.items():
        for folder in folders:
            os.makedirs(os.path.join(date_folder, cam, folder), exist_ok=True)

init_structure()

def init_csv(cam_folder):
    with open(os.path.join(date_folder, cam_folder, "csv", f"vid_{file_count}.csv"), 'w', newline='') as csv_file:
        fieldnames = ['t'] + [f"{p}_{dim}" for p in pos for dim in ["x", "y", "z", "v"]]
        csv.DictWriter(csv_file, fieldnames=fieldnames).writeheader()

init_csv(camera1_folder)
init_csv(camera2_folder)

# Initialize video capture
caps = {i: cv2.VideoCapture(i) for i in [0, 1, 2]}
fps = {i: cap.get(cv2.CAP_PROP_FPS) for i, cap in caps.items()}

# Initialize video writers
def create_video_writer(cam_folder, sub_folder, fourcc, frame_rate, resolution):
    return cv2.VideoWriter(os.path.join(date_folder, cam_folder, sub_folder, f"vid_{file_count}.mp4"), fourcc, frame_rate, resolution)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
frame_rate = 25
video_writers = {
    k: create_video_writer(cam_folder, sub_folder, fourcc, frame_rate, (int(caps[i].get(cv2.CAP_PROP_FRAME_HEIGHT)), int(caps[i].get(cv2.CAP_PROP_FRAME_WIDTH))))
    for i, (cam_folder, sub_folder) in enumerate([(camera0_folder, 'raw'), (camera1_folder, 'raw'), (camera2_folder, 'raw')])
    for k in range(3)
}

# Initialize Mediapipe
pose = mp.solutions.pose.Pose()

# Main loop
count, t = 0, 0
csv_writers = {
    cam_folder: csv.DictWriter(open(os.path.join(date_folder, cam_folder, "csv", f"vid_{file_count}.csv"), 'a', newline=''),
                              fieldnames=['t'] + [f"{p}_{dim}" for p in pos for dim in ["x", "y", "z", "v"]])
    for cam_folder in [camera1_folder, camera2_folder]
}

while True:
    ret, frames = zip(*[(cap.read()) for cap in caps.values()])
    if not all(ret):
        break

    rotated_frames = [cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE) for ok, frame in zip(ret, frames) if ok]
    
    for i, (writer, frame) in enumerate(zip(video_writers.values(), rotated_frames)):
        writer.write(frame)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(img)
        
        if results.pose_landmarks:
            row = {"t": t}
            row.update({f"{p}_{dim}": getattr(results.pose_landmarks.landmark[i], dim) for i, p in enumerate(pos) for dim in ["x", "y", "z", "v"]})
            csv_writers[camera1_folder if i == 1 else camera2_folder].writerow(row)
            
    t += 1

for cap in caps.values():
    cap.release()

for writer in video_writers.values():
    writer.release()

cv2.destroyAllWindows()
