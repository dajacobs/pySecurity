#!/usr/bin/env python

#UDP Host Discovery Tool
import socket
import os

#list for host
host = '192.168.0.196'

#raw socket with bind to public interface
if os.name == 'nt':
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))

#IP header included in capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
#IOCTL for Windows, promiscuous mode
if os.name = 'nt':
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

#read single packet
print sniffer.recvfrom(65565)

#Turn off promiscuous, if not Windows
if os.name == 'nt':
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)			