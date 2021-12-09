# -*- coding: utf-8 -*-
'''
views for {{project_name}}.request

Created on  {% now "Y-m-d" %}

@copyright: 2021 The President and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from rest_framework.decorators import permission_classes
from rest_framework import status, permissions
from ifxrequest.views import get_request_list as ifxrequest_get_request_list
from ifxrequest.views import get_valid_processor_states as ifxrequest_get_valid_processor_states
from ifxrequest.views import set_request_state as ifxrequest_set_request_state
from ifxrequest.views import onboard_requests as ifxrequest_onboard_requests
from ifxrequest.views import update_account_request as ifxrequest_update_account_request
from {{project_name}}.permissions import AdminPermission


@permission_classes((AdminPermission,))
def get_request_list(request):
    '''
    Return request list data
    '''
    return ifxrequest_get_request_list(request)


@permission_classes((AdminPermission,))
def get_valid_processor_states(request):
    '''
    Return valid processor states
    '''
    return ifxrequest_get_valid_processor_states(request)


@permission_classes((AdminPermission, ))
def set_request_state(request):
    '''
    Set request state
    '''
    return ifxrequest_set_request_state(request)


@permission_classes((AdminPermission, ))
def onboard_requests(request, pk=None):
    '''
    Get or update onboard requests
    '''
    return ifxrequest_onboard_requests(request, pk)


@permission_classes((permissions.IsAuthenticated,))
def update_account_request(request, pk=None):
    '''
    Allow onboarding tool to update account request information
    '''
    return ifxrequest_update_account_request(request, pk)
