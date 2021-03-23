# -*- coding: utf-8 -*-

'''
serializers.py

Serializers and ViewSets for {{project_name}}
'''
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import transaction
from rest_framework.response import Response
from rest_framework import serializers, viewsets
from ifxuser import serializers as ifxuser_serializers
from ifxuser import models as ifxuser_models
from {{project_name}} import permissions


logger = logging.getLogger(__name__)


class ContactViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for Contacts
    '''
    queryset = ifxuser_models.Contact.objects.all()
    serializer_class = ifxuser_serializers.ContactSerializer
    permission_classes = [permissions.AdminPermission]


class OrganizationViewSet(viewsets.ModelViewSet):
    '''
    Viewset for Organizations
    '''
    serializer_class = ifxuser_serializers.OrganizationSerializer
    permissions = [permissions.AdminPermission]


    def get_queryset(self):
        '''
        Filter by name or org_tree
        '''
        org_trees = self.request.query_params.get('org_tree', '').split(',')
        name = self.request.query_params.get('name')
        search = self.request.query_params.get('search')

        orgset = ifxuser_models.Organization.objects.all()
        if org_trees and org_trees[0]:
            orgset = orgset.filter(org_tree__in=org_trees)
        if name:
            orgset = orgset.filter(name=name)
        if search:
            orgset = orgset.filter(Q(rank__icontains=search)| Q(name__icontains=search))

        return orgset.order_by('org_tree', 'name')


class GroupSerializer(serializers.ModelSerializer):
    '''
    Serializer for Groups
    '''
    class Meta:
        model = Group
        fields = '__all__'


class GroupViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for groups
    '''

    def list(self, request):
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = get_user_model().objects.all().filter(username=username)
            serializer = ifxuser_serializers.UserSerializer(queryset, many=True)
            data = serializer.data[0]['groups']
        else:
            queryset = Group.objects.all()
            serializer = GroupSerializer(queryset, many=True)
            data = serializer.data
        return Response(data=data)
