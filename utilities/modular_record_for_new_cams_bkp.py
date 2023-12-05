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

    ''' 
    Needs testing, couple of issues with the below commands
    print(camera_1.camera_nodes.PixelFormat.is_writable())
    print('current pixel format: ', camera_1.camera_nodes.PixelFormat.get_node_value().get_enum_name())
    print(camera_1.camera_nodes.PixelFormat.get_entries_names())
    camera_1.camera_nodes.PixelFormat.set_node_value_from_str('BGR8')

    print(camera_2.camera_nodes.PixelFormat.is_writable())
    print('current pixel format: ', camera_2.camera_nodes.PixelFormat.get_node_value().get_enum_name())
    print(camera_2.camera_nodes.PixelFormat.get_entries_names())
    camera_2.camera_nodes.PixelFormat.set_node_value_from_str('BGR8')
    '''

    # Old-style camera 0
    cap_0 = cv2.VideoCapture(0)
    
    # Video writer configs
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    frame_rate = 30  # assuming all cameras are at 30 fps
    
    # Create video writers
    resolution_0 = (int(cap_0.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap_0.get(cv2.CAP_PROP_FRAME_WIDTH)))
    resolution_1 = (camera_1.camera_nodes.Height.get_node_value(), camera_1.camera_nodes.Width.get_node_value())
    resolution_2 = (camera_2.camera_nodes.Height.get_node_value(), camera_2.camera_nodes.Width.get_node_value())
    
    video_writers = {
        0: create_video_writer(date_folder, "dart_tracking", fourcc, frame_rate, resolution_0),
        1: create_video_writer(date_folder, "body_tracking/camera_1", fourcc, frame_rate, resolution_1),
        2: create_video_writer(date_folder, "body_tracking/camera_2", fourcc, frame_rate, resolution_2),
    }

    # Start acquisition
    try:
        camera_1.begin_acquisition()
        camera_2.begin_acquisition()
    except Exception as e:
        print(f"Failed to start acquisition: {e}")

    while True:
        ret_0, frame_0 = cap_0.read()
        image_cam_1 = camera_1.get_next_image(timeout=5)
        # frame_1 = np.array(image_cam_1.get_image_data(), dtype=np.uint8).reshape(resolution_1 + (3,))
        frame_1 = np.array(image_cam_1.get_image_data()).reshape(resolution_1)
        # frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_RGB2BGR)
        image_cam_1.release()

        image_cam_2 = camera_2.get_next_image(timeout=5)
        # frame_2 = np.array(image_cam_2.get_image_data(), dtype=np.uint8).reshape(resolution_2 + (3,))
        frame_2 = np.array(image_cam_2.get_image_data()).reshape(resolution_1)
        # frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_RGB2BGR)
        image_cam_2.release()
        
        if not ret_0:
            break

        video_writers[0].write(frame_0)
        video_writers[1].write(frame_1)
        video_writers[2].write(frame_2)

        cv2.imshow("Camera 0", frame_0)
        cv2.imshow("Camera 1", frame_1)
        cv2.imshow("Camera 2", frame_2)
        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap_0.release()
    camera_1.end_acquisition()
    camera_1.deinit_cam()
    camera_2.end_acquisition()
    camera_2.deinit_cam()
    
    for writer in video_writers.values():
        writer.release()

    cv2.destroyAllWindows()
