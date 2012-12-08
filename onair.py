"""

- python-memcache

"""
import memcache


class onair():

    def __init__(self):
        """Class initialization"""
        self.memcache_conn()

    def memcache_conn(self):
        """
        Connect to memcache
        """
        self.memcache = memcache.Client(['127.0.0.1:11211'], debug=0)

    def onair(self):
        """
        Store the actual playing song
        """
        print "Titre : %s" % self.memcache.get("onair_title")
        print "Artist : %s" % self.memcache.get("onair_artist")
        print "Full : %s " % self.memcache.get("onair_full")
        print "Score : %s " % self.memcache.get("onair_score")

if __name__ == "__main__":
    onair = onair()
    onair.onair()
