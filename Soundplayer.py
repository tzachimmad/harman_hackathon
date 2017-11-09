#!/usr/bin/env python
import pygst
pygst.require('0.10')
import gst
import sys
import time
import socket
import sys

LEFT = 1919.0
BOTTOM =1079.0

def calc_distance(x,y):
	prog = 2201/10
	volume_a= int((x**2 + y**2)**0.5)
	volume_b =  int(((LEFT-x)**2 + y**2)**0.5)
	volume_c = int((x**2 + (BOTTOM-y)**2)**0.5)
	volume_a = 10-int(volume_a/prog)
	volume_b = 10-int(volume_b/prog)
	volume_c = 10-int(volume_c/prog)
	arr = [volume_a,volume_b,volume_c]
	max_num = max(arr)
	for i in range(0,len(arr)):
		if arr[i]!=max_num:
			arr[i] -= max_num-arr[i] +1
		if arr[i]<0:
			arr[i]=0
	return arr

def calc_volumes(a,b,c):
	
	maxdist=2201
    #max(max(a,b),c)
	
	vola=int(10-a/maxdist*10);
	volb=int(10-b/maxdist*10);
	volc=int(10-c/maxdist*10);
	
	arr = [vola,volb,volc]
	
	return arr



def set_volume(players,volumes):
	for i in range(0,len(players)):
		players[i].set_property('volume',volumes[i])

def create_player(fname):
	pl = gst.element_factory_make("playbin", "player")
	pl.set_property('uri','file://'+fname)
	return pl

def main():
	players = []
	for i in range(1,len(sys.argv)):
		players.append(create_player(str(sys.argv[i])) )
	for pl in players:
		pl.set_state(gst.STATE_PLAYING)
	
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Bind the socket to the port
	server_address = ('0.0.0.0', 10000)
#	server_address = ('localhost', 10000)

	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)

	#Listen for incoming connections
	sock.listen(1)
	
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()

	while True:
		
	 
		try:
			print >>sys.stderr, 'connection from', client_address
			
		# Receive the data in small chunks and retransmit it
			while True:
				data = connection.recv(64)
				print >>sys.stderr, 'received "%s"' % data
				if data:
					#print >>sys.stderr, 'sending data back to the client'
					xy=data.split(',');
					a=float(xy[0])
					b=float(xy[1])
					c=float(xy[2])
					d=float(xy[3])
					#volumes = calc_distance(float(x),float(y))
					volumes = calc_volumes(a,b,c)
					set_volume(players,volumes)
					print volumes[0],volumes[1],volumes[2]
					#connection.sendall(data)
				else:
					print >>sys.stderr, 'no more data from', client_address
					#break
		finally:
		# Clean up the connection
			connection.close()
			break

main()
