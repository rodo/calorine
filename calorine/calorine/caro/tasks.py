# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
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
The tasks
"""
from time import sleep
import json
import requests
import logging
from celery.task import task
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import get_object_or_404
from calorine.caro.models import Upload
from calorine.caro.models import Mime
from calorine.caro.utils import move_file
from calorine.caro.utils import importsong
from calorine.caro.utils import get_tags
import calorine.caro.converters

logger = logging.getLogger(__name__)


@task()
def mail_uploader(user):
    """Send an email at the end of upload
    """
    email = user.email_user

    logger.debug("send email to [%s]" % (email))
    msg = "Thanks,\n\nYou upload is now finish\n"
    send_mail('Upload',
              msg,
              settings.EMAIL_FROM,
              [email])


@task()
def import_upload(uuid, maxtime=480, url=settings.NGINX_PROGRESS_URL):
    """Import uploaded files

    maxtime : number in second to wait max
    """
    state = 'starting'
    counter = 1

    datas = {'state': 'starting'}

    while (counter < maxtime) and (state != 'done'):
        counter += 1
        datas = get_upload_status(uuid, url)

        if datas['state'] == 'done':
            state = 'done'
            upload = get_object_or_404(Upload, uuid=uuid)
            store_upload(upload)
        sleep(1)

    return datas


def get_upload_status(uuid, url=settings.NGINX_PROGRESS_URL):
    """Retrieve upload status from nginx

    Return : dict
    """
    status = {'state': 'starting'}
    params = {'X-Progress-ID': uuid}
    logger.debug("Connect on nginx progress url [%s]" % (url))
    try:
        datas = requests.get(url, params=params, timeout=1).content
        status = json.loads(datas)
    except requests.ConnectionError:
        logger.info("Cant't connect on nginx progress url [%s]" % (url))

    return status


def store_upload(upload):
    """Store the file uploaded
    """
    oggname = None
    newpath = move_file(upload.path, upload.filename)
    try:
        mime = Mime.objects.get(name=upload.content_type)
        logger.info("will use %s() to convert %s" % (mime.function,
                                                     mime.name))
    except ObjectDoesNotExist:
        logger.error("(%s) wrong mime/type for %s %s" % ('store_upload',
                                                         newpath,
                                                         upload.content_type))
        upload.status = 'bad format'
        upload.save()
        return 1

    convert = getattr(calorine.caro.converters, mime.function)
    oggname = convert(newpath, upload)

    if oggname is None:
        return 2
    else:
        importsong(oggname)
        upload.status = 'done'
        upload.save()
        mail_uploader.delay(upload.user)
        return 0


@task()
def addgenre(song):
    """Import uploaded files
    """
    try:
        song.genre += ','.join(get_tags(song.artist, song.title))
        song.save()
        return 0
    except:
        return 1
