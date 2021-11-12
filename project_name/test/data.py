# -*- coding: utf-8 -*-

'''
Test data {{project_name}}

Created on  {% now "Y-m-d" %}

@copyright: 2021 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from copy import deepcopy
from rest_framework.reverse import reverse
from ifxuser.models import Organization, IfxUser, IfxUserAffiliation
from ifxbilling.models import Product, Facility, Account, Rate

FACILITIES = [
]

ORGS = [
    {
        'name': 'Kitzmiller Lab',
        'rank': 'lab',
        'org_tree': 'Harvard',
    },
    {
        'name': 'Nobody Lab',
        'rank': 'lab',
        'org_tree': 'Harvard',
    }
]

ACCOUNTS = [
    {
        'name': 'Test expense code',
        'account_type': 'Expense Code',
        'code': '370-00000-0000-000000-000000-0000-00000',
        'organization': 'Kitzmiller Lab',
    },
]

USERS = [
    {
        'username': 'sslurpiston',
        'first_name': 'Slurpy',
        'last_name': 'Slurpiston',
        'full_name': 'Slurpy Slurpiston',
        'email': 'sslurpiston@gmail.com',
        'ifxid': 'IFXIDX0000000001'
    },
    {
        'username': 'dderpiston',
        'first_name': 'Derpy',
        'last_name': 'Derpiston',
        'full_name': 'Derpy Derpiston',
        'email': 'dderpiston@gmail.com',
        'ifxid': 'IFXIDX0000000002'
    },
]

PRODUCTS = [
]


def clearTestData():
    """
    Clean up before and after
    """

    Organization.objects.all().delete()
    for user_data in USERS:
        try:
            IfxUser.objects.get(ifxid=user_data['ifxid']).delete()
        except IfxUser.DoesNotExist:
            pass

    try:
        IfxUser.objects.filter(username='hers').delete()
        Product.objects.all().delete()
        Account.objects.all().delete()
        Facility.objects.all().delete()
    except Exception:
        pass


def init():
    """
    Initialize organizations and users
    """
    for user_data in USERS:
        # User might be created as the logged in client
        IfxUser.objects.get_or_create(**user_data)
    for org_data in ORGS:
        Organization.objects.create(**org_data)
    for facility_data in FACILITIES:
        Facility.objects.create(**facility_data)

    org = Organization.objects.get(name='Kitzmiller Lab')
    for user in IfxUser.objects.all():
        if user.username in ('sslurpiston', 'dderpiston'):
            IfxUserAffiliation.objects.create(ifxuser=user, organization=org, role='member')
    for original_product_data in PRODUCTS:
        product_data = deepcopy(original_product_data)
        product_data['facility'] = Facility.objects.get(name=product_data.pop('facility'))
        rates_data = product_data.pop('rates')
        product = Product.objects.create(**product_data)
        for rate_data in rates_data:
            rate_data['product'] = product
            Rate.objects.create(**rate_data)

    for original_account_data in ACCOUNTS:
        account_data = deepcopy(original_account_data)
        account_data['organization'] = Organization.objects.get(name=account_data.pop('organization'))
        account = Account.objects.create(**account_data)
