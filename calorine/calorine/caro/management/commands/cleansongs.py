from django.core.management.base import BaseCommand, CommandError
from calorine.caro.models import Song


class Command(BaseCommand):
    help = 'Remove from db unonw on disk song'

    def handle(self, *args, **options):
        count = Song.objects.filter(score=-1000).count()
        try:
            Song.objects.filter(score=-1000).delete()
        except Song.DoesNotExist:
            raise CommandError('Unable to remove song from db')
        msg = 'Successfully remove %d songs from database\n' % count
        self.stdout.write(msg)
