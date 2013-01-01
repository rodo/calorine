# -*- coding: utf-8 -*-
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
from calorine.caro.models import Logs
from calorine.utils.lastfm import get_tags
from calorine.caro.models import Song
import subprocess


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
        unicode(filename)
    except UnicodeDecodeError:
        pass

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


def onair_datas():
    """Read onair datas from cache
    """
    artist = cache.get('onair_artist')
    title = cache.get('onair_title')
    album = cache.get('onair_album')

    datas = {'artist': artist,
             'title': title,
             'album': album}

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
    # Get an instance of a logger
    logger = logging.getLogger(__name__)

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
            result = createsong(tags, sig, fpath)
    else:
        logger.error('No tags found in [%s]' % fpath)

    return result


def updatesong(song, fpath):
    """Update the path if file moved
    """
    song.filename = fpath
    song.save()
    return "[U] %s\n" % song.title


def createsong(tags, sig, fpath):
    """Create a new song in db
    """

    song = Song.objects.create(artist=tags['artist'],
                               album=tags['album'],
                               title=tags['title'],
                               genre=tags['genre'],
                               score=0,
                               uniq=sig,
                               global_score=0,
                               filename=fpath)
    if hasattr(song, 'title') and song.title is not None:
        try:
            song.genre += ','.join(get_tags(song.artist, song.title))
        except:
            pass
    song.save()
    return "[I] %s\n" % song.title


def move_file(path_from, filename):
    """Move file from upload_dir to final dest

    path_from is an nginx datas
    """
    finaldir = settings.UPLOAD_DEST_DIR

    path_to = os.path.join(finaldir, filename)

    if not os.path.exists(path_to):
        shutil.copyfile(path_from, path_to)

    return path_to


def readtags(fname):
    """Read mp3 IDS Tags

    Return array with tags
    """
    datas = {}
    fields = ['album', 'artist', 'title', 'genre', 'date', 'tracknumber',
              'year']
    muts = mutagen.File(fname, easy=True)
    for fld in fields:
        if fld in muts:
            data = muts[fld]
            datas[fld] = data[0]
        else:
            datas[fld] = ''

    return datas


def mp3ogg(fname):
    """
    Encode mp3 files to ogg vorbis
    """
    logger = logging.getLogger('calorine')
    oggname = "%s.ogg" % fname[:-4]
    logger.info("encode %s" % fname)
    logger.info(" %s" % __name__)

    datas = readtags(fname)
    mpg = subprocess.Popen([settings.MPG123,
                            "-w",
                            "-",
                            fname],
                           stdout=subprocess.PIPE)

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
        ogg = subprocess.Popen(command,
                               stdin=mpg.stdout,
                               stdout=subprocess.PIPE)
        output = ogg.communicate()[0]
        result = oggname
    except:
        output = 'error inmp3ogg'
        result = None

    logger.debug(output)

    if result:
        os.unlink(fname)

    return result


def mp4ogg(fname):
    """
    Encode mp4 files to ogg vorbis
    """
    logger = logging.getLogger('calorine')
    logger.info("(mp4ogg) encode %s" % fname)
    oggname = "%s.oga" % fname[:-4]

    try:
        subprocess.call([settings.FFMPEG2THEORA, fname])
        result = oggname
    except:
        result = None

    if result:
        os.unlink(fname)

    return result


def recode(fname, content_type):
    """Recode files
    """
    result = None

    # if content_type == 'audio/mpeg':
    #     result = mp3ogg(fname)

    # if content_type == 'audio/mp4':
    #     result = mp4ogg(fname)

    if fname.endswith('.mp3'):
        result = mp3ogg(fname)

    if fname.endswith('.m4a'):
        result = mp4ogg(fname)

    return result
