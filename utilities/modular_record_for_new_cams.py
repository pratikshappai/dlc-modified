import os
import datetime
import csv
import cv2
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
    for cam, folders in {'dart_tracking': ['raw'], 'body_tracking/camera_1': ['raw'], 'body_tracking/camera_2': ['raw']}.items():
        for folder in folders:
            os.makedirs(os.path.join(date_folder, cam, folder), exist_ok=True)

def create_video_writer(date_folder, cam_folder, fourcc, frame_rate, resolution):
    file_count = get_file_count(os.path.join(date_folder, cam_folder, "raw"))
    return cv2.VideoWriter(os.path.join(date_folder, cam_folder, "raw", f"vid_{file_count}.mp4"), fourcc, frame_rate, resolution)

if __name__ == "__main__":
    date_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    init_structure(date_folder)
    
    # Initialize SpinSystem and Camera
    system = SpinSystem()
    cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)
    
    camera_1 = cameras.create_camera_by_index(0)
    camera_1.init_cam()
    camera_2 = cameras.create_camera_by_index(1)
    camera_2.init_cam()

    # Old-style camera 0
    cap_0 = cv2.VideoCapture(0)
    cap_0.set(cv2.CAP_PROP_FPS, 30)
    # ADDED: Check filesystem permissions
    if not os.access(date_folder, os.W_OK):
        raise PermissionError(f"No write permission to {date_folder}")

    # ADDED: Check frame rate from specialized cameras
    try:
        frame_rate_1 = camera_1.camera_nodes.AcquisitionFrameRate.get_node_value()
        frame_rate_2 = camera_2.camera_nodes.AcquisitionFrameRate.get_node_value()
    except Exception as e:
        print("Failed to get frame rate from specialized cameras:", e)
        frame_rate_1 = frame_rate_2 = 30  # fallback to default
    
    # Video writer configs
    fourcc = cv2.VideoWriter_fourcc(*"MJPG") # mp4v H264
    frame_rate = 30.0  # assuming all cameras are at 30 fps
    frame_rate_1 = 120.0
    frame_rate_2 = 120.0

    # print actual frame rate
    actual_frame_rate_0 = cap_0.get(cv2.CAP_PROP_FPS)
    print('actual_frame_rate_0: ', actual_frame_rate_0)
    actual_frame_rate_1 = camera_1.camera_nodes.AcquisitionFrameRate.get_node_value()
    print('actual_frame_rate_1: ', actual_frame_rate_1)
    actual_frame_rate_2 = camera_2.camera_nodes.AcquisitionFrameRate.get_node_value()
    print('actual_frame_rate_2: ', actual_frame_rate_2)
    
    # Create video writers
    resolution_0 = (int(cap_0.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap_0.get(cv2.CAP_PROP_FRAME_WIDTH)))
    resolution_1 = (camera_1.camera_nodes.Height.get_node_value(), camera_1.camera_nodes.Width.get_node_value())
    resolution_1_T = (resolution_1[1], resolution_1[0])
    resolution_2 = (camera_2.camera_nodes.Height.get_node_value(), camera_2.camera_nodes.Width.get_node_value())
    resolution_2_T = (resolution_2[1], resolution_2[0])

    video_writers = {
        0: create_video_writer(date_folder, "dart_tracking", fourcc, frame_rate, resolution_0),
        1: create_video_writer(date_folder, "body_tracking/camera_1", fourcc, frame_rate_1, resolution_1_T),
        2: create_video_writer(date_folder, "body_tracking/camera_2", fourcc, frame_rate_2, resolution_2_T),
    }

    # ADDED: Validate VideoWriter
    for idx, writer in video_writers.items():
        if not writer.isOpened():
            raise Exception(f"VideoWriter {idx} not opened")

    print('resolution set for video writers')
    print('resolution_0: ', resolution_0)
    print('resolution_1: ', resolution_1_T)
    print('resolution_2: ', resolution_2_T)
    
    # Start acquisition
    try:
        camera_1.begin_acquisition()
        camera_2.begin_acquisition()
    except Exception as e:
        print(f"Failed to start acquisition: {e}")

    count = 10
    image_count = 0

    while count:
        # time start
        start = time.time()
        count -= 1
        ret_0, frame_0 = cap_0.read()
        
        try:
            image_cam_1 = camera_1.get_next_image()
            frame_1 = np.array(image_cam_1.get_image_data()).reshape(resolution_1)
            frame_1 = cv2.rotate(frame_1, cv2.ROTATE_90_COUNTERCLOCKWISE)
            image_cam_1.release()
        except Exception as e1:
            print("Error with Camera 1:", e1)
            continue

        try:
            image_cam_2 = camera_2.get_next_image()
            frame_2 = np.array(image_cam_2.get_image_data()).reshape(resolution_2)
            frame_2 = cv2.rotate(frame_2, cv2.ROTATE_90_CLOCKWISE)
            image_cam_2.release()
        except Exception as e2:
            print("Error with Camera 2:", e2)
            continue

        if not ret_0:
            print("Error with Camera 0")
            break
        
        try:
            cv2.imwrite(f"{date_folder}/dart_tracking/raw/frame_{image_count}_0.png", frame_0)
            cv2.imwrite(f"{date_folder}/body_tracking/camera_1/raw/frame_{image_count}_1.png", frame_1)
            cv2.imwrite(f"{date_folder}/body_tracking/camera_2/raw/frame_{image_count}_2.png", frame_2)
            image_count += 1
        except Exception as e:
            print(f"Error saving image: {e}")
            break
        
        for idx, writer in video_writers.items():
            if not video_writers[idx].isOpened():
                raise Exception(f"VideoWriter {idx} not opened")


        try:
            # print("Writing to video for count = ", count)
            video_writers[0].write(frame_0)
            # video_writers[1].write(frame_1)
            # video_writers[2].write(frame_2)
        except Exception as e:
            print(f"Error writing to video: {e}")
            break

        try:
            pass
            cv2.imshow("Camera 0", frame_0)
            cv2.imshow("Camera 1", frame_1)
            cv2.imshow("Camera 2", frame_2)

            # show the frame size 
            # print('inside the while loop')
            # print("frame_0: ", frame_0.shape)
            # print("frame_1: ", frame_1.shape)
            # print("frame_2: ", frame_2.shape)

        except Exception as e:
            print(f"Error displaying frame: {e}")
            break
        stop = time.time()
        print('time taken for one loop: ', stop - start)
        print('fps: ', 1/(stop-start))
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release camera capture objects
    cap_0.release()
    try:
        camera_1.end_acquisition()
        camera_1.deinit_cam()
        camera_1.release()
    except Exception as e:
        print(f"Error cleaning up camera_1: {e}")

    try:
        camera_2.end_acquisition()
        camera_2.deinit_cam()
        camera_2.release()
    except Exception as e:
        print(f"Error cleaning up camera_2: {e}")

    # release video writers
    for writer in video_writers.values():
        try:
            writer.release()
        except Exception as e:
            print(f"Error releasing video writer: {e}")
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()
