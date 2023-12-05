import csv
import matplotlib.pyplot as plt
import numpy as np


pos = ['nose', 'left_eye_inner', 'left_eye', 'left_eye_outer', 'right_eye_inner', 'right_eye', 'right_eye_outer', 'left_ear', 'right_ear', 'mouth_left', 'mouth_right', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky', 'left_index', 'right_index', 'left_thumb', 'right_thumb', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle', 'left_heel', 'right_heel', 'left_foot_index', 'right_foot_index']
csv_file_name = "test/vid_0.csv"
x = []
y = []
z = []

with open(csv_file_name, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['t'])
        for p in pos:
            if row[p + "_x"] != "":
                x.append(row[p + "_x"])
            if row[p + "_y"] != "":
                y.append(row[p + "_y"])
            if row[p + "_z"] != "":
                z.append(row[p + "_z"])
            # print(row[p + "_x"], row[p + "_y"], row[p + "_z"], row[p + "_v"])
        # print("\n")

# plot x y z


print("len x")
print(len(x))
print("len y")
print(len(y))
print("len z")
print(len(z))


t = range(len(x))

plt.plot(t, x, label='x')
plt.plot(t, y, label='y')
plt.plot(t, z, label='z')

plt.xlabel('time')
plt.ylabel('position')
plt.title('position over time')
plt.legend()
plt.show()
