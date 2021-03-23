# -*- coding: utf-8 -*-

'''
Permissions classes for views
'''
import logging
from rest_framework import permissions
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

