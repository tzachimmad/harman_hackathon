#!/usr/bin/env python
import pygst
pygst.require('0.10')
import gst
import sys

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
        i=0

if __name__ == "__main__":
    try:
        main()
    except:
        print "Error occured"
        sys.exit(1)