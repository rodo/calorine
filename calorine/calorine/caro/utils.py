# -*- coding: utf-8 -*-
#
# Copyright (c) 2012,2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
Utils for calorine.caro
"""
import os
import logging
import shutil
import sys
import hashlib
import mutagen
from django.conf import settings
from django.core.cache import cache
from django.db.models import Min
from celery.task import task
from calorine.caro.models import Logs
from calorine.utils.lastfm import get_tags
from calorine.utils.lastfm import get_picture
from calorine.caro.models import Song
import subprocess

logger = logging.getLogger(__name__)


def clean_cache(user_id, song_id, ple_id):
    """Remove data in cache
    """

    key = 'ple_{}_{}'.format(user_id, ple_id)
    song_key = 'song_{}'.format(song_id)

    cache.delete(key)
    cache.delete(song_key)
    return 0


def checkid3(filename):
    """
    Create a new song in database
    """
    datas = None
    mdat = None

    try:
        mdat = mutagen.File(filename, easy=True)
    except:
        msg = "mutagen failed %s" % sys.exc_value
        Logs.objects.create(filename=filename, message=msg)

    if mdat is not None:
        try:
            genre = mdat['genre'][0]
        except:
            genre = ''

        try:
            datas = {'artist': mdat['artist'][0],
                     'album': mdat['album'][0],
                     'title': mdat['title'][0],
                     'genre': genre}
        except KeyError:
            msg = "%s : %s is not in the list." % (str(sys.exc_type),
                                                   sys.exc_value)
            Logs.objects.create(filename=filename, message=msg)

    return datas


def sigfile(fpath):
    """
    Calculate the sha1 value of a file
    """
    sigsha = hashlib.sha1()
    fbj = open(fpath, 'rb')
    try:
        sigsha.update(fbj.read())  # pylint: disable-msg=E1101
    finally:
        fbj.close()
    return sigsha.hexdigest()


def onair_datas(userid):
    """Read onair datas from cache
    """

    songid = cache.get('onair_songid')
    artist = cache.get('onair_artist')
    title = cache.get('onair_title')
    album = cache.get('onair_album')

    song_key = 'song_{}_user_{}'.format(songid, userid)

    voted = cache.get(song_key)

    if voted is None:
        voted = 'null'

    datas = {'artist': artist,
             'title': title,
             'album': album,
             'songid': songid,
             'user_vote': voted}

    return datas


def importdir(path):
    """
    Import all files present in dir recursively

    Return an array containing all paths
    """
    paths = []
    extensions = ['ogg']
    dirlist = []
    try:
        dirlist = os.listdir(path)
    except OSError:
        pass

    for filename in dirlist:
        if os.path.isdir(os.path.join(path, filename.strip())):
            for filex in importdir(os.path.join(path,
                                                filename.strip())):
                paths.append(filex)
        else:
            ext = filename.split('.')[-1]
            if ext in extensions:
                paths.append(os.path.join(path, filename.strip()))

    return paths


def importsong(fpath):
    """Import a file as a song
    """
    result = ""

    tags = checkid3(fpath)
    if tags is not None:
        sig = sigfile(fpath)
        exsong = Song.objects.filter(uniq=sig)

        if len(exsong) > 0:
            if exsong[0].filename != fpath:
                result = updatesong(exsong[0], fpath)
            else:
                result = "[X] %s" % exsong[0].title
        else:
            result = createsong(tags, sig, fpath, songminplay())
    else:
        logger.error('No tags found in [%s]' % fpath)

    return result


def songminplay():
    """The min played from all songs
    """
    played = Song.objects.filter(score__gte=0).aggregate(Min('played'))
    if played['played__min'] is None:
        result = 0
    else:
        result = played['played__min']
    return result


def updatesong(song, fpath):
    """Update the path if file moved
    """
    song.filename = fpath
    song.save()
    return "[U] %s\n" % song.title


def createsong(tags, sig, fpath, played=0):
    """Create a new song in db
    """

    song = Song.objects.create(artist=tags['artist'],
                               album=tags['album'],
                               title=tags['title'],
                               genre=tags['genre'],
                               score=0,
                               played=played,
                               uniq=sig,
                               global_score=0,
                               filename=fpath)
    # lookup to fill cover
    picture.delay(song)
    
    if hasattr(song, 'title') and song.title != '':
        try:
            song.genre += ','.join(get_tags(song.artist, song.title))
        except:
            pass
    song.save()
    return "[I] %s\n" % song.title


@task()
def picture(song):
    """
    Return a picture of the album containing this song
    """
    pict = None
    if song.cover == '' or song.cover is None:
        pict = get_picture(song.artist, song.title)
        if pict:
            song.cover = pict
            song.save()
        else:
            logger.warning('no picture found for %s %s' % (song.artist,
                                                           song.title))
    return pict


def move_file(path_from, filename):
    """Move file from nginx upload_store to UPLOAD_DEST_DIR

    path_from is an nginx datas
    """
    finaldir = getormakedir(settings.UPLOAD_DEST_DIR, filename)

    path_to = os.path.join(finaldir, filename)

    if not os.path.exists(path_to):
        shutil.copyfile(path_from, path_to)
        if settings.REMOVE_UPLOAD_FILES:
            remove_file(path_from)

    return path_to


def getormakedir(base, random):
    """
    Create path from filename, create the directory corresponding
    if not exists

    Return (string) the path
    """
    sha = hashlib.sha224(random).hexdigest()  # pylint: disable-msg=E1101
    newdir = os.path.join(base, sha[0], sha[1])
    if not os.path.exists(newdir):
        logger.debug("create dir %s" % newdir)
        os.makedirs(newdir)
    return newdir


def remove_file(fpath):
    """Remove file and log on error

    path_from is an nginx datas
    """
    logger.debug("remove file [%s]" % fpath)
    try:
        os.unlink(fpath)
        return 0
    except:
        logger.info("can't delete [%s]" % fpath)
        return 1


def readtags(fname):
    """Read mp3 IDS Tags

    Return array with tags
    """
    datas = {}
    muts = None
    fields = ['album', 'artist', 'title', 'genre', 'date', 'tracknumber',
              'year']
    try:
        muts = mutagen.File(fname, easy=True)
    except:
        logger.error("can't read tags in [%s]" % fname)

    if muts:
        for fld in fields:
            if fld in muts:
                data = muts[fld]
                datas[fld] = data[0]
            else:
                datas[fld] = ''

    return datas


def mp3ogg(fname, datas):
    """
    Encode mp3 files to ogg vorbis
    """
    oggname = "%s.ogg" % fname[:-4]
    logger.info("(mp3ogg) encode [%s]" % fname)
    logger.debug("(mp3ogg) oggenc binary path %s" % settings.OGGENC)
    logger.debug("(mp3ogg) mpg123 binary path %s" % settings.MPG123)

    command = [settings.OGGENC,
               "--artist", datas['artist'],
               "--title", datas['title'],
               "--album", datas['album'],
               "--genre", datas['genre'],
               "--date", datas['date'],
               "--tracknum", datas['tracknumber'],
               "-o", oggname,
               "-"]

    try:
        mpg = subprocess.Popen([settings.MPG123,
                                "-w",
                                "-",
                                fname],
                               stdout=subprocess.PIPE)

        ogg = subprocess.Popen(command,
                               stdin=mpg.stdout,  # pylint: disable-msg=E1101
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        (stdout, stderr) = ogg.communicate()
        logger.debug(stdout)
        logger.error(stderr)
        result = oggname
    except:
        logger.error("(mp3ogg) subprocess failed on [%s]" % fname)
        result = None

    if result:
        os.unlink(fname)

    return result


def mp4ogg(fname):
    """
    Encode mp4 files to ogg vorbis
    """

    logger.info("(mp4ogg) encode [%s] with [%s]" % (fname,
                                                    settings.FFMPEG2THEORA))
    oggname = "%s.oga" % fname[:-4]

    rescom = subprocess.call([settings.FFMPEG2THEORA, fname])
    if rescom == 0:
        logger.debug("(mp4ogg) success on [%s]" % fname)
        result = oggname
    else:
        logger.warning("(mp4ogg) subprocess failed on [%s]" % fname)
        result = None

    if result:
        os.unlink(fname)

    return result
