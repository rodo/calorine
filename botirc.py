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
from utils import extract_command

"""
debian package python-irclib
"""

class BotCalorine(ircbot.SingleServerIRCBot):

    pl_prefix = ["donne moi du", "allez balance", "vas-y envoi", "gimme",
                 "balance"]

    manage = os.path.join(os.path.dirname(__file__),
                          'calorine',
                          'manage.py')

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

        insultes = [" con ", " pute ", " connard ", " salope ", " salop ", " crétin ",
                    "pétasse ", " putain ", " bordel "," chier "]

        for insulte in insultes:
            if insulte in message:
                serv.privmsg(self.chan, "ouh que c'est pas beau les gros mots %s" % auteur)
                break

        if message.startswith(self.nick):
            self.action(message, serv, event)

    def on_join(self, serv, event):
        """
        When someone join
        """
        auteur = irclib.nm_to_n(event.source())

        hello = ["salut %s",
                 "coucou %s",
                 "bonjour %s",
                 "quel plaisir de vous accueillir parmi nous %s",
                 "soit le bienvenu parmi nous %s",
                 "yo mon poto %s",
                 "bisous mouillé %s",
                 "allez %s claque m'en 5",
                 "damned voilà %s",
                 "yo %s",
                 "bisous %s",
                 "kiss %s",
                 "ohoho %s",
                 "en ce jour bénit voici que %s arrive parmi nous",
                 "ça fait plaisir de te voir %s",
                 "Big smack pour %s",
                 "%s hi",
                 "%s est dans la place \o/",
                 "hey %s ça claque ?",
                 "tcho %s, ça farte ?",
                 "%s ça va ou bien",
                 "hey what's up %s",
                 "tss % encore dans le coin",
                 "ah bah te v'la %s",
                 "chut le voilà",
                 "kikoo %s",
                 "te voilà enfin %s"]
        rand = int(random() * len(hello))
        if auteur != self.nick:
            self.speak(hello[rand] % auteur)

    def speak(self, message):
        """
        speak on chan
        """
        self.queue.send(message, self.chan)

    def action(self, message, serv, event):
        msg = message.lower()
        if message.startswith(self.nick):

            command = extract_command(message)

            if command == "cassos":
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
            elif command == "asv":
                self.asv()
            elif command == "onair":
                self.onair()
            elif command == "on air":
                self.onair()
            elif command == "like":
                self.like(irclib.nm_to_n(event.source()))
            elif command == "je kiffe":
                self.like(irclib.nm_to_n(event.source()))
            elif command == "love":
                self.like(irclib.nm_to_n(event.source()))
            elif command == "j'aime":
                self.like(irclib.nm_to_n(event.source()))
            elif command == "hate":
                self.hate(irclib.nm_to_n(event.source()))
            elif command == "caca":
                self.hate(irclib.nm_to_n(event.source()))
            elif command == "beurk":
                self.hate(irclib.nm_to_n(event.source()))
            elif command == "pouah":
                self.hate(irclib.nm_to_n(event.source()))
            elif command == "dislike":
                self.hate(irclib.nm_to_n(event.source()))
            elif command == "help":
                self.help()
            else:
                for plp in self.pl_prefix:
                    if command == plp:
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

    def hate(self, nick):
        """Hate a song
        """
        syslog.syslog("action: dislike from %s" % nick)
        res = subprocess.check_output([self.manage, 'ircdislike', nick])
        self.speak(res.rstrip())

    def like(self, nick):
        """Like a song
        """
        syslog.syslog("action: like from %s" % nick)
        res = subprocess.check_output([self.manage, 'irclike', nick])
        self.speak(res.rstrip())

    def help(self):
        """Prints help commands on IRC
        """
        self.speak("prefix the following command by 'nick: '")
        self.speak(" asv : critical information, must sign an NDA to know them")
        self.speak(" cassos : irc bot quit")
        self.speak(" like : I like the song")
        self.speak(" onair : display on air song informations")

    def asv(self):
        """asv command
        """
        self.speak("petit curieux va :-) allez rejoint moi sur %s, canailloute" % self.url)

    def addpl(self, message):
        msg = message.lower()

        syslog.syslog("run %s" % self.manage)
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
                res = subprocess.check_output([self.manage, 'lookup_add_playlist', lookup])
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

