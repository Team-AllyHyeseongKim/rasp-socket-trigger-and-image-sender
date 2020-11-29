import numpy as np
import os
import cv2
import socket
import time
import struct


def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


TCP_IP = '192.168.0.21'
TCP_PORT = 4965

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]


cap = cv2.VideoCapture(0)

sock = socket.socket()

while True:
    sock.connect((TCP_IP, TCP_PORT))
    myip = ip2int(get_ip_address())
    sock.send(struct.pack('I', myip))


    sock.recv(1)

    startT = time.time()
    while(cap.isOpened()):
        cap.grab()
        ret, frame = cap.retrieve()
        result, encoded = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(encoded)
        imageByte = data.tobytes()
        #print(len(imageByte))
        TS = time.time()-startT
        #print(TS);
        sock.send(struct.pack('d', TS))
        sock.send(str(len(imageByte)).ljust(16).encode())
        sock.send(imageByte)
        

cap.release()
sock.close()




























