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
from ifxrequest import views as ifxrequest_views
from {{project_name}}.permissions import AdminPermission


@permission_classes((AdminPermission,))
def get_request_list(request):
    '''
    Return request list data
    '''
    return ifxrequest_views.get_request_list(request)


@permission_classes((AdminPermission,))
def get_valid_processor_states(request):
    '''
    Return valid processor states
    '''
    return ifxrequest_views.et_valid_processor_states(request)


@permission_classes((AdminPermission, ))
def set_request_state(request):
    '''
    Set request state
    '''
    return ifxrequest_views.set_request_state(request)


@permission_classes((AdminPermission, ))
def onboard_requests(request, pk=None):
    '''
    Get or update onboard requests
    '''
    return ifxrequest_views.onboard_requests(request, pk)


@permission_classes((permissions.IsAuthenticated,))
def update_account_request(request, pk=None):
    '''
    Allow onboarding tool to update account request information
    '''
    return ifxrequest_views.update_account_request(request, pk)
