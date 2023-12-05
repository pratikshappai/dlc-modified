import csv
import os

def save_array_to_csv(array, path, filename):
    file_path = os.path.join(path, filename)

    # Open the file in write mode
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the array to the CSV file
        writer.writerows(array)

