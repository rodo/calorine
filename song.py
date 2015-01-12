# -*- coding: utf-8 -*-
#
# Copyright (c) 2013,2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
"""

- python-memcache
- python-mutagen

"""
import psycopg2
import memcache
import mutagen
from random import randint
import sys
from os import path
from optparse import OptionParser
from utils import hashfile


class Song():
    
    prefix = 'calorine_'

    def __init__(self):
        """Class initialization"""
        self.listener = ""
        self.conf = self.readopts()
        self.memcache = self._memcache_conn()
        self.conn = psycopg2.connect(self.conf)

    def readopts(self):
        """
        Read options passed on command line
        """
        parser = OptionParser()
        parser.add_option("--dbname",
                          action="store",
                          type="string",
                          dest="dbname",
                          default=None)

        parser.add_option("--user",
                          action="store",
                          type="string",
                          dest="user",
                          default=None)

        parser.add_option("--password",
                          action="store",
                          type="string",
                          dest="password",
                          default=None)

        parser.add_option("--host",
                          action="store",
                          type="string",
                          dest="host",
                          default=None)

        parser.add_option("--port",
                          action="store",
                          type="string",
                          dest="port",
                          default=None)

        parser.add_option("--listener",
                          action="store",
                          type="string",
                          dest="listener",
                          default=None)

        (options, args) = parser.parse_args()
        self.listener = options.listener

        if options.dbname is None:
            print "dbname is mandatory"
            exit(1)

        conf = "dbname=%s" % options.dbname
        for parm in ['user', 'password', 'host', 'port']:
            if options.__dict__[parm] is not None:
                conf = "%s %s=%s" % (conf, parm, options.__dict__[parm])
        return conf


    def _memcache_conn(self):
        """
        Connect to memcache
        """
        return memcache.Client(['127.0.0.1:11211'], debug=0)

    def onair(self, song, score, songid):
        """
        Store the actual playing song
        """
        for key in ['title', 'artist', 'score', 'full', 'songid']:
            self.memcache.delete("%s:1:onair_%s" % (self.prefix, key))

        try:
            datas = mutagen.File(song, easy=True)
        except:
            pass

        try:
            self.memcache.set("%s:1:onair_songid" % self.prefix, songid)
            self.memcache.set("%s:1:onair_title" % self.prefix, datas["title"][0])
            self.memcache.set("%s:1:onair_artist" % self.prefix, datas["artist"][0])
            self.memcache.set("%s:1:onair_score" % self.prefix, score)
        except:
            pass

        try:
            self.memcache.set("%s:1:onair_full" % self.prefix,
                              "%s - %s" % (datas["artist"][0],
                                           datas["title"][0]))
        except:
            pass

    def next(self):
        """Do the job"""
        res = 0

        x = 0

        rows = self.next_playlist()
        if rows is None:
            rows = self.next_random()
        filename = rows[1]
        song_id = rows[0]
        song_score = rows[2]

        cur = self.conn.cursor()
        query = """UPDATE caro_song set played = played + 1, score = 0 WHERE id=%s"""
        cur.execute(query, (song_id, ))

        self.memcache.delete("%s:1:song_%d" % (self.prefix, song_id))

        query = """DELETE FROM caro_playlistentry WHERE song_id=%s"""
        cur.execute(query, (song_id, ))

        query = """INSERT INTO caro_historyentry (song_id, date_played) VALUES (%s, now())"""
        cur.execute(query, (song_id, ))

        self.onair(filename, song_score, song_id)

        self.conn.commit()

        return filename


    def userpl(self):
        """
        Fetch favorites songs from a user
        """
        qry = " ".join(["SELECT distinct(s.filename) from caro_song s",
                        "INNER JOIN caro_vote v on s.id=v.song_id",
                        "INNER JOIN auth_user u on u.id=v.user_id",
                        "WHERE u.username=%s"])

        cur = self.conn.cursor()
        cur.execute(qry, (self.listener,))
        datas = cur.fetchall()
        cur.close()

        rows = [row[0] for row in datas]
        return rows


    def next_playlist(self):
        """
        Fetch song from playlist
        """
        query = """SELECT s.id, s.filename, s.score FROM caro_playlistentry AS p, caro_song as s WHERE s.id = p.song_id AND s.score >= 0 ORDER BY p.score DESC, p.rank, p.date_add ASC LIMIT %s"""
        rows = self.fetchfile(query, (1,))
        return rows

    def next_random(self):
        """
        Fetch a random song
        """
        query = """SELECT id, filename, score FROM caro_song """
        query = query + """WHERE score >= 0 AND ( played = 0 """
        query = query + """ OR (played > 0 AND global_score > 0 ) )"""
        query = query + """ORDER by played ASC, global_score DESC, uniq ASC LIMIT %s OFFSET %s"""
        rows = self.fetchfile(query, (1, randint(1,100),))
        return rows


    def fetchfile(self, query, parms):
        """
        Fetch file from db and mark it as deleted if not exists
        """
        cur = self.conn.cursor()
        exists = False
        i = 0
        limit = 1000
        datas = None
        while (not exists) and (i < limit):
            cur.execute(query, parms)
            rows = cur.fetchall()
            if len(rows) == 0:
                break
            i = i + 1
            exists = path.isfile(rows[0][1])
            datas = rows[0]

            if not exists:
                self.markfile(datas[0])

        return datas

    def markfile(self, song_id):
        """
        Mark a song with score = -1000
        Delete the file from Playlist
        """
        cur = self.conn.cursor()
        query = """UPDATE caro_song SET score = -1000 WHERE id=%s"""
        cur.execute(query, (song_id, ))

        self.memcache.delete(":1:song_%d" % song_id)

        query = """DELETE FROM caro_playlistentry WHERE song_id=%s"""
        cur.execute(query, (song_id, ))


    def checkfile(self, fsig):
        qry = "SELECT id FROM caro_song WHERE uniq=%s"
        cur = self.conn.cursor()
        cur.execute(qry, (fsig,))
        datas = cur.fetchall()
        cur.close()
        return len(datas)

    def newsong(self, filename):
        """
        Create a new song in database
        """
        datas = None
        try:
            unicode(filename)
        except UnicodeDecodeError:
            return

        cur = self.conn.cursor()

        try:
            datas = mutagen.File(filename, easy=True)
        except:
            query = """INSERT INTO caro_logs (filename, message, date_import) VALUES (%s, 'ERROR 01', now());"""
            cur.execute(query, (filename,))


        if datas is not None:
            artist = None
            album = None
            title = None
            genre = None

            try:
                artist = datas['artist'][0]
                album = datas['album'][0]
                title = datas['title'][0]
                genre = datas['genre'][0]
            except KeyError as e:
                msg = str(sys.exc_type), ":", "%s is not in the list." % sys.exc_value

                query = """INSERT INTO caro_logs (filename, message, date_import) VALUES (%s, %s, now());"""
                cur.execute(query, (filename, msg, ))

            if artist and album and genre and title:
                fsig = hashfile(filename)
                chk = self.checkfile(fsig)
                if chk == 0:
                    self.insertfile([filename, artist, album, title, genre, fsig])
                else:
                    self.update_path(filename, fsig)
            else:
                print "Missing tag"
            self.conn.commit()

    def update_path(self, fname, sig):
        """
        Update file in database
        """
        query = """UPDATE caro_song SET filename=%s WHERE uniq=%s"""
        cur = self.conn.cursor()
        try:
            cur.execute(query, (fname, sig,))
        except:
            pass

    def insertfile(self, datas):
        """
        Insert datas in database
        
        Global score is set to 1 at creation to push the song in the
        mains stream
        """
        query = """INSERT INTO caro_song (score, filename, artist, album, title, genre, played, uniq, global_score, family) VALUES (0, %s, %s, %s, %s, %s, 0, %s, 1, 0);"""
        cur = self.conn.cursor()
        try:
            cur.execute(query, (datas[0],
                                datas[1],
                                datas[2],
                                datas[3],
                                datas[4],
                                datas[5]
                                ))
        except KeyError:
            query = """INSERT INTO caro_logs (filename, message, date_import) VALUES (%s, 'ERROR 02', now());"""
            cur.execute(query, (datas[0],))

