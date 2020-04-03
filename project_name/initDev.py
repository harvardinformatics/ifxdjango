# -*- coding: utf-8 -*-

'''
{{project_name}} initDev

Initializes development data for a system, include some
dev users and application tokens.

Created on  2019-12-23

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from {{project_name}}.init import main as init_production
from {{project_name}}.init import USER_APP_MODEL



def main():
    '''
    Run dev data initialization
    '''
    modelsForFixture = init_production()
    modelsForFixture[USER_APP_MODEL].extend(initUsers())
    modelsForFixture['authtoken.Token'] = initTokens()
    return modelsForFixture

def initUsers():
    '''
    Setup veradmin and application user tokens
    '''
    pks = []
    users = [
        {
            'username': 'veradmin',
            'first_name': 'Vera D.',
            'last_name': 'Min',
            'is_active': True,
            'is_superuser': True,
            'is_staff': True,
        },
    ]
    for userdata in users:
        (obj, created) = get_user_model().objects.get_or_create(**userdata)
        pks.append(obj.pk)

    return pks


def initTokens():
    '''
    Set tokens to common values
    '''
    pks = []
    tokens = [
        {
            'username': 'veradmin',
            'token': '9f822e797823b3a6d5cf2a353baf0649a012e13c',
        },
    ]
    for tokendata in tokens:
        user = get_user_model().objects.get(username=tokendata['username'])
        (obj, created) = Token.objects.get_or_create(user=user)
        Token.objects.filter(user=user).update(key=tokendata['token'])
        pks.append(obj.pk)

    return pks
