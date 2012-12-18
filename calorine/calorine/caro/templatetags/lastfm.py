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
        picture = cache.get(key)
    else:
        picture = get_picture(song.artist, song.title)
        if picture:
            cache.set(key, picture)
        else:
            cache.set(key, "picture")
    return {
        'picture': picture
    }

register.inclusion_tag('picture.html')(picture)
