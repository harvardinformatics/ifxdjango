# -*- coding: utf-8 -*-

'''
Ensure that product_accounts are returned from UserViewSet

Created on  {% now "Y-m-d" %}

@copyright: 2021 The President and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework import status
from ifxuser.models import IfxUser
from ifxbilling.models import UserProductAccount, Account, Product
from {{project_name}}.test import data

class TestUserAccounts(APITestCase):
    '''
    Test User accounts
    '''
    def setUp(self):
        '''
        setup
        '''
        data.clearTestData()
        Token.objects.all().delete()
        self.superuser = get_user_model().objects.create_superuser('john', 'john@snow.com', 'johnpassword')
        group, created = Group.objects.get_or_create(name=settings.GROUPS.ADMIN_GROUP_NAME)
        self.superuser.groups.add(group)
        self.login('john', 'johnpassword')

    def login(self, username, password):
        '''
        Set the self.client to the specified username, password and set token
        '''
        user = get_user_model().objects.get(username=username)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token(user=user)
            token.save()
        self.client.login(username=username, password=password)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def testGetUserWithUserProductAccount(self):
        '''
        Ensure that a user with a user_product_account returns the data
        '''
        data.init()
        PRODUCT_NAME = 'Liquid Nitrogen'
        ACCOUNT_NAME = 'Test expense code'
        USERNAME = 'sslurpiston'

        product = Product.objects.get(product_name=PRODUCT_NAME)
        account = Account.objects.get(name=ACCOUNT_NAME)
        user = IfxUser.objects.get(username=USERNAME)
        UserProductAccount.objects.create(product=product, user=user, account=account)

        url = reverse('user-detail', kwargs={'pk': user.id})

        response = self.client.get(url, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
        user_data = response.data
        self.assertTrue(len(user_data['product_accounts']) == 1, f'Incorrect number of user product accounts {user_data}')
        self.assertTrue(user_data['product_accounts'][0]['product']['product_name'] == PRODUCT_NAME, f'Incorrect product name {user_data["product_accounts"]}')
        self.assertTrue(user_data['product_accounts'][0]['is_valid'], f'Incorrect product account valid status {user_data["product_accounts"]}')
        self.assertTrue(user_data['product_accounts'][0]['percent'] == 100, f'Incorrect product account percent {user_data["product_accounts"]}')
