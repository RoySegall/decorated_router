from django.core.management.base import BaseCommand
from decorated_router.api.api import get_decorated_classes
from os import getcwd


class Command(BaseCommand):
    help = 'Migrating data into the system'

    def handle(self, *args, **options):
        # Get the entry point instance.
        get_decorated_classes(getcwd())
