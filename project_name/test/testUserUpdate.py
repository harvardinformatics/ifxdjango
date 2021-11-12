# -*- coding: utf-8 -*-

'''
User update tests.  Copied over from ifxuser
because inheriting doesn't quite work properly

Created on  {% now "Y-m-d" %}

@copyright: 2021 The Presidents and Fellows of Harvard College.
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
from nanites.client import API as NanitesAPI
from ifxuser.test import data

class TestUserUpdate(APITestCase):
    '''
    Test User update
    '''
    def setUp(self):
        '''
        setup
        '''
        data.clear()
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

    def testCreateUserFail(self):
        '''
        Ensure that users cannot be created via POST
        '''
        data.init()
        data.syncUsers()

        user_data = {
            'username': 'uoioiu',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'alskjdf@alskdjf.com',
            'is_staff': False,
            'ifxid': 'IFXID0000001',
        }
        url = reverse('user-list')
        response = self.client.post(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_403_FORBIDDEN, f'Incorrect response code {response.status_code}')

    def testAdminUpdateGroups(self):
        '''
        Ensure that an admin can update groups, including removing them entirely
        '''
        data.init()
        data.syncUsers()

        group_name = data.GROUPS[0]['name']
        username = data.TEST_LOGIN['username']

        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
        self.assertTrue(len(response.data) == 1, f'Incorrect number of results returned {response.data}')
        # Add one
        user_data = response.data[0]
        user_data['groups'] = [group_name]
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code after PUT {response.status_code}, {response.data}')
        self.assertTrue(len(response.data['groups']) == 1, f'Incorrect group list returned {response.data}')

        # Add another
        user_data['groups'] = [group_name, data.GROUPS[1]['name']]
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code after PUT {response.status_code}')
        self.assertTrue(len(response.data['groups']) == 2, f'Incorrect group list returned {response.data}')

        # Remove them all
        user_data['groups'] = []
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code after PUT {response.status_code}')
        self.assertTrue(len(response.data['groups']) == 0, f'Incorrect group list returned {response.data}')

    def testAdminUpdateIsActive(self):
        '''
        Ensure that an admin can update the is_active flag and that it propagates to Login
        '''
        data.init()
        data.syncUsers()

        username = data.TEST_LOGIN['username']

        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect status {response.status_code}')

        # Update is_active status
        user_data = response.data[0]
        self.assertTrue(user_data['is_active'], f'User should start out with is_active == True')
        user_data['is_active'] = False
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'PUT failed {response.status_code}')
        self.assertFalse(response.data['is_active'], f'User is still active {response.data}')

        # Ensure that the login is updated as well
        logins = NanitesAPI.listLogins(login=settings.IFX_APP['name'], username=username)
        self.assertFalse(logins[0].is_enabled, f'Login was not disabled {logins[0]}')

    def testAdminUpdatePersonFields(self):
        '''
        Ensure that an admin can update some person fields (full name)
        '''
        data.init()
        data.syncUsers()

        username = data.TEST_LOGIN['username']

        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
        self.assertTrue(len(response.data) == 1, f'Incorrect number of results returned {response.data}')

        # Update full name
        new_full_name = 'Changed'
        user_data = response.data[0]
        self.assertTrue(user_data['full_name'] == data.TEST_LOGIN['person']['full_name'], f'Full name starts wrong???')
        user_data['full_name'] = new_full_name
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response {response.status_code}')
        self.assertTrue(response.data['full_name'] == new_full_name, f'Full name not updated correctly {response.data}')

        # Ensure that the person is also updated
        person = NanitesAPI.readPerson(ifxid=user_data['ifxid'])
        self.assertTrue(person.full_name == new_full_name, f'Person full name is wrong {person.full_name}')

    def testAdminUpdateUsernameFail(self):
        '''
        Ensure that an attempt to update username will fail
        '''
        data.init()
        data.syncUsers()

        username = data.TEST_LOGIN['username']

        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')

        # Update username
        user_data = response.data[0]
        self.assertTrue(user_data['username'] == username, f'Username starts wrong???')
        user_data['username'] = 'changed'
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response {response.status_code}')
        self.assertTrue(response.data['username'] == username, f'Username was changed! {response.data}')

    # def testUserUpdatePersonFields(self):
    #     '''
    #     Ensure that a user can update their own first_name, affiliations, and contacts
    #     '''
    #     data.init()
    #     data.syncUsers()

    #     # Get the user data
    #     username = data.TEST_LOGIN['username']
    #     url = reverse('user-list')
    #     response = self.client.get(url, {'username': username}, format='json')
    #     self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
    #     user_data = response.data[0]

    #     # Login as user
    #     pwd = 'alskjfdla'
    #     user = get_user_model().objects.get(username=username)
    #     user.set_password(pwd)
    #     self.login(username, pwd)

    #     # Update first name, add affiliation and contact
    #     new_first_name = 'Howdy'
    #     user_data['first_name'] = new_first_name
    #     user_data['affiliations'].append(
    #         {
    #             'organization': 'Center for Nanoscale Systems (a Harvard Institute)',
    #             'role': 'member'
    #         }
    #     )
    #     user_data['contacts'].append(
    #         {
    #             'role': 'Additional email',
    #             'contact': {
    #                 'type': 'Email',
    #                 'detail': 'stuff@junk.com'
    #             }
    #         }
    #     )
    #     url = reverse('user-detail', kwargs={'pk': user_data['id']})
    #     response = self.client.put(url, user_data, format='json')
    #     self.assertTrue(response.data['first_name'] == new_first_name, f'Name not updated {response.data}')
    #     self.assertTrue(len(response.data['affiliations']) == 2, f'Affiliations not updated {response.data}')
    #     self.assertTrue(len(response.data['contacts']) == 2, f'Contacts not updated {response.data}')

    #     # Ensure Person is updated
    #     logins = NanitesAPI.listLogins(login=settings.IFX_APP['name'], username=username)
    #     self.assertTrue(logins[0].person.first_name == new_first_name, f'Person not updated {logins[0]}')
    #     self.assertTrue(len(logins[0].person.affiliations) == 2, f'Incorrect number of affiliations {logins[0]}')

    def testUserUpdatePersonFieldFail(self):
        '''
        Ensure that a user cannot update their full name
        '''
        data.init()
        data.syncUsers()

        # Get the user data
        username = data.TEST_LOGIN['username']
        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
        user_data = response.data[0]

        # Login as user
        pwd = 'alskjfdla'
        user = get_user_model().objects.get(username=username)
        user.set_password(pwd)
        self.login(username, pwd)

        # Update full name
        old_full_name = user_data['full_name']
        new_full_name = 'Howdy'
        user_data['full_name'] = new_full_name
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.data['full_name'] == old_full_name, f'Name updated! {response.data}')

        # Ensure Person is not updated
        logins = NanitesAPI.listLogins(login=settings.IFX_APP['name'], username=username)
        self.assertTrue(logins[0].person.full_name == old_full_name, f'Person updated! {logins[0]}')

    def testUserUpdateOtherPersonFail(self):
        '''
        Ensure that a user cannot update someone else's data
        '''
        data.init()
        data.syncUsers()

        # Get the user data
        username = data.TEST_LOGIN['username']

        url = reverse('user-list')
        response = self.client.get(url, {'username': username}, format='json')
        self.assertTrue(response.status_code == status.HTTP_200_OK, f'Incorrect response code {response.status_code}')
        user_data = response.data[0]

        # Login as other user
        username2 = data.TEST_LOGIN_2['username']
        pwd = 'alskjfdla'
        user = get_user_model().objects.get(username=username2)
        user.set_password(pwd)
        self.login(username2, pwd)

        # Try to update first name
        new_first_name = 'Howdy'
        user_data['first_name'] = new_first_name
        url = reverse('user-detail', kwargs={'pk': user_data['id']})
        response = self.client.put(url, user_data, format='json')
        self.assertTrue(response.status_code == status.HTTP_404_NOT_FOUND, f'Incorrect response {response.status_code}')
