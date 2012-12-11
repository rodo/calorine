"""
Add a random song in playlist
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc
from datetime import datetime
from random import sample
from calorine.caro.models import PlaylistEntry
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Add a random song to playlist'

    def handle(self, *args, **options):
        try:
            count = Song.objects.filter(family=0).count()
            rand_id = sample(xrange(1, count), 1)[0]
            song = Song.objects.all()[rand_id]
            PlaylistEntry.objects.create(
                song=song,
                date_add=datetime.utcnow().replace(tzinfo=utc),
                score=0)

        except Song.DoesNotExist:
            raise CommandError('Unable to find a song')

        self.stdout.write('Add %s %s %s to playlist\n' % (song.artist,
                                                          song.title,
                                                          song.album))
