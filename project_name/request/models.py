# -*- coding: utf-8 -*-

'''
models for {{project_name}} request

Created on  {% now "Y-m-d" %}

@copyright: 2020 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
from django.db.models.signals import post_save
from ifxrequest.models import BaseAccountRequest, AccountRequestManager, post_save_request_init


logger = logging.getLogger(__name__)


class AccountRequest(BaseAccountRequest):
    '''
    Account requests for {{project_name}}
    '''

    objects = AccountRequestManager()

    class Meta:
        '''
        meta
        '''
        proxy = True

    @property
    def harvard_key(self):
        '''
        Property getter
        '''
        result = self.getDataField('harvard_key')
        if not result:
            harvard_key_login = self.getLogin('Harvard Key')
            if harvard_key_login:
                result = harvard_key_login.username
        return result

    @harvard_key.setter
    def harvard_key(self, harvard_key):
        self.setDataField('harvard_key', harvard_key)


post_save.connect(post_save_request_init, sender=AccountRequest)
