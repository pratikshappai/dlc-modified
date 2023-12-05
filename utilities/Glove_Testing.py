import socket
import Gloves_Controller as gloves
from pynput import keyboard
import time
import Read_Write as rw

# Set the IP address and port number to send to
ip = gloves.get_glove_ip()
hand = "right"
port = gloves.get_glove_port_number(hand)

# Create a UDP sockets
sock = gloves.get_socket()

# This will change when 's' is pressed
continue_loop = True

def on_press(key):
    global continue_loop
    try:
        if key.char == 's':
            continue_loop = False
    except AttributeError:
        pass

t = 0
output = []
# Start the listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

while continue_loop:
    new_data, t = gloves.get_data(t,sock,ip,port)
    output.append(new_data)

listener.stop()

path = "C:/Users/Data acquisition/Desktop/Data"
name = "testing.csv"

rw.save_array_to_csv(output,path,name)