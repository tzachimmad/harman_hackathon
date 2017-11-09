#!/usr/bin/env python
import pygst
pygst.require('0.10')
import gst
import sys
from Xlib import display
import time

LEFT = 1919.0
BOTTOM =1079.0

def mousepos():
	"""mousepos() --> (x, y) get the mouse coordinates on the screen (linux, Xlib)."""
	data = display.Display().screen().root.query_pointer()._data
	return data["root_x"], data["root_y"]

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
	while (True):
		time.sleep(0.2)
		x,y = mousepos()
		volumes = calc_distance(float(x),float(y))
		set_volume(players,volumes)
		print volumes[0],volumes[1],volumes[2]

main()
##if __name__ == "__main__":
   ## try:
  ##	  main()
  ##  except:
   ##	 print "Error occured"
   ##	 sys.exit(1)
