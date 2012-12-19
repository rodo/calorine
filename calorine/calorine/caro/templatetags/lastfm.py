from django import template
from calorine.utils.lastfm import get_picture
from django.core.cache import cache
from django.template.defaultfilters import slugify

register = template.Library()


def picture(song):
    """
    Return a picture of the album containing this song
    """
    key = 'song_image_{}_{}'.format(slugify(song.artist),
                                    slugify(song.title))
    if cache.get(key):
        pict = cache.get(key)
    else:
        pict = get_picture(song.artist, song.title)
        if pict:
            cache.set(key, pict)
        else:
            cache.set(key, "no pic")
    return {
        'picture': pict
    }

register.inclusion_tag('picture.html')(pict)
