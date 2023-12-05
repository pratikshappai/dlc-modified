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
    for cam, folders in {'body_tracking/camera_1': ['raw'], 'body_tracking/camera_2': ['raw']}.items():
        for folder in folders:
            raw_path = os.path.join(date_folder, cam, folder)
            os.makedirs(raw_path, exist_ok=True)
            index = get_folder_count(raw_path)
            os.makedirs(os.path.join(raw_path, str(index)), exist_ok=True)

def create_video_writer(date_folder, cam_folder, index, fourcc, frame_rate, resolution):
    file_count = get_file_count(os.path.join(date_folder, cam_folder, "raw"))
    os.makedirs(os.path.join(date_folder, cam_folder, "raw", str(index)), exist_ok=True)

    return cv2.VideoWriter(os.path.join(date_folder, cam_folder, "raw", f"vid_{file_count}.mp4"), fourcc, frame_rate, resolution)

def acquire_images(cam_index, date_folder, fourcc, frame_rate, video_writers, barrier):
    print(f"Starting camera {cam_index+1}")
    camera = cameras.create_camera_by_index(cam_index)
    camera.init_cam()
    try:
        frame_rate = camera.camera_nodes.AcquisitionFrameRate.get_node_value()
    except Exception:
        frame_rate = 30


    print('current frame rate: ', frame_rate)
    resolution = (camera.camera_nodes.Height.get_node_value(), camera.camera_nodes.Width.get_node_value())
    resolution_T = (resolution[1], resolution[0])

    cam_folder = f"body_tracking/camera_{cam_index+1}"
    index = get_folder_count(os.path.join(date_folder, cam_folder))
    # video_writer = create_video_writer(date_folder, f"body_tracking/camera_{cam_index+1}", fourcc, frame_rate, resolution_T)
    # video_writer = create_video_writer(date_folder, cam_folder, index, fourcc, frame_rate, resolution_T)


    try:
        camera.begin_acquisition()
    except Exception:
        pass

    count = 10
    image_count = 0

    total_time = 0
    total_start = time.time()
    while count:
        barrier.wait()
        count -= 1
        start = time.time()
        try:
            image = camera.get_next_image()
            frame = np.array(image.get_image_data()).reshape(resolution)
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image.release()
        except Exception:
            continue

        try:
            # cv2.imwrite(f"{date_folder}/body_tracking/camera_{cam_index+1}/raw/frame_{image_count}_{cam_index+1}.png", frame)
            cv2.imwrite(f"{date_folder}/body_tracking/camera_{cam_index+1}/raw/{index}/frame_{image_count}_{cam_index+1}.png", frame)


            image_count += 1
        except Exception:
            break

        # try:
        #     video_writer.write(frame)
        # except Exception:
        #     break

        stop = time.time()
        print(f"Camera {cam_index+1} - time taken: {(stop-start)}, fps: {1/(stop-start)}")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    try:
        camera.end_acquisition()
        camera.deinit_cam()
        camera.release()
    except Exception:
        pass
    
    total_stop = time.time()
    print(f"Camera {cam_index+1} - total time taken: {(total_stop-total_start)}, fps: {1/(total_stop-total_start)}")
    # video_writer.release()

if __name__ == "__main__":
    date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    init_structure(date_folder)

    system = SpinSystem()
    cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    frame_rate_1 = 120.0  # Assuming both cameras have the same frame rate
    
    video_writers = {}  # Empty dict, individual threads will handle their own video writers

    barrier = threading.Barrier(2)
    thread1 = threading.Thread(target=acquire_images, args=(0, date_folder, fourcc, frame_rate_1, video_writers, barrier))
    thread2 = threading.Thread(target=acquire_images, args=(1, date_folder, fourcc, frame_rate_1, video_writers, barrier))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    cv2.destroyAllWindows()
