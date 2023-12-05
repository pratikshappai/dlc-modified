import socket
import time
from pynput import keyboard

# Set the IP address and port number to send to
ip_address = "127.0.0.1"
port_number = 53450

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout for receiving messages (1 second)
sock.settimeout(0.1)

print("start")
t = 0

output = []

# This will change when 's' is pressed
continue_loop = True

def on_press(key):
    global continue_loop
    try:
        if key.char == 's':
            continue_loop = False
    except AttributeError:
        pass

# Start the listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

while continue_loop:
    if t!=time.time():
        message = '{"type":"ping"}'.encode() 
        sock.sendto(message, (ip_address, port_number)) 
        t=time.time()
        
    # Receive a message from the target IP address and port
    try: 
        data, address = sock.recvfrom(10000) 
        output.append(data.decode())
        #print(f"Received message: {data.decode()} from {address}")
    except Exception as e: 
        pass

listener.stop()

print(output)
print("Loop stopped")
