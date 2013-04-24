#!/usr/bin/env python
# Benjamin James Wright <bwright@cse.unsw.edu.au>
# This is a simple capture program that will capture a section of
# the screen on a decided interval and then output the images
# with their corresponding timestamps. (Borrowed from stackoverflow).
# This will continue to capture for the seconds specified by argv[1]

import gtk.gdk
import glib
import time
import sys
import config



X = 0
Y = 0
W = 863
H = 580

w = gtk.gdk.get_default_root_window()
sz = w.get_size()
sz = (W, H)


wait_time = 3

base_name = sys.argv[1]
mode = None
if len(sys.argv) > 2:
  mode = sys.argv[2]


class State:
  pass
state = State()
state.frame_number = 0
state.running = False


def countdown(delay):
  for t in xrange(delay):
    print '%s...' % (wait_time - t)
    time.sleep(1)


def yieldsleep(func):
  def start(*args, **kwds):
    iterable = func(*args, **kwds)
    def step(*args, **kwds):
      try:
        time = next(iterable)
        glib.timeout_add_seconds(time, step)
      except StopIteration:
        pass
    glib.idle_add(step)
  return start


@yieldsleep
def advance_loop(state):
  while state.running:
    advance(state)
    yield wait_time


def toggle_auto_advance(state):
  if state.running:
    print 'Stopping auto capture'
    state.running = False
    return
  else:
    print 'Starting auto capture, ctrl-alt-m to stop...'
    state.running = True
    countdown(wait_time)
    advance_loop(state)


def advance(state):
  if mode == 'wait_key':
    current_time = state.frame_number
  elif mode == 'wait_time':
    current_time = state.frame_number
  else:
    current_time = int(time.time())
  state.frame_number += 1

  filename = str(current_time)

  pointer = w.get_pointer()

  f = open(base_name + '/screenshot_' + filename + '.txt', 'w')
  f.write('%s,%s' % (pointer[0], pointer[1]))
  f.close()

  pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
  pb = pb.get_from_drawable(w,w.get_colormap(),X,Y,0,0,sz[0],sz[1])
  if (pb != None):
    pb.save(base_name + '/screenshot_' + filename + '.png', 'png')
    print "Screenshot " + filename + " saved."
  else:
    print "Unable to get the screenshot."


if mode == 'wait_key':
  print 'Press ctrl-alt-n to capture, ctrl-alt-m to toggle 3sec loop...'
  import keybinder
  keybinder.bind('<Ctrl><Mod1>n', advance, state)
  keybinder.bind('<Ctrl><Mod1>m', toggle_auto_advance, state)
  gtk.main()
elif mode == 'wait_time':
  while True:
    countdown(wait_time)
    advance(state)
else:
  while True:
    advance(state)
    time.sleep(config.CAPTURE_DELAY)
