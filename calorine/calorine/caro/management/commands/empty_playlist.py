from django.core.management.base import BaseCommand, CommandError
from calorine.caro.models import PlaylistEntry


class Command(BaseCommand):
    help = 'Remove from db unonw on disk song'

    def handle(self, *args, **options):
        try:
            PlaylistEntry.objects.filter().delete()
        except Song.DoesNotExist:
            raise CommandError('Unable to empty playlist')

        self.stdout.write('Successfully empty playlist\n')
