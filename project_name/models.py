# -*- coding: utf-8 -*-

'''
models for {{project_name}}

Created on  {% now "Y-m-d" %}

@author: Meghan Correa <mportermahoney@g.harvard.edu>
@copyright: 2021 The President and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
from django.db import models
from ifxuser.models import IfxUser


logger = logging.getLogger(__name__)

class {{project_name|title}}User(IfxUser):
    '''
    Proxy model for IfxUser.  Currently just used to permit a {{project_name}}-specific user admin.
    '''
    class Meta:
        proxy = True

