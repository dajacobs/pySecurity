import sys
import socket
import getopt
import threading
import subprocess

# Global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def usage():
    print "Net Tool"
    print
    print "Usage: net.py -t target_host -p port"
    print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command             - initialize a command shell"
    print "-u --upload=destination  - upon receiving connection, upload a file and write to [destination]"

    print
    print
    print "Examples: "
    print "net.py -t 192.168.0.1 -p 5555 -l -c"
    print "net.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "net.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./net.py -t 192.168.11.12 -p 135"
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SO_STREAM)

    try:
        # Connect to target host
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)
        while True:
            # Wait for data
            recv_len = 1
            response = ""

            while recv_len:
                data     = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # Wait for input
            buffer = raw_input("")
            buffer += "\n"

            # Send data
            client.send(buffer)

    except:
        print "[*] Exception! Exiting."

        # Tear down the connection
        client.close()

def server_loop():
    global target

    # If no target, listen on all interfaces
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.blind((target,port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # Thread to handle new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    # Trim newline
    command = command.rstrip()

    # Run the command and get output
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command.\r\n"

    # Send the output back to the client
    return output

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()
    # Read commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",
        ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"

    # Listen or send data from stdin
    if not listen and len(target) and port > 0:
        # Read in the buffer from the commandline
        # This will block, so send CTRL-D if not sending input
        # to stdin
        buffer = sys.stdin.read()

        # Send data
        client_sender(buffer)

    # Listen and potentially upload things, execute commands,
    # and drop a shell back depending on our command line
    # options above
    if listen:
        server_loop()

main()