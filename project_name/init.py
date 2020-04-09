# -*- coding: utf-8 -*-

'''
{{project_name}} init

Initializes data for a new system.  To be used in both prod and dev.

Uses get_or_create so that it can be run when partial data exists.
For user creation, this code uses get_user_model and the app name / model
in USER_APP_MODEL.  You should just have to change the latter if the user model
is different and ifxuser.IfxUser

Created on  2019-12-23

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.contrib.auth import get_user_model
from collections import OrderedDict

USER_APP_MODEL = 'ifxuser.IfxUser'

def migrate(apps, schema_editor):
    '''
    Set data via migration
    '''
    user_app_name, model_name = USER_APP_MODEL.split('.')
    initUsers(apps.get_model(user_app_name, model_name))

def main():
    '''
    If called directly, rather than as a migration
    '''
    # from {{project_name}} import models

    modelsForFixture = OrderedDict()
    modelsForFixture[USER_APP_MODEL] = initUsers(get_user_model())

    return modelsForFixture


def initUsers(cls):
    '''
    Initialize application users.  Do NOT set tokens here.
    '''
    pks = []
    # users = [
    #     {
    #         'username': 'nice',
    #         'first_name': 'NICE',
    #         'last_name': 'Application',
    #         'is_active': True,
    #         'is_superuser': True,
    #     },
    # ]

    # for userdata in users:
    #     (obj, created) = cls.objects.get_or_create(**userdata)
    #     pks.append(obj.pk)

    return pks

if __name__ == '__main__':
    main()