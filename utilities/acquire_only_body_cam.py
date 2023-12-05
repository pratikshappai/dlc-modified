import os
import datetime
import cv2
import numpy as np
from rotpy.system import SpinSystem
from rotpy.camera import CameraList
import time

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

def init_structure(date_folder):
    for cam, folders in {'body_tracking/camera_1': ['raw']}.items():
        for folder in folders:
            os.makedirs(os.path.join(date_folder, cam, folder), exist_ok=True)

def create_video_writer(date_folder, cam_folder, fourcc, frame_rate, resolution):
    file_count = get_file_count(os.path.join(date_folder, cam_folder, "raw"))
    return cv2.VideoWriter(os.path.join(date_folder, cam_folder, "raw", f"vid_{file_count}.mp4"), fourcc, frame_rate, resolution)

if __name__ == "__main__":
    date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    init_structure(date_folder)

    system = SpinSystem()
    cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)
    camera_1 = cameras.create_camera_by_index(0)
    # camera_1.BinningHorizontal.set_node_value(2)
    # camera_1.BinningVertical.set_node_value(2)
    
    camera_1.init_cam()


    try:
        frame_rate_1 = camera_1.camera_nodes.AcquisitionFrameRate.get_node_value()
    except Exception:
        frame_rate_1 = 30

    print('current frame rate: ', frame_rate_1)

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # frame_rate_1 = 120.0

    resolution_1 = (camera_1.camera_nodes.Height.get_node_value(), camera_1.camera_nodes.Width.get_node_value())
    resolution_1_T = (resolution_1[1], resolution_1[0])

    video_writers = {
        1: create_video_writer(date_folder, "body_tracking/camera_1", fourcc, frame_rate_1, resolution_1_T),
    }

    try:
        camera_1.begin_acquisition()
    except Exception:
        pass

    count = 10
    image_count = 0

    while count:
        start = time.time()
        count -= 1
        
        try:
            image_cam_1 = camera_1.get_next_image()
            frame_1 = np.array(image_cam_1.get_image_data()).reshape(resolution_1)
            frame_1 = cv2.rotate(frame_1, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_cam_1.release()
        except Exception:
            continue

        try:
            cv2.imwrite(f"{date_folder}/body_tracking/camera_1/raw/frame_{image_count}_1.png", frame_1)
            image_count += 1
        except Exception:
            break

        try:
            video_writers[1].write(frame_1)
        except Exception:
            break

        try:
            cv2.imshow("Camera 1", frame_1)
        except Exception:
            break

        stop = time.time()
        print(f"time taken: {(stop-start)}")
        print(f"fps: {1/(stop-start)}")
        if cv2.waitKey(1) & 0xFF == 27:
            break

    try:
        camera_1.end_acquisition()
        camera_1.deinit_cam()
        camera_1.release()
    except Exception:
        pass

    video_writers[1].release()
    cv2.destroyAllWindows()
