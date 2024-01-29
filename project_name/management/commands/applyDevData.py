# -*- coding: utf-8 -*-

'''
Apply the dev data from the listed fixtures
'''
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

# Additional fixtures other than auth and authtoken
FIXTURES = []
DEV_USERNAMES = [
    'mhamilton', 'gvrossum', 'alanturing', 'jvneumann', 'jobs', 'woz', 'dknuth', 'ghopper','veradmin', 'dritchie', 'adalovelace', 'bstroustrup'
]


class Command(BaseCommand):
    '''
    Apply data from fixtures over top of production if needed
    '''
    help = 'Applies the data in the fixtures ifxuser, authtoken, %s. Resets tokens if they exist. Usage:\n./manage.py applyDevData' % ', '.join(FIXTURES)

    def handle(self, *args, **kwargs):
        # Reset all tokens if there are any users
        for user in get_user_model().objects.all():
            try:
                Token.objects.filter(user=user).delete()
                if (user.last_name and user.last_name.lower() != 'application') and user.username not in DEV_USERNAMES:
                    Token.objects.create(user=user)
            except Exception as e:
                print(f'Error resetting token for {user}: {e}')
        # Load auth
        call_command('loaddata', '/app/{{project_name}}/fixtures/authgroup.json')
        # Load users
        call_command('loaddata', '/app/{{project_name}}/fixtures/ifxuser.json')
        # Load tokens
        call_command('loaddata', '/app/{{project_name}}/fixtures/authtoken.json')

        # Load remaining fixtures
        for fixture in FIXTURES:
            call_command('loaddata', fixture)
