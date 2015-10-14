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