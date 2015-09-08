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