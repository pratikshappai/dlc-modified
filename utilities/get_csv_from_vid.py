import csv
import glob
import opencv

video_data = '2023-04-13/body_tracking/processed/vid_0.mp4'

csv_file_name = "output.csv"  # Replace with your desired file name

with open(csv_file_name, mode='w') as csv_file:
    fieldnames = ['x', 'y', 'z']  # Replace with your desired field names
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header

    # go through each frame in the video_data


    for frame_data in video_data:
        x = frame_data['x']  # Replace with the actual key for x coordinate in your data
        y = frame_data['y']  # Replace with the actual key for y coordinate in your data
        z = frame_data['z']  # Replace with the actual key for z coordinate in your data
        writer.writerow({'x': x, 'y': y, 'z': z})