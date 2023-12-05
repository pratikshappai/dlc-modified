import os
import cv2
import datetime
import numpy as np
from rotpy.system import SpinSystem
from rotpy.camera import CameraList

# Initialize SpinSystem and Camera
system = SpinSystem()
cameras = CameraList.create_from_system(system, update_cams=True, update_interfaces=True)
camera = cameras.create_camera_by_index(0)
camera.init_cam()
print(camera.camera_nodes.PixelFormat.is_writable())

try:
    camera.camera_nodes.PixelFormat.set_node_value_from_str('RGB8')
except Exception as e:
    print(f"Failed to set PixelFormat: {e}")

camera.begin_acquisition()

# Initialize directory for saving
now = datetime.datetime.now()
date_folder = now.strftime("%Y-%m-%d")
test_folder = "testing_one_camera"
os.makedirs(date_folder, exist_ok=True)
os.makedirs(os.path.join(date_folder, test_folder), exist_ok=True)

# Count existing files
check_num_files = os.path.join(date_folder, test_folder)
file_count = len([name for name in os.listdir(check_num_files) if os.path.isfile(os.path.join(check_num_files, name))])

fps = camera.camera_nodes.AcquisitionFrameRate.get_node_value()
fps = int(round(camera.camera_nodes.AcquisitionFrameRate.get_node_value()))
# setting fps explicitly
fps = 30
width = camera.camera_nodes.Width.get_node_value()
height = camera.camera_nodes.Height.get_node_value()
resolution = (width, height)

print("fps: ", fps)
print("resolution: ", resolution)

# Video Writing Setup
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video_writer = cv2.VideoWriter(
    os.path.join(date_folder, test_folder, f"raw", f"vid_{file_count}.mp4"),
    fourcc,
    fps,
    resolution,
)

# name of the video file
filename = os.path.join(date_folder, test_folder, f"raw", f"vid_{file_count}.mp4")
print("filename: ", filename)


# Acquisition Loop
while True:
    image_cam = camera.get_next_image(timeout=5)
    image = image_cam.deep_copy_image(image_cam)
    image_cam.release()
    
    # frame = np.array(image.get_image_data())  # Placeholder
    frame = np.array(image.get_image_data()).reshape(height, width)    
    cv2.imshow("Camera", frame)
    video_writer.write(frame)
    
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release resources
camera.end_acquisition()
camera.deinit_cam()
camera.release()
video_writer.release()
cv2.destroyAllWindows()
