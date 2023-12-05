import cv2
import os

# Open the video file for reading
video_path = "2023-08-30\\body_tracking\\camera_1\\raw\\vid_12.mp4"

# check if video path is valid
if not os.path.exists(video_path):
    print("Error: Video file does not exist.")
    exit()


cap = cv2.VideoCapture(video_path)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Loop to read and display each frame of the video
while True:
    ret, frame = cap.read()

    # Break the loop if no frame was read
    if not ret:
        break

    # Display the frame
    cv2.imshow("Video", frame)

    # Exit the loop if the 'Esc' key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the video capture object and close the window
cap.release()
cv2.destroyAllWindows()
