# -*- coding: utf-8 -*-

'''
Admin role

Created on  2024-01-29

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2024 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging


logger = logging.getLogger(__name__)


def has_role(user, organization=None, active_only=True):
    '''
    Does user have this role.  For admin, organization, active_only are ignored
    '''
    return user.groups.filter(name=settings.GROUPS.ADMIN_GROUP_NAME).exists()


def set_role(user, organization=None, active_only=True):
    '''
    Make user an Admin.  For admin, organization, active_only are ignored
    '''
    return user.groups.add(Group.objects.get(name=settings.GROUPS.ADMIN_GROUP_NAME))


def remove_role(user, organization=None):
    '''
    Remove user from Admin.  For admin, organization are ignored
    '''
    return user.groups.remove(Group.objects.get(name=settings.GROUPS.ADMIN_GROUP_NAME))

