import socket
import sys
import time
from Xlib import display



def mousepos():
	"""mousepos() --> (x, y) get the mouse coordinates on the screen (linux, Xlib)."""
	data = display.Display().screen().root.query_pointer()._data
	return data["root_x"], data["root_y"]


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
	# Send data
	while (True):
		time.sleep(2)
		x,y = mousepos()
		message = str(x) + "," + str(y)
		
		print >>sys.stderr, 'sending "%s"' % message
		sock.sendall(message)
	
		# Look for the response
		amount_received = 0
		amount_expected = len(message)
	
		while amount_received < amount_expected:
			data = sock.recv(16)
			amount_received += len(data)
			print >>sys.stderr, 'received "%s"' % data
			if len(data) == 0:
				break
	
finally:
	print >>sys.stderr, 'closing socket'
	sock.close()
