import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command

with open('all_data.json', 'w', encoding='utf-8') as output_file:
    call_command('dumpdata', stdout=output_file)
