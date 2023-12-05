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
    for cam, folders in {'body_tracking/camera_1': ['raw'], 'body_tracking/camera_2': ['raw']}.items():
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
    
    # Initialize camera 1
    camera_1 = cameras.create_camera_by_index(0)
    camera_1.init_cam()
    try:
        frame_rate_1 = camera_1.camera_nodes.AcquisitionFrameRate.get_node_value()
    except Exception:
        frame_rate_1 = 30
    resolution_1 = (camera_1.camera_nodes.Height.get_node_value(), camera_1.camera_nodes.Width.get_node_value())
    resolution_1_T = (resolution_1[1], resolution_1[0])

    # Initialize camera 2
    camera_2 = cameras.create_camera_by_index(1)
    camera_2.init_cam()
    try:
        frame_rate_2 = camera_2.camera_nodes.AcquisitionFrameRate.get_node_value()
    except Exception:
        frame_rate_2 = 30
    resolution_2 = (camera_2.camera_nodes.Height.get_node_value(), camera_2.camera_nodes.Width.get_node_value())
    resolution_2_T = (resolution_2[1], resolution_2[0])

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    
    video_writers = {
        1: create_video_writer(date_folder, "body_tracking/camera_1", fourcc, frame_rate_1, resolution_1_T),
        2: create_video_writer(date_folder, "body_tracking/camera_2", fourcc, frame_rate_2, resolution_2_T)
    }

    camera_1.begin_acquisition()
    camera_2.begin_acquisition()

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
            cv2.imwrite(f"{date_folder}/body_tracking/camera_1/raw/frame_{image_count}_1.png", frame_1)
            video_writers[1].write(frame_1)
            cv2.imshow("Camera 1", frame_1)
        except Exception:
            pass

        try:
            image_cam_2 = camera_2.get_next_image()
            frame_2 = np.array(image_cam_2.get_image_data()).reshape(resolution_2)
            frame_2 = cv2.rotate(frame_2, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_cam_2.release()
            cv2.imwrite(f"{date_folder}/body_tracking/camera_2/raw/frame_{image_count}_2.png", frame_2)
            video_writers[2].write(frame_2)
            cv2.imshow("Camera 2", frame_2)
        except Exception:
            pass

        image_count += 1

        stop = time.time()
        print(f"time taken: {(stop-start)}")
        print(f"fps: {1/(stop-start)}")
        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera_1.end_acquisition()
    camera_1.deinit_cam()
    camera_1.release()

    camera_2.end_acquisition()
    camera_2.deinit_cam()
    camera_2.release()

    video_writers[1].release()
    video_writers[2].release()

    cv2.destroyAllWindows()
