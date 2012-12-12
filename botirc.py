#!/usr/bin/env python
# -*- coding: utf8 -*
#
# Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
import irclib
import ircbot
import syslog
import socket
import subprocess
import memcache
from threading import Thread
from botcommon import OutputManager
from random import random
from optparse import OptionParser
from time import sleep
import ttclient

"""
debian package python-irclib
"""

class BotCalorine(ircbot.SingleServerIRCBot):

    pl_prefix = ["je kiffe", "j'aime", "je like", "donne moi du",
                 "allez balance", "vas-y envoi"]

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
            self.action(message, serv)

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

    def action(self, message, serv):
        msg = message.lower()
        if message.startswith(self.nick):
            if message == "%s: cassos" % self.nick:
                self.queue.stop()
                sleep(.7)  # ensure the stop was read
                self.speak("ok je comprends")
                self.inputthread.stop()
                ttclient.trigger()
                sleep(.2)
                serv.disconnect("Au revoir, comme aurait dit VGE")
                sleep(2)
                syslog.syslog("quit on cassos irc message")
                sys.exit(0)
            elif msg.startswith("%s: asv" % self.nick):
                self.asv()
            elif msg.startswith("%s: onair" % self.nick):
                self.onair()
            else:
                for plp in self.pl_prefix:
                    if msg.startswith("%s: %s" % (self.nick, plp)):
                        self.addpl(message)

    def onair(self):
        """asv command
        """
        conn = '127.0.0.1:11211'
        prefix = "calorine_"
        info = "pas d'info"
        try:
            mmc = memcache.Client([conn], debug=0)
            info = "onair : %s " % (mmc.get("%s:1:onair_full" % prefix))
        except:
            syslog.syslog("error on connecting to memcache %s" % conn)

        self.speak(info)

    def asv(self):
        """asv command
        """
        self.speak("petit curieux va :-) allez rejoint moi sur %s, canailloute" % self.url)

    def addpl(self, message):
        msg = message.lower()

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

        if ' biolay' in msg:
            self.speak("pitié pas Biolay")
            return 0

        if ';' in msg:
            self.speak("hum j'aime pas trop les points-virgules")
            return 0

        if '&' in msg:
            self.speak("je n'aime pas les esperluettes d'abord")
            return 0

        for plp in self.pl_prefix:
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

    def stop(self):
        self.go_on = False

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
                      default="calorine")

    parser.add_option("-n", "--nick",
                      action="store",
                      type="string",
                      dest="nick",
                      default='calorine')

    parser.add_option("-u", "--url",
                      action="store",
                      type="string",
                      dest="url",
                      default='http://calorine.quiedeville.org/')

    (options, args) = parser.parse_args()

    if not options.chan.startswith("#"):
        options.chan = "#%s" % options.chan

    return options

def main():
    """
    Main
    """
    options = readopts()
    bot = BotCalorine(options.nick,
                      options.chan,
                      options.url)
    bot.start()

if __name__ == "__main__":
    main()

