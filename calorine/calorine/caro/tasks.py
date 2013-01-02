# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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
The tasks
"""
from django.conf import settings
from django.shortcuts import get_object_or_404
from time import sleep
import json
import requests
import logging
from celery.task import task
from calorine.caro.models import Upload
from calorine.caro.utils import move_file
from calorine.caro.utils import recode
from calorine.caro.utils import importsong
from calorine.caro.utils import get_tags


@task()
def import_upload(uuid):
    """Import uploaded files
    """
    url = settings.NGINX_PROGRESS_URL
    
    upload = get_object_or_404(Upload, uuid=uuid)

    params = {'X-Progress-ID': uuid}

    state = 'starting'
    counter = 1

    while (counter < 480) and (state != 'done'):
        counter += 1
        prg = requests.get(url, params=params, timeout=1).content
        datas = json.loads(prg)

        if datas['state'] == 'done':
            state = 'done'
            store_upload(upload)
        sleep(1)

    return datas


def store_upload(upload):
    """Store the file uploaded
    """
    oggname = None
    newpath = move_file(upload.path, upload.filename)
    if upload.content_type == 'audio/mpeg':
        oggname = convert_upload(newpath, upload)
    elif upload.content_type == 'audio/mp3':
        oggname = convert_upload(newpath, upload)
    elif upload.content_type == 'video/ogg':
        oggname = newpath
    else:
        logger = logging.getLogger(__name__)
        logger.info("(store_upload) wrong type for %s %s" % (newpath,
                                                             upload.content_type))
        upload.status = 'bad format'
        upload.save()

    if oggname is not None:
        importsong(oggname)
        upload.status = 'done'
        upload.save()
    return 0


def convert_upload(newpath, upload):
    """Convert non ogg files
    """
    oggname = recode(newpath, upload.content_type)
    upload.status = 'uploaded'
    upload.save()
    return oggname

@task()
def addgenre(song):
    """Import uploaded files
    """
    try:
        song.genre += ','.join(get_tags(song.artist, song.title))
        song.save()
    except:
        pass

    return 0
