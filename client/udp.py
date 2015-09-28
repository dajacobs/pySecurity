#!/usr/bin/env python

import socket

target_host = "127.0.0.1"
target_port = 80

# create the socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send data
client.sendto("AAABBBCCC", (target_host, target_port))

# receive data
data, addr = client.recvfrom(4096)

print data