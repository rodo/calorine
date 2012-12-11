from django.core.management.base import BaseCommand, CommandError
from calorine.caro.models import PlaylistEntry


class Command(BaseCommand):
    help = 'Remove from db unonw on disk song'

    def handle(self, *args, **options):
        PlaylistEntry.objects.filter().delete()

        self.stdout.write('Successfully empty playlist\n')
