# -*- coding: utf-8 -*-

'''
nanites initDev

Initializes development data for a system, include some
dev users and application tokens.

Created on  2019-12-23

@author: Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>
@copyright: 2019 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
# from {{project_name}}.init import main as init_production


# def main():
#     '''
#     Run dev data initialization
#     '''
#     modelsForFixture = init_production()
#     modelsForFixture['auth.User'].extend(initUsers())
#     modelsForFixture['authtoken.Token'] = initTokens()
#     return modelsForFixture

# def initUsers():
#     '''
#     Setup veradmin and application user tokens
#     '''
#     pks = []
#     users = [
#         {
#             'username': 'veradmin',
#             'first_name': 'Vera D.',
#             'last_name': 'Min',
#             'is_active': True,
#             'is_superuser': True,
#             'is_staff': True,
#         },
#         {
#             'username': 'nanites.client',
#             'first_name': 'Nanites Client',
#             'last_name': 'Application',
#             'is_active': True,
#             'is_superuser': True,
#             'is_staff': True,
#         }
#     ]
#     for userdata in users:
#         (obj, created) = get_user_model().objects.get_or_create(**userdata)
#         pks.append(obj.pk)

#     return pks


# def initTokens():
#     '''
#     Set tokens to common values
#     '''
#     pks = []
#     tokens = [
#         {
#             'username': 'veradmin',
#             'token': '9f822e797823b3a6d5cf2a353baf0649a012e13c',
#         },
#         {
#             'username': 'cns',
#             'token': '56a2ed873309e7440b5bbd5dc25a802d861e61b0',
#         },
#         {
#             'username': 'nice',
#             'token': '52b28b781722283740d228ce311a487227ec26a4',
#         },
#         {
#             'username': 'p3',
#             'token': 'c7367dd90551513ae56ad112e68b69f7b78e6c58',
#         },
#         {
#             'username': 'cas',
#             'token': 'cf31a96fd6238c4e7760dab4967a7cd494164b0a',
#         },
#         {
#             'username': 'ifxonboard',
#             'token': '52b28b781722283740d228ce311a487227ec2999',
#         },
#         {
#             'username': 'pubs',
#             'token': 'cf31a96fd6238c4e7760dab4967a7cd494164999',
#         },
#         {
#             'username': 'nanites.client',
#             'token': '5944af78759a6efd27aca271072e094a939dc072'
#         },
#         {
#             'username': 'portal',
#             'token': 'b4748dd0545ebdcb6d40c68eb0d3783f2ca2404c'
#         },
#     ]
#     for tokendata in tokens:
#         user = get_user_model().objects.get(username=tokendata['username'])
#         (obj, created) = Token.objects.get_or_create(user=user)
#         Token.objects.filter(user=user).update(key=tokendata['token'])
#         pks.append(obj.pk)

#     return pks
