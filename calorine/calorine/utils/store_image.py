# -*- coding: utf-8 -*-  pylint: disable-msg=R0801
#
# Copyright (c) 2012 Yohann Gabory <yohann@gabory.fr>
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
from django.core.cache import cache
from requests import get
from StringIO import StringIO
from django.template.defaultfilters import slugify
from PIL import Image


def store_image(url):
    """Store image in cache
    """
    key = slugify(url)
    raw = get(url, timeout=5)
    img = Image.open(StringIO(raw.content))
    cache.set("%s_data" % key, img.tostring())
    cache.set("%s_mode" % key, img.mode)
    cache.set("%s_size" % key, img.size)
    print key
    return key
