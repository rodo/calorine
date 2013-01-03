# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2013 Rodolphe Quiédeville <rodolphe@quiedeville.org>
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
The converters defined in Mime Model
"""

import logging
from calorine.caro.utils import mp3ogg
from calorine.caro.utils import mp4ogg

logger = logging.getLogger(__name__)


def convert_mp3(fpath, upload):
    """Convert mp3 files
    """
    logger.info("(convert_upload) [%s] as [%s]" % (fpath,
                                                   upload.content_type))

    oggname = mp3ogg(fpath)
    upload.status = 'uploaded'
    upload.save()
    return oggname


def convert_mp4(fpath, upload):
    """Convert mp4 files
    """
    logger.info("(convert_upload) [%s] as [%s]" % (fpath,
                                                   upload.content_type))

    oggname = mp4ogg(fpath)
    upload.status = 'uploaded'
    upload.save()
    return oggname


def convert_none(fpath, upload):
    """Do nothing for ogg files
    """
    logger.info("(convert_none) [%s] as [%s]" % (fpath,
                                                 upload.content_type))
    upload.status = 'uploaded'
    upload.save()
    return fpath
