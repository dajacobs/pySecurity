#!/usr/bin/env python

import socket
import paramiko
import threading
import sys

# Use key from Paramiko demo files
host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInferface):
	def _init_(self):
		self.event = threading.Event()
	def check_channel_request(self, king, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	def check_auth_password(self, username, password):
		if(username == 'justin') and (password == 'lovesthepython'):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
server = sys.argv[1]
ssh_port = int(sys.argv[2])
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((server, ssh_port))
	socket.listen(100)
	print '[+] Listening for connection ...'
	client, addr = sock.accept()
except Exception,e:
	print '[-] Listen failed: ' + str(e)
	sys.exit(1)
print '[+] God a connection!'								