#!/usr/bin/env python
import sys
import socket
import threading

def main():
	if len(sys.argv[1:]) !=5:
		print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
		print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
		sys.exit(0)

		# Local listening parameters
		local_host = sys.argv[1]
		local_port = int(sys.argv[2])

		# Remote target
		remote_host = sys.argv[3]
		remote_port = int(sys.argv[4])

		# Connect proxy and receive data before sending to remote host
		receive_first = sys.argv[5]

		if "True" in receive_first:
			receive_first = True
		else:
			receive_first = False

		# Start listening socket
		server_loop(local_host, local_port, remote_host, remote_port, receive_first)	

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		server.bind((local_host, local_port))
	except:
		print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
		print "[!!] Check for other listening socket or correct permissions."
		sys.exit(0)
	print "[*] Listening on %s:%d" % (local_host, local_port)
	
	server.listen(5)	
	
	while True:
		client_socket, addr = server.accept()

		# Print local connection information
		print "[==>] Received incomding connection from %s:%d" % (addr[0], addr[1])

		# Start thread to talk to the remote host
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))

		proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
	# Connect to remote host
	remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	remote_socket.Connect((remote_host, remote_port))

	# Receive the data from the remote end
	if receive_first:
		remote_buffer = receive_from(remote_socket)
		hexdump(remote_buffer)

		# Send the data to our response handler
		remote_buffer = response_handler(remote_buffer)

		# Send data to locate client
		if len(remote_buffer):
			print "[<==] Sending %d bytes to localhost." % 
			len(remote_buffer)
			client_socket.send(remote_buffer)
	# Loop and read from local, send to remote, and send to local rinse, wash, and repeat
	while True:
		# Read from the local host
		local_buffer = receive_from(client_socket)	

		if len(local_buffer):
			print "[==>] Received %d bytes from localhost." %
			len(local_buffer)
			hexdump(local_buffer)

			# Send to response handler
			remote_buffer = response_handler(remote_buffer)

			# Send reponse to the local socket
			client_socket.send(remote_buffer)

			print "[<==] Sent to localhost."

		# If no data on either side, close connections
		if not len(local_buffer) or not len(remote_buffer):
			client_socket.close()
			remote_socket.close()
			print "[*] No more data. Closing connections."
			break			

# Hexdumping function
def hexdump(src, length=16):
	result = []
	digits = 4 if isinstance(src, unicode) else 2
	for i in xrange(0, len(src), length):
		s = src[i:i+length]
		hexa = b' '.join(["%0+X" % (digits, ord(x)) for x in s])
		text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
		result.append(b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))
	print b'\n'.join(result)

def receive_from(connection):
	buffer = ""

	# Set a two second timeout; depending upon target, may need to adjust
	connection.settimeout(2)
		try:
			# Read into buffer until no more data or timeout
			while True:
				data = connection.recv(4096)
				if not data:
					break
				buffer += data
		except 
			pass
		return buffer	
# Modify any requests destined for remote host
def request_handler(buffer):
	# Packet modification
	return buffer
# Modify any requests destined for remote host	
def response_handler(buffer):
	# Packet modification
	return buffer			
main()		