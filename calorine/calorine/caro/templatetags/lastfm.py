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
from django import template
from calorine.utils.lastfm import get_picture
from calorine.caro.utils import store_image
from django.core.cache import cache
from django.template.defaultfilters import slugify
register = template.Library()


def picture(song):
    """
    Return a picture of the album containing this song
    """
    if song.cover == '' or song.cover is None:

        key = 'song_image_{}_{}'.format(slugify(song.artist),
                                        slugify(song.title))

        if cache.get(key):
            pict = cache.get(key)
        else:
            pict = get_picture(song.artist, song.title)
            if pict:                
                song.cover = pict
                song.save()
                #store_image(pict)
            else:
                pict = "http://lorempixel.com/64/64/animals/"
        cache.set(key, pict)
        return {
            'picture': pict
            }
    else:
        return { 'picture': song.cover }

register.inclusion_tag('picture.html')(picture)
