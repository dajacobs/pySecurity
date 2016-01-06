#!/usr/bin/env python

import socket
import os
from ctypes import *

#host to listen
host = '192.168.0.187'

#IP header
class IP(Structure):
	_fields_ = [('ihl', c_ubyte, 4), ('version', c_ubyte, 4), ('toss', c_ubyte), ('len', c_ushort), ('id', c_ushort), ('offset', c_ushort), ('ttl', c_ubyte), ('protocol_num', c_ubyte), ('sum', c_ushort), ('src', c_ulong), ('dst', c_ulong)]

	def __new__(self, socket_buffer=None):
		return self.from_buffer_copy(socket_buffer)
	def __init__(self, socket_buffer=None):

		#map protocol constant to names
		self.protocol_map = {1:'ICMP', 6:'TCP', 17:'UDP'}
		#human readable IP addresses
		self.src_address = socket.inet_ntoa(struct.pack('<L', self.src))
		self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))
		#human readable protocol
		try:
			self.protocol = self.protocol_map[self.protocol_num]
		except:
			self.protocol = str(self.protocol_num)
if os.name == 'nt':
	socket_protocol = socket.IPPROTO_IP
else:
	socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == 'nt':					
	sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
try:
	while True:
		#read packet
		raw_buffer = sniffer.recvfrom(65565)[0]
		#create IP header from first 20 bytes of buffer
		ip_header = IP(raw_buffer[0:20])

		class ICMP(Structure):
			_fields_ = [('type', c_ubyte), ('code', c_ubyte), ('checksum', c_ushort), ('unused', c_ushort), ('next_hop_mtu', c_ushort)]
			def __new__(self, socket_buffer):
				return self.from_buffer_copy(socket_buffer)
			def __init__(self, socket_buffer):
				pass

		#print out protocol detected and hosts
		print 'Protocol: %s %s -> %s' % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)

		#if ICMP
		if ip_header.protocol = 'ICMP':
			#calculate where ICMP packet starts
			offset = ip_header.ihl * 4
			buf = raw_buffer[offset:offset + sizeof(ICMP)]
			#create ICMP structure
			icmp_header = ICMP(buf)

			print 'ICMP -> Type: %d Code: %d' % (icmp_header.type, icmp_header.code)

#handle CRTRL-C
except KeyboardInterrupt:
	#if Windows, promiscuous mode off
	if os.name == 'nt':
		sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)					