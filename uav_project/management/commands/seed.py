# myapp/management/commands/seed.py
from django.core.management.base import BaseCommand

from uav_project.utils.helpers import create_initial_data


class Command(BaseCommand):
    help = "Create initial data"

    def handle(self, *args, **options):
        create_initial_data()
        self.stdout.write(self.style.SUCCESS("Successfully seeded database"))
