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
from rest_framework.decorators import api_view, permission_classes
from ifxuser.views import get_location_info as ifxuser_get_location_info
from ifxuser.views import get_contact_list as ifxuser_get_contact_list
from ifxmail.client import send
from ifxmail.client.views import messages, mailings
from {{project_name}} import permissions

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


# TODO: add authorization
def ifx_messages(request):
    return messages(request)

# TODO: add authorization
def ifx_mailings(request):
    return mailings(request)

@api_view(['POST',])
def send_ifx_mailing(request):
    fromstr = request.data.get('fromstr')
    tostr = request.data.get('tostr')
    ccstr = request.data.get('ccstr')
    bccstr = request.data.get('bccstr')
    message = request.data.get('message', None)
    subject = request.data.get('subject', None)
    ifxmessage = request.data.get('ifxmessage', None)

    try:
        # to, fromaddr, subject=None, message=None, cclist=[], bcclist=[], replyto=None, ifxmessage=None, data=None, timeout=5
        send(
            to=tostr,
            fromaddr=fromstr,
            ifxmessage=ifxmessage,
            subject=subject,
            message=message,
            field_errors=True
        )
        msg = 'Successfully sent mailing.'
        status = HTTP_200_OK
        data = {'message': msg}
    except FieldErrorsException as e:
        logger.exception(e)
        data = e.field_errors
        status = e.status
    return Response(data=data, status=status)


def get_location_info(request):
    '''
    Address location information
    '''
    return ifxuser_get_location_info(request)


@permission_classes((permissions.AdminPermission, ))
def get_contact_list(request):
    '''
    Contact list
    '''
    return ifxuser_get_contact_list(request)
