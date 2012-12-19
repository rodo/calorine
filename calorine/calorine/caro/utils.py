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
import sys
import hashlib
import mutagen
from calorine.caro.models import Logs
from django.core.cache import cache
from PIL import Image
from requests import get
from StringIO import StringIO
from django.template.defaultfilters import slugify


def store_image(url):
    """Store image in cache
    """
    key = slugify(url)
    raw = get(url, timeout=5)
    img = Image.open(StringIO(raw.content))
    cache.set("%s_data" % key, img.tostring())
    cache.set("%s_mode" % key, img.mode)
    cache.set("%s_size" % key, img.size)
    return key


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
        pass

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
