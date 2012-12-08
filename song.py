"""

- python-memcache
- python-mutagen

"""
import psycopg2
import memcache
import mutagen
import sys

class Song():

    def __init__(self, conf):
        """Class initialization"""
        self.conf = conf
        self.memcache_conn()

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
            cur = conn.cursor()
            query = """SELECT id, filename, score FROM songs ORDER by played ASC, score DESC, uniq ASC LIMIT 1"""
            cur.execute(query)
            rows = cur.fetchall()
            filename = rows[0][1]
            song_id = rows[0][0]
            song_score = rows[0][2]

            query = """UPDATE songs set played = played + 1 WHERE id=%s"""
            cur.execute(query, (song_id, ))

            query = """INSERT INTO played (song_id, date_played) VALUES (%s, now())"""
            cur.execute(query, (song_id, ))

            self.onair(filename, song_score)

            conn.commit()
            conn.close()

        return filename

    def newsong(self, filename):
        """Do the job"""

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

                query = """INSERT INTO caro_song (score, filename, artist, album, title, genre) VALUES (0, %s, %s, %s, %s, %s);"""
                try:
                    cur.execute(query, (filename, artist, album,
                                        title,
                                        genre,
                                        ))
                except KeyError:
                    query = """INSERT INTO caro_logs (filename, message, date_import) VALUES (%s, 'ERROR 02', now());"""
                    cur.execute(query, (filename,))
                    pass


            conn.commit()
        conn.close()
