# -*- coding: utf-8 -*-

'''
nanites init

Initializes data for a new system.  To be used in both prod and dev.

Uses get_or_create so that it can be run when partial data exists

Created on  2019-12-23

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''

from collections import OrderedDict


def migrate(apps, schema_editor):
    '''
    Set data via migration
    '''
    initIfxId(apps.get_model('nanites', 'IfxId'))
    initSources(apps.get_model('nanites', 'Source'))
    initApplications(apps.get_model('nanites', 'Application'))
    initUsers(apps.get_model('auth', 'User'))

def main():
    '''
    If called directly, rather than as a migration
    '''
    from nanites import models
    from django.contrib.auth.models import User
    initIfxId(models.IfxId)

    modelsForFixture = OrderedDict()
    modelsForFixture['nanites.Source'] = initSources(models.Source)
    modelsForFixture['nanites.Application'] = initApplications(models.Application)
    modelsForFixture['auth.User'] = initUsers(User)

    return modelsForFixture


def initIfxId(cls):
    '''
    Initialize the ifxid counter if it doesn't have any records yet
    '''
    if not cls.objects.all():
        ifxid = cls(nextval='0000000000')
        ifxid.save()

def initSources(cls):
    '''
    Initialize Person Sources
    '''
    pks = []
    sources = [
        {
            'name': 'Manual Entry',
            'description': 'Manually entered data',
        }
    ]
    for sourcedata in sources:
        (obj, created) = cls.objects.get_or_create(**sourcedata)
        pks.append(obj.pk)

    return pks


def initApplications(cls):
    '''
    Initialize the Application instances
    '''
    pks = []
    applications = [
        {
            'name': 'CNS Admin Intranet',
            'fields': '__all__',
            'auth': 'CNS Staff',
        },
        {
            'name': 'CNS User Portal',
            'fields': '__all__',
            'auth': 'CNS User',
        },
        {
            'name': 'CNS User Admin Intranet',
            'fields': 'first_name,last_name,full_name,ifxid,primary_email,primary_affiliation',
            'auth': 'CNS User Admin',
        },
        {
            'name': 'Harvard Key',
            'fields': 'None',
            'auth': 'Harvard Key'
        },
        {
            'name': 'nice',
            'auth': 'Harvard Key',
            'fields': '__all__',
        },
        {
            'name': 'p3',
            'auth': 'RC',
            'fields': '__all__',
        },
        {
            'name': 'Research Computing AD',
            'auth': 'RC',
            'fields': '__all__',
        }
    ]
    for appdata in applications:
        (obj, created) = cls.objects.get_or_create(**appdata)
        pks.append(obj.pk)

    return pks


def initUsers(cls):
    '''
    Initialize application users.  Do NOT set tokens here.
    '''
    pks = []
    users = [
        {
            'username': 'nice',
            'first_name': 'NICE',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'p3',
            'first_name': 'p3',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'cns',
            'first_name': 'CNS',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'cas',
            'first_name': 'CAS',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'pubs',
            'first_name': 'PUBS',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'ifxonboard',
            'first_name': 'IfxOnboard',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
        {
            'username': 'portal',
            'first_name': 'Portal',
            'last_name': 'Application',
            'is_active': True,
            'is_superuser': True,
        },
    ]

    for userdata in users:
        (obj, created) = cls.objects.get_or_create(**userdata)
        pks.append(obj.pk)

    return pks

if __name__ == '__main__':
    main()