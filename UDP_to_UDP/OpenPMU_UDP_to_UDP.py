# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 18:26:46 2021

@author: OpenPMU.org
"""
import signal, sys
import socket
import json

import datetime, time

# Keyboard Interrupt event handler (CTRL+C to quit)
def signal_handler(signal, frame):
    global runLoop 
    runLoop = False
    print('You pressed Ctrl+C!')
    mcTxSock.close()
    udpRxSock.close()
    sys.exit(0)
  
# Load the config file
def loadConfig(configFile="config.json"):
    with open(configFile) as jsonFile:
        return json.load(jsonFile)
    
# Heartbeat 'tick' on console
def heartbeat(prev):
    now = datetime.now()
    if now.second != prev.second:
        print(".", end="", flush=True)
    return now

def UDPreceive(UDP_IP, UDP_PORT):
    udpRxSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # Internet, UDP
    udpRxSock.bind((UDP_IP, UDP_PORT))
    udpRxSock.settimeout(1)                                         # Timeout 1 second
    return udpRxSock

def UDPtransmit():
    socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP 
    return udpTxSock

if __name__ == '__main__':
    
    # Keyboard interrupt
    signal.signal(signal.SIGINT, signal_handler)
        
    print("OpenPMU - UDP to UDP")
    
    config = loadConfig("config.json")
    
    UDP_IP_in        = config["UDP_IP_in"]
    UDP_PORT_in      = config["UDP_PORT_in"]
    UDP_IP_out       = config["UDP_IP_out"]
    UDP_PORT_out      = config["UDP_PORT_out"]
        
    # Setup UDP Receive Socket
    udpRxSock = UDPreceive(UDP_IP, UDP_PORT)
     
    # Setup UDP Transmit Socket
    udpTxSock = UDPtransmit()
    
    print("UDP_IP_in:     {:>15}   - UDP_PORT_in:    {}".format(UDP_IP_in, UDP_PORT_in))
    print("UDP_IP_out:    {:>15}   - UDP_PORT_out:   {}".format(UDP_IP_out, UDP_PORT_out))
    print("Go!")
    
    # Loop forever (CTRL+C to quit)
    runLoop = True
    while runLoop:
        try:
            # Receive UDP, send to UDP
            data, addr = udpRxSock.recvfrom(10240)  # buffer size is 10240 bytes
            udpTxSock.sendto(data, (UDP_IP_out, UDP_PORT_out))
            # Heartbeat on console
            prev = heartbeat(prev)
        except Exception as e:
            print(e)
            pass
        
    udpTxSock.close()
    udpRxSock.close()
        
    
    
    
