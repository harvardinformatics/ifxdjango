# -*- coding: utf-8 -*-

'''
Apply the dev data from the listed fixtures
'''
from django.core.management.base import BaseCommand
from django.core.management import call_command


FIXTURES = [
    'ifxuser',
    'authtoken',
    'authgroup'
]


class Command(BaseCommand):
    '''
    Apply data from initDev and create a fixture out of it
    '''
    help = 'Applies the data in the fixtures %s. Usage:\n./manage.py applyDevData' % ', '.join(FIXTURES)

    def handle(self, *args, **kwargs):
        call_command('loaddata', *FIXTURES)
