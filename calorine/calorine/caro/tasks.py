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
from celery.task import task
from calorine.caro.models import Upload
from calorine.caro.utils import move_file
from django.shortcuts import get_object_or_404
from time import sleep
from calorine.caro.utils import importsong
from calorine.caro.utils import get_tags
import syslog
import json
import requests

@task()
def import_upload(uuid):
    """Import uploaded files
    """

    url = 'http://127.0.0.1:81/progress'

    upload = get_object_or_404(Upload, uuid=uuid)

    params = {'X-Progress-ID': uuid}

    state = 'starting'
    counter = 1

    while (counter < 10) and (state != 'done'):
        counter += 1
        prg = requests.get(url, params=params, timeout=1).content
        datas = json.loads(prg)

        syslog.syslog('state: %s for %s' % (datas['state'], uuid))
        if datas['state'] == 'done':
            state = 'done'
            newpath = move_file(upload.path, upload.filename)
            importsong(newpath)
        sleep(1)

    return datas


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
