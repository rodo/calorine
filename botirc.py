#!/usr/bin/env python
# -*- coding: utf8 -*

import os
import sys
import irclib
import ircbot
import syslog
import socket
from threading import Thread
from botcommon import OutputManager
from random import random
from optparse import OptionParser

"""
debian package python-irclib
"""

class BotModeration(ircbot.SingleServerIRCBot):
    def __init__(self, chan):
        """
        Constructeur qui pourrait prendre des paramètres dans un "vrai" programme.
        """
        ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)],
                                           "calorine", "IRC bot for Calorine radio")
        self.insultes = ["con", "pute", "connard"]

        self.queue = OutputManager(self.connection, .9)
        self.queue.start()

        self.inputthread = sockinput(self)
        self.inputthread.start()
        self.chan = chan

    def on_welcome(self, serv, ev):
        """
        Méthode appelée une fois connecté et identifié.
        Notez qu'on ne peut rejoindre les canaux auparavant.
        """
        serv.join(self.chan)
        wmsg = ["yo les baiseaux", "salut les bouseux",
                "coucou les filles", "coucou tout le monde",
                "\o calorine est dans la place !", "Yi ah c'est moi !",
                "kikoo les chouchous", "salut les bouseux",
                "yo gros", "bonjour bonjour les amours"]
        rand = int(random() * 10)
        serv.privmsg(self.chan, wmsg[rand])

    def on_kick(self, serv, ev):
        """
        auto rejoin on kick
        """
        serv.join(self.chan)
        serv.privmsg(self.chan, "qui c'est qui qui ma kické, kiki ?")

    def on_pubmsg(self, serv, ev):
        """
        Méthode appelée à la réception d'un message
        """
        # Il n'est pas indispensable de passer par des variables
        # Ici elles permettent de clarifier le tout.
        auteur = irclib.nm_to_n(ev.source())
        canal = ev.target()
        message = ev.arguments()[0].lower() # Les insultes sont écrites en minuscules.

        for insulte in self.insultes:
            if insulte in message:
                serv.privmsg(self.chan, "t'es gentil %s mais tu te calmes" % auteur)
                break

        if message == "calorine: cassos":
            self.queue.stop()
            self.speak("ok je comprends")
            self.inputthread.go_on = False
            serv.disconnect("Au revoir, comme aurait dit VGE")
            sys.exit(0)

    def speak(self, message):
        """
        speak on chan
        """
        self.queue.send(message, self.chan)

class sockinput(Thread):
    """Listen on a sockfile
    """

    def __init__(self, bot):
        Thread.__init__(self)
        self.sockfile = "/tmp/calorine.socket"
        self.bot = bot
        self.go_on = True
        if os.path.exists( self.sockfile ):
            os.remove( self.sockfile )

        syslog.syslog("Opening socket...")

        self.server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
        self.server.bind(self.sockfile)
        self.server.listen(5)

    def run(self):

        syslog.syslog("Listening...")
        while self.go_on:
            conn, addr = self.server.accept()

            while True: 
                data = conn.recv( 1024 )
                if not data:
                    break
                else:
                    self.bot.speak(data)


def readopts():
    """
    Read options passed on command line
    """
    parser = OptionParser()
    parser.add_option("--dbname", action="store", type="string", dest="dbname", default=None)
    
    parser.add_option("-c", "--chan",
                      action="store",
                      type="string",
                      dest="chan",
                      default=None)
    
    (options, args) = parser.parse_args()
    return options

def main():
    """
    Main
    """
    options = readopts()
    bot = BotModeration("#%s" % options.chan)
    bot.start()

if __name__ == "__main__":
    main()
    
