
# -*- coding: utf-8 -*-

'''
Apply the dev data from initDev to the database
'''
from io import StringIO
from django.core.management.base import BaseCommand
from django.core.management import call_command
from nanites.initDev import main


class Command(BaseCommand):
    '''
    Apply data from initDev and create a fixture out of it
    '''
    help = 'Applies the data in init.py and initDev.py and returns fixture text. Usage:\n' + \
        "./manage.py applyDevData > nanites/fixtures/dev.json"

    def handle(self, *args, **kwargs):
        modelsForFixture = main()
        out = StringIO()
        for modelname, pks in modelsForFixture.items():
            call_command('dumpdata', modelname, '--pks', ','.join([str(pk) for pk in pks]), stdout=out)

        print(out.getvalue().replace('][', ','))
