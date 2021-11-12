# -*- coding: utf-8 -*-

'''
views.py

Created on  {% now "Y-m-d" %}

@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
import json
from ifxmail.client import send
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from ifxmail.client import FieldErrorsException
from ifxmail.client.views import messages, readUpdateOrDeleteMessage, mailings, readMailing
from ifxuser.models import USER_EDITABLE_PERSON_FIELDS, ADMIN_EDITABLE_PERSON_FIELDS
from ifxuser.nanites import updateOrCreateIfxUser
from ifxuser.views import get_ifxapp_nanite_login as ifxuser_get_ifxapp_nanite_login
from ifxuser.views import get_location_info as ifxuser_get_location_info
from ifxuser.views import get_contact_list as ifxuser_get_contact_list
from nanites.client import API as NanitesAPI
from hers.permissions import AdminOrOwner, AdminPermission
from hers import roles as Roles
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# Import views from ifxmail.client after aaron pushes the changes
# # Add adminonly permission layer

logger = logging.getLogger(__name__)

def get_remote_user_auth_token(request):
    '''
    Return the user token for subsequent javascript calls
    '''
    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        logger.error('Token not found for user %s', request.user)
        return JsonResponse({'error': 'User record for %s is not complete- missing token.' % str(request.user)}, status=401)

    if not request.user.is_active:
        logger.error('User %s is not active', request.user.username)
        return JsonResponse({'error': 'User is inactive.'}, status=401)

    return JsonResponse({
        'token': str(token),
        'is_staff': request.user.is_staff is True,
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'groups': [g.name for g in request.user.groups.all()]
    })


@permission_classes((AdminPermission,))
def ifx_messages(request):
    return messages(request)


@permission_classes((AdminPermission,))
def ifx_read_update_or_delete_message(request, pk):
    '''
    message operations with a pk
    '''
    return readUpdateOrDeleteMessage(request, pk)


@permission_classes((AdminPermission,))
def ifx_mailings(request):
    return mailings(request)


@permission_classes((AdminPermission,))
def ifx_read_mailing(request, pk):
    return readMailing(request, pk)


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
        cclist = []
        if ccstr:
            cclist = ccstr.split(',')
        bcclist = []
        if bccstr:
            bcclist = bccstr.split(',')
        send(
            to=tostr,
            fromaddr=fromstr,
            ifxmessage=ifxmessage,
            subject=subject,
            message=message,
            field_errors=True,
            cclist=cclist,
            bcclist=bcclist,
        )
        msg = 'Successfully sent mailing.'
        status_code = HTTP_200_OK
        data = {'message': msg}
    except FieldErrorsException as e:
        logger.exception(e)
        data = e.field_errors
        status_code = e.status
    return Response(data=data, status=status_code)

@api_view(['GET'])
def mock_error(request, pk=None):
    '''
    Return a mock error response object
    '''
    status_code = pk if pk else 401
    data = {'error': f"This error has been mocked. It has the status code: {status_code}. User is: {request.user}"}
    return JsonResponse(data=data, status=status_code)


@permission_classes((AdminOrOwner,))
def get_ifxapp_nanite_login(request):
    '''
    Get a nanite login by username
    '''
    return ifxuser_get_ifxapp_nanite_login(request)


@api_view(['POST'])
@permission_classes((AdminOrOwner,))
def update_person(request):
    '''
    Update a user by updating Nanites and syncing.  Reset group membership.
    Only changes the fields in the user or admin editable lists.
    '''

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError as e:
        logger.exception(e)
        return Response(data={'error': 'Cannot parse request body'}, status=status.HTTP_400_BAD_REQUEST)

    if not data:
        return Response(data={'error': 'Empty request'}, status=status.HTTP_400_BAD_REQUEST)

    # Pop off the non-person fields
    print(data)

    try:
        username = data.pop('username')
        is_active = data.pop('is_active')
        group_names = data.pop('groups', [])
    except Exception as e:
        logger.exception(e)
        return Response(data={'error': 'Missing values in payload %s' % str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Update the nanites person record and sync
    try:
        person_data = NanitesAPI.readPerson(ifxid=data['ifxid']).to_dict()

        fieldlist = USER_EDITABLE_PERSON_FIELDS
        if Roles.userIsAdmin(request.user):
            fieldlist = ADMIN_EDITABLE_PERSON_FIELDS

        for field in fieldlist:
            person_data[field] = data[field]

        # Catch changes to is_active as a modification to the login
        if Roles.userIsAdmin(request.user):
            for i, login in enumerate(person_data['logins']):
                if login['application'] == settings.IFX_APP['name']:
                    if is_active is not None and login['is_enabled'] != is_active:
                        person_data['logins'][i]['is_enabled'] = is_active

        NanitesAPI.updatePerson(**person_data)

    except Exception as e:
        logger.error('Error updating user %s', username)
        logger.exception(e)
        if hasattr(e, 'body'):
            try:
                # pylint: disable=no-member
                error_dict = json.loads(e.body)
                return Response(data=error_dict, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except json.JSONDecodeError:
                pass
        msg = 'Unable to update Person data (first name, last name, etc): %s' % str(e)
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if 'not authorized' in str(e).lower():
            error_status = status.HTTP_401_UNAUTHORIZED
        return Response(data={'error': msg}, status=error_status)

    try:
        user = get_user_model().objects.get(username=username)
        updateOrCreateIfxUser(ifxuser=user, login=settings.IFX_APP['name'], username=username)
    except Exception as e:
        logger.exception(e)
        return Response(
            data={
                'error': 'Person / Login data was updated but synchronization failed: %s' % str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    try:
        groups = Group.objects.filter(name__in=group_names)
        user.groups.set(groups)
    except Exception as e:
        logger.exception(e)
        return Response(data={'error': 'Unable to set user groups to %s: %s' % (', '.join(group_names), str(e))})

    return Response()


def get_location_info(request):
    '''
    Address location information
    '''
    return ifxuser_get_location_info(request)


@permission_classes((AdminPermission, ))
def get_contact_list(request):
    '''
    Contact list
    '''
    return ifxuser_get_contact_list(request)
