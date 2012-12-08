"""

- python-memcache
- python-mutagen

"""
import psycopg2
import memcache
import mutagen
import sys
from os import path
from optparse import OptionParser
from utils import hashfile

class Song():

    def __init__(self):
        """Class initialization"""
        self.conf = self.readopts()
        self.memcache_conn()

    def readopts(self):
        """
        Read options passed on command line
        """
        parser = OptionParser()
        parser.add_option("--dbname", action="store", type="string", dest="dbname", default=None)
        
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
        
        (options, args) = parser.parse_args()

        if options.dbname is None:
            print "dbname is mandatory"
            exit(1)

        conf = "dbname=%s" % options.dbname
        for parm in ['user', 'password', 'host', 'port']:
            if options.__dict__[parm] is not None:
                conf = "%s %s=%s" % (conf, parm, options.__dict__[parm])
        return conf


    def memcache_conn(self):
        """
        Connect to memcache
        """
        self.memcache = memcache.Client(['127.0.0.1:11211'], debug=0)

    def onair(self, song, score):
        """
        Store the actual playing song
        """
        datas = mutagen.File(song, easy=True)

        self.memcache.set("onair_title", datas["title"][0])
        self.memcache.set("onair_artist", datas["artist"][0])
        self.memcache.set("onair_score", score)
        self.memcache.set("onair_full", "%s - %s" % (datas["artist"][0],
                                                     datas["title"][0]))

    def next(self):
        """Do the job"""
        res = 0
        conn = psycopg2.connect(self.conf)
        x = 0
        if conn:
            rows = self.fetchfile(conn)
            filename = rows[1]
            song_id = rows[0]
            song_score = rows[2]

            cur = conn.cursor()
            query = """UPDATE caro_song set played = played + 1, score = 0 WHERE id=%s"""
            cur.execute(query, (song_id, ))

            query = """INSERT INTO caro_historyentry (song_id, date_played) VALUES (%s, now())"""
            cur.execute(query, (song_id, ))

            self.onair(filename, song_score)

            conn.commit()
            conn.close()

        return filename

    def fetchfile(self, conn):
        """

        """
        cur = conn.cursor()
        exists = False
        i = 0
        limit = 1000
        datas = None
        while (not exists) and (i < limit):
            query = """SELECT id, filename, score FROM caro_song WHERE score >= 0 ORDER by played ASC, score DESC, uniq ASC LIMIT 1"""
            cur.execute(query)
            rows = cur.fetchall()
            i = i + 1
            exists = path.isfile(rows[0][1])
            datas = rows[0]

            if not exists:
                self.markfile(conn, datas[0])
                print datas[1]

        return datas
        
    def markfile(self, conn, song_id):
        """
        Mark a song with score = -1000
        """
        cur = conn.cursor()
        query = """UPDATE caro_song SET score = -1000 WHERE id=%s"""
        cur.execute(query, (song_id, ))


    def checkfile(self, conn, fsig):
        qry = "SELECT id FROM caro_song WHERE uniq=%s"
        cur = conn.cursor()
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

        conn = psycopg2.connect(self.conf)
        cur = conn.cursor()

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
                chk = self.checkfile(conn, fsig)
                if chk == 0:
                    self.insertfile(conn, 
                                    [filename, artist, album, title, genre, fsig])
                else:
                    print "File exists in DB"
            else:
                print "Missiong tag"
            conn.commit()
        conn.close()




    def insertfile(self, conn, datas):
        """
        Insert datas in database
        """
        query = """INSERT INTO caro_song (score, filename, artist, album, title, genre, played, uniq) VALUES (0, %s, %s, %s, %s, %s, 0, %s);"""
        cur = conn.cursor()
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

