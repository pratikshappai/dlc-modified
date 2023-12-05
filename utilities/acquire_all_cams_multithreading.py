import os
import datetime
import cv2
import numpy as np
from rotpy.system import SpinSystem
from rotpy.camera import CameraList
import time
import threading

def get_folder_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))])

def get_file_count(folder):
    return len([name for name in os.listdir(folder) if os.path.isfile(os.path.join(folder, name))])

def init_structure(date_folder):
    cams_structure = {
        'body_tracking/camera_1': ['raw'],
        'body_tracking/camera_2': ['raw'],
        'dart_tracking': ['raw']
    }
    for cam, folders in cams_structure.items():
        for folder in folders:
            raw_path = os.path.join(date_folder, cam, folder)
            os.makedirs(raw_path, exist_ok=True)
            index = get_folder_count(raw_path)
            os.makedirs(os.path.join(raw_path, str(index)), exist_ok=True)

def acquire_images_common(cam_index, date_folder, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    print(f"Starting body camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()

    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value())
    cam_folder = f"body_tracking/camera_{cam_index+1}"
    index = get_folder_count(os.path.join(date_folder, cam_folder, 'raw'))

    camera.begin_acquisition()

    start_time = time.time()
    while time.time() - start_time < acquire_time:
        # barrier.wait()
        image = camera.get_next_image()
        frame = np.array(image.get_image_data()).reshape(resolution)
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image.release()

        image_count = int((time.time() - start_time) * frame_rate)
        try:
            cv2.imshow(f"Camera {cam_index+1}", frame)
            cv2.imwrite(f"{date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png", frame)
            print(f"Saved image {date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png")
        except Exception:
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.end_acquisition()
    camera.deinit_cam()
    camera.release()

def acquire_dart_images(cam_index, date_folder, fourcc, frame_rate, barrier, cam_folder, acquire_time):
    print(f"Starting dart camera {cam_index+1}")
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    if not ret:
        print("Failed to open Dart camera.")
        return

    frame_rate = 30  # Dart camera
    resolution = frame.shape[:2]

    index = get_folder_count(os.path.join(date_folder, cam_folder, 'raw'))

    start_time = time.time()
    while time.time() - start_time < acquire_time:
        # barrier.wait()
        ret, frame = cap.read()
        if not ret:
            print("Failed to acquire image from Dart camera.")
            break
        
        image_count = int((time.time() - start_time) * frame_rate)
        try:
            cv2.imshow("Dart camera", frame)
            cv2.imwrite(f"{date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png", frame)
            print(f"Saved image {date_folder}/{cam_folder}/raw/{index}/frame_{image_count}_{cam_index+1}.png")
        except Exception:
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

if __name__ == "__main__":
    date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    init_structure(date_folder)

    system = SpinSystem()
    cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    frame_rate_1 = 120.0  # Body cameras
    acquire_time = 1.0  # Acquire for 1 seconds
    
    barrier = threading.Barrier(3)

    thread1 = threading.Thread(target=acquire_images_common, args=(0, date_folder, fourcc, frame_rate_1, barrier, 'body_tracking/camera_1', acquire_time))
    thread2 = threading.Thread(target=acquire_images_common, args=(1, date_folder, fourcc, frame_rate_1, barrier, 'body_tracking/camera_2', acquire_time))
    thread3 = threading.Thread(target=acquire_dart_images, args=(0, date_folder, fourcc, 30, barrier, 'dart_tracking', acquire_time))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    cv2.destroyAllWindows()
