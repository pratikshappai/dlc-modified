import tkinter as tk
import Collection_Controller as controller
import os

path_experiment = ""
trial_count = 0
path_current_trial = ""

def new_trial():
    #Creates the path for the new trial
    path_current_trial = os.path.join(path_experiment, trial_count)
    trial_count = trial_count + 1
    print("New trial started")

def end_trial():
    print("Trial ended")

def end_experiment():
    print("Experiment ended")
    experiment_window.destroy()
    root.deiconify()  # Unhide the main window

def start_experiment():
    part_ID = entry_part_ID.get()

    trial_count = 0

    #Creates the path for the info document
    path_info = os.path.join(path_experiment, "info.txt")

    # Open the file in write mode
    with open(path_info, "w") as file:
        # Write the content to the file
        file.write(part_ID)

    # Create a new window
    global experiment_window
    experiment_window = tk.Toplevel(root)
    experiment_window.geometry("800x600")

    # Create "New Trial" button
    btn_new_trial = tk.Button(experiment_window, text="New Trial", command=new_trial)
    btn_new_trial.pack()

    # Create "End Trial" button
    btn_end_trial = tk.Button(experiment_window, text="End Trial", command=end_trial)
    btn_end_trial.pack()

    # Create "End Experiment" button
    btn_end_experiment = tk.Button(experiment_window, text="End Experiment", command=end_experiment)
    btn_end_experiment.pack()

    # Close the previous window
    new_window.destroy()

    # Hide the main window
    root.withdraw()

def new_experiment():
    # Create a new window
    global new_window
    new_window = tk.Toplevel(root)
    new_window.geometry("800x600")

    #Creates the folder for the new experiment and returns the path to the folder
    path_experiment = controller.load_experiment_folder()

    # Create a label
    label = tk.Label(new_window, text="Participant ID")
    label.pack()

    # Create a text entry field
    global entry_part_ID
    entry_part_ID = tk.Entry(new_window)
    entry_part_ID.pack()

    # Create a button
    button = tk.Button(new_window, text="Start Experiment", command=start_experiment)
    button.pack()

    # Hide the main window
    root.withdraw()

# Create the main window
root = tk.Tk()
root.geometry("800x600")

# Create a button
btn_new_experiment = tk.Button(root, text="New Experiment", command=new_experiment)
btn_new_experiment.pack()

# Run the main event loop
root.mainloop()
