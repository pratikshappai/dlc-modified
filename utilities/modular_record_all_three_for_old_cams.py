import os
import datetime
import csv
import cv2

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

def init_structure():
    for cam, folders in {'dart_tracking': ['raw'], 'body_tracking/camera_1': ['raw', 'processed', 'csv'],
                          'body_tracking/camera_2': ['raw', 'processed', 'csv']}.items():
        for folder in folders:
            os.makedirs(os.path.join(date_folder, cam, folder), exist_ok=True)

def init_csv(cam_folder, file_count):
    with open(os.path.join(date_folder, cam_folder, "csv", f"vid_{file_count}.csv"), 'w', newline='') as csv_file:
        fieldnames = ['t']
        csv.DictWriter(csv_file, fieldnames=fieldnames).writeheader()

def create_video_writer(cam_folder, sub_folder, fourcc, frame_rate, resolution):
    return cv2.VideoWriter(os.path.join(date_folder, cam_folder, sub_folder, f"vid_{file_count}.mp4"), fourcc, frame_rate, resolution)

if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    script_path = os.path.abspath(__file__)
    date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    camera0_folder, camera1_folder, camera2_folder = "dart_tracking", "body_tracking/camera_1", "body_tracking/camera_2"
    # os.makedirs(os.path.join(date_folder, camera0_folder, "raw"), exist_ok=True)

    init_structure()
    file_count = get_file_count(os.path.join(date_folder, camera0_folder, "raw"))
    
    print(f"number of vids already recorded = {file_count}")

    

    init_csv(camera1_folder, file_count)
    init_csv(camera2_folder, file_count)
    
    caps = {i: cv2.VideoCapture(i) for i in [0, 1, 2]}
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_rate = 25
    
    video_writers = {
        k: create_video_writer(cam_folder, sub_folder, fourcc, frame_rate, (int(caps[i].get(cv2.CAP_PROP_FRAME_HEIGHT)), int(caps[i].get(cv2.CAP_PROP_FRAME_WIDTH))))
        for i, (cam_folder, sub_folder) in enumerate([(camera0_folder, 'raw'), (camera1_folder, 'raw'), (camera2_folder, 'raw')])
        for k in range(3)
    }

    while True:
        ret, frames = zip(*[(cap.read()) for cap in caps.values()])
        if not all(ret):
            break
        
        for i, frame in enumerate(frames):
            video_writers[i].write(frame)
            cv2.imshow(f"Camera {i}", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    for cap in caps.values():
        cap.release()
    
    for writer in video_writers.values():
        writer.release()

    cv2.destroyAllWindows()
