"""
DewarRequestProcessor, processes helium dewar requests.

@author: Meghan Correa
@copyright: 2020 The Presidents and Fellows of Harvard College. All rights reserved.
@license: GPL v2.0
@contact: mportermahoney@g.harvard.edu
"""
import logging
from collections import OrderedDict
from django.contrib.auth.models import Group
from django.conf import settings
from ifxrequest.processor import BaseAccountRequestProcessor


logger = logging.getLogger(__name__)


class AccountRequestProcessor(BaseAccountRequestProcessor):
    '''
    {{project_name}} account request handler
    '''

    def getLoginsForAccessRequests(self, request):
        '''
        Return Logins needed for successful requests
        '''
        login_data = []
        for role, current_status in request.access_requests.items():
            if current_status == 'Request':
                if role == '{{project_name}}_user':
                    login_data.append(
                        {
                            'application': 'Harvard Key',
                            'username': request.harvard_key,
                            'role': 'user',
                        },
                    )
                    login_data.append(
                        {
                            'application': '{{project_name}}',
                            'username': request.harvard_key,
                            'role': role,
                        },
                    )
        return login_data
