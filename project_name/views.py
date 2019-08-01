# -*- coding: utf-8 -*-

'''
views.py

Created on  2019-09-18

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
from rest_framework.authtoken.models import Token
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def get_remote_user_auth_token(request):
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        return JsonResponse({'error': 'User record for %s is not complete- missing token.' % str(request.user)}, status=401)

    if not request.user.is_active:
        logger.info('User %s is not active', request.user.username)
        return JsonResponse({'error': 'User is inactive.'}, status=401)

    return JsonResponse({
        'token': str(token),
        'is_staff': request.user.is_staff is True,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'groups': [g.name for g in request.user.groups.all()]
    })
