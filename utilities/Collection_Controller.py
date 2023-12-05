#Imports packages
import datetime
import os

#Stores the path of the data
path_data = "C:/Users/Data acquisition/Desktop/Data"

#Loads todays data folder 
def load_experiment_folder():
    
    #Get date
    date = datetime.datetime.now().strftime("%Y%m%d")

    #Checks if the data folder for today's date already exists, and creates it if it does not
    path_date_folder = os.path.join(path_data, date)
    if not os.path.isdir(path_date_folder):
        os.makedirs(path_date_folder)

    #Gets the current time
    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    #Creates the current experiment folder
    path_experiment_folder = os.path.join(path_date_folder, current_time)
    os.makedirs(path_experiment_folder)

    return path_experiment_folder

#Creates a new trial folder
def load_trial_folder(path):
    os.makedirs(path)


