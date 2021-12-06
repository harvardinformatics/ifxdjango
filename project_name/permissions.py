# -*- coding: utf-8 -*-

'''
Permissions classes for views

Created on  {% now "Y-m-d" %}
'''

import json
import logging
from rest_framework import permissions
from ifxuser.permissions import UserViewSetPermissions
from {{project_name}} import roles as Roles

logger = logging.getLogger(__name__)

class AdminPermission(permissions.IsAuthenticated):
    '''
    User must be an admin
    '''
    def has_permission(self, request, view):
        result = Roles.userIsAdmin(request.user)
        logger.debug('user is admin? %s', str(result))
        return result


class AdminOrOwner(permissions.IsAuthenticated):
    '''
    User must be an Admin or the person being updated
    '''
    def has_permission(self, request, view):
        # Find username in GET, POST, or body data
        username = None
        if request.method == 'GET':
            username = request.GET.get('username')
        elif request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                username = data.get('username')
            except json.JSONDecodeError:
                pass
        return (Roles.userIsAdmin(request.user) or request.user.username == username) and super().has_permission(request, view)


class {{project_name|title}}UserViewSetPermissions(UserViewSetPermissions):
    '''
    Use local userIsAdmin
    '''
    def user_is_admin(self, user):
        '''
        How admin is determined
        '''
        return Roles.userIsAdmin(user)
