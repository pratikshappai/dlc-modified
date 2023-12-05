# get all csvs from 2023*/body_tracking/csv folder name then as the folder name

import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib import style
import datetime
import csv

# get all csvs from 2023*/body_tracking/csv folder name then as the folder name

# folders = glob.glob("2023*/body_tracking/csv")
# print(folders)


folder = "2023-04-13/body_tracking/csv"

# get all csvs from folder
all_csvs = glob.glob(folder + "/*.csv")
print(all_csvs)
for vid_csv in all_csvs:
    print("for loop {}".format(vid_csv))

    df = pd.read_csv(vid_csv)

    x = df['X'].tolist()
    y = df['Y'].tolist()
    z = df['Z'].tolist()
    
    size = len(x)
    print(size)

    t = np.arange(0, size, 1)

    # plot for x y z as a function of time

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
    plt.clf()

    plt.plot(t, x, label="x")
    plt.grid()
    plt.legend()
    plt.show()
    plt.clf()
    
    plt.plot(t, y, label="y")
    plt.grid()
    plt.legend()
    plt.show()
    plt.clf()

    plt.plot(t, z, label="z")
    plt.grid()
    plt.legend()
    plt.show()
    plt.clf()





