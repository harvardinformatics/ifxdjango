# -*- coding: utf-8 -*-

'''
roles for {{project_name}}

Created on  2020-09-16

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2020 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.conf import settings


def userIsAdmin(user):
    '''
    Determine if a user is an admin by checking for admin group
    '''
    return user.groups.filter(name=settings.GROUPS.ADMIN_GROUP_NAME).exists()
