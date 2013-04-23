#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# This is a simple capture program that will capture a section of
# the screen on a decided interval and then output the images
# with their corresponding timestamps. (Borrowed from stackoverflow).
# This will continue to capture for the seconds specified by argv[1]

import gtk.gdk
import time
import sys
import config


base_name = sys.argv[1]
mode = None
if len(sys.argv) > 2:
  mode = sys.argv[2]


print "Starting Capture"
print "================"

X = 0
Y = 0
W = 800
H = 580

w = gtk.gdk.get_default_root_window()
sz = w.get_size()
sz = (W, H)

wait_time = 3
next_time = 0

for i in xrange(0, config.CAPTURE_NUM):
  if mode == 'wait':
    for t in xrange(wait_time):
      print '%s...' % (t)
      time.sleep(1)
    current_time = next_time
    next_time += 1
  else:
    current_time = int(time.time())

  filename = str(current_time)

  pointer = w.get_pointer()

  f = open(base_name + '/screenshot_' + filename + '.txt', 'w')
  f.write('%s,%s' % (pointer[0], pointer[1]))
  f.close()

  pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
  pb = pb.get_from_drawable(w,w.get_colormap(),X,Y,0,0,sz[0],sz[1])
  if (pb != None):
    pb.save(base_name + '/screenshot_' + filename + '.png', 'png')
    print "Screenshot " + str(i) + " saved."
  else:
    print "Unable to get the screenshot."
  time.sleep(config.CAPTURE_DELAY)
