# -*- coding: utf-8 -*-

'''
roles for {{project_name}}

Created on  {% now "Y-m-d" %}

@copyright: 2021 The President and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.conf import settings


def userIsAdmin(user):
    '''
    Determine if a user is an admin by checking for admin group
    '''
    return user.groups.filter(name=settings.GROUPS.ADMIN_GROUP_NAME).exists()
