from django import template
from calorine.utils.lastfm import get_picture
register = template.Library()


def picture(song):
    """
    Return a picture of the album containing this song
    """
    picture = get_picture(song.artist, song.title)
    return {
        'picture': picture
    }

register.inclusion_tag('picture.html')(picture)
