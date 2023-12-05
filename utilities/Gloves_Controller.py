import socket
import time

def get_glove_port_number(hand):
    if hand == "right":
        port_number = 53450
    else:
        port_number = 53451
    return port_number

def get_glove_ip():
    ip_address = "127.0.0.1"
    return ip_address

def get_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0.1)
    return sock

def get_data(t,sock,ip,port):
    if t!=time.time():
        message = '{"type":"ping"}'.encode() 
        sock.sendto(message, (ip, port)) 
        t=time.time()
    # Receive a message from the target IP address and port
    try: 
        data, address = sock.recvfrom(10000) 
        decoded = data.decode()
        return decoded, t
    except Exception as e: 
        return "nothing", t
