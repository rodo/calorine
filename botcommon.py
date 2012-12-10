"""
Common bits and pieces used by the various bots.

Source : http://code.google.com/p/ircbot-collection/
License : GPVv2
"""

import time
from threading import Thread, Event

class OutputManager(Thread):
  def __init__(self, connection, delay=.5):
    Thread.__init__(self)
    self.setDaemon(1)
    self.connection = connection
    self.delay = delay
    self.event = Event()
    self.queue = []
    self.go_on = True

  def run(self):
    while self.go_on:
      self.event.wait()
      while self.queue:
        msg,target = self.queue.pop(0)
        self.connection.privmsg(target, msg)
        time.sleep(self.delay)
      self.event.clear()

  def send(self, msg, target):
    self.queue.append((msg.strip(),target))
    self.event.set()

  def stop(self):
    self.go_on = False
