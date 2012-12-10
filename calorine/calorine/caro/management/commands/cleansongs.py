from django.core.management.base import BaseCommand, CommandError
from calorine.caro.models import Song

class Command(BaseCommand):
    help = 'Remove from db unonw on disk song'

    def handle(self, *args, **options):
        try:
            song = Song.objects.filter(score=-1000).delete()
        except Song.DoesNotExist:
            raise CommandError('Unable to remove song from db')

        self.stdout.write('Successfully clean database\n')
