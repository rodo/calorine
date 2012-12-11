#!/usr/bin/env python
# -*- coding: utf8 -*

import os
import sys
import irclib
import ircbot
import syslog
import socket
import subprocess
from threading import Thread
from botcommon import OutputManager
from random import random
from optparse import OptionParser

"""
debian package python-irclib
"""

class BotCalorine(ircbot.SingleServerIRCBot):

    def __init__(self, nick, chan, url):
        """
        Constructeur qui pourrait prendre des paramètres dans un "vrai" programme.
        """
        ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.net", 6667)],
                                           nick, "IRC bot for Calorine radio")
        self.queue = OutputManager(self.connection, .9)
        self.queue.start()

        self.inputthread = sockinput(self)
        self.inputthread.start()
        self.chan = chan
        self.nick = nick
        self.url = url

    def on_welcome(self, serv, event):
        """
        Méthode appelée une fois connecté et identifié.
        Notez qu'on ne peut rejoindre les canaux auparavant.
        """
        syslog.syslog("irc: join %s" % self.chan)
        serv.join(self.chan)
        wmsg = ["yo les baiseaux", "salut les bouseux",
                "coucou les filles", "coucou tout le monde",
                "\o calorine est dans la place !", "Yi ah c'est moi !",
                "kikoo les chouchous", "salut les bouseux",
                "yo gros", "bonjour bonjour les amours"]
        rand = int(random() * 10)
        serv.privmsg(self.chan, wmsg[rand])

    def on_kick(self, serv, event):
        """
        auto rejoin on kick
        """
        serv.join(self.chan)
        serv.privmsg(self.chan, "qui c'est qui qui ma kické, kiki ?")

    def on_pubmsg(self, serv, event):
        """
        Méthode appelée à la réception d'un message
        """
        # Il n'est pas indispensable de passer par des variables
        # Ici elles permettent de clarifier le tout.
        auteur = irclib.nm_to_n(event.source())
        canal = event.target()
        message = event.arguments()[0].lower() # Les insultes sont écrites en minuscules.

        insultes = ["con ", "pute", "connard", "salope", "salop", "crétin"]

        for insulte in insultes:
            if insulte in message:
                serv.privmsg(self.chan, "t'es gentil %s mais tu te calmes" % auteur)
                break

        if message.startswith(self.nick):
            self.action(message)

    def on_join(self, serv, event):
        """
        When someone join
        """
        auteur = irclib.nm_to_n(event.source())

        hello = ["salut", "coucou", "bonjour",
                 "yo", "bisous", "kiss",
                 "salut", "Big smack pour", "hi",
                 "yo"]
        rand = int(random() * 10)
        if auteur != self.nick:
            self.speak("%s %s" % (hello[rand], auteur))

    def speak(self, message):
        """
        speak on chan
        """
        self.queue.send(message, self.chan)

    def action(self, message):
        msg = message.lower()
        if message.startswith(self.nick):
            if message == "%s: cassos" % self.nick:
                self.queue.stop()
                self.speak("ok je comprends")
                self.inputthread.go_on = False
                serv.disconnect("Au revoir, comme aurait dit VGE")
                sys.exit(0)
            elif msg.startswith("%s: je kiffe " % self.nick):
                self.addpl(message)
            elif msg.startswith("%s: j'aime " % self.nick):
                self.addpl(message)
            elif msg.startswith("%s: donne moi du " % self.nick):
                self.addpl(message)
            else:
                self.speak("tu aimes la musique, ecoute %s" % self.url)

    def addpl(self, message):
        msg = message.lower()
        pl_prefix = ["je kiffe", "j'aime", "je like", "donne moi du"]
        manage = os.path.join(os.path.dirname(__file__),
                              'calorine',
                              'manage.py')
        syslog.syslog("run %s" % manage)
        if 'britney' in msg:
            self.speak("euh, ça non je ne peux pas, Britney ça fait saigner les oreilles, désolé")
            return 0

        if ' dion' in msg:
            self.speak("mais tu sais qu'écouter Céline Dion tue un chaton ?")
            return 0


        if ';' in msg:
            self.speak("hum j'aime pas trop les points-virgules")
            return 0

        if '&' in msg:
            self.speak("je n'aime pas les esperluettes d'abord")
            return 0

        for plp in pl_prefix:
            if msg.startswith("%s: %s" % (self.nick, plp)):
                index = len(self.nick) + 2 + len(plp) + 1
                lookup = message[index:]
                syslog.syslog("action: lookup %s " % lookup)
                res = subprocess.check_output([manage, 'lookup_add_playlist', lookup])
                self.speak(res.rstrip())


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
    nickname = 'calorine'
    url = 'http://calorine.quiedeville.org:8042/chezleo'
    options = readopts()
    bot = BotCalorine(nickname, "#%s" % options.chan, url)
    bot.start()

if __name__ == "__main__":
    main()

