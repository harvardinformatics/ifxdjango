# -*- coding: utf-8 -*-

'''
serializers.py

Created on  {% now "Y-m-d" %}

Serializers and ViewSets for hers
'''
import logging
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.db import transaction
from rest_framework import serializers, viewsets
from ifxuser import serializers as ifxuser_serializers
from ifxuser import models as ifxuser_models
from ifxbilling import models as ifxbilling_models
from ifxbilling import serializers as ifxbilling_serializers
from {{project_name}} import permissions
from {{project_name}} import roles as Roles
from {{project_name}} import models

logger = logging.getLogger(__name__)

class SkinnyUserSerializer(serializers.ModelSerializer):
    '''
    Serializer that just provides user basics.
    '''
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'ifxid',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'primary_affiliation',
            'email',
            'is_active',
        )


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
    permission_classes = [permissions.AdminPermission]


    def get_queryset(self):
        '''
        Filter by name or org_tree
        '''
        org_trees = self.request.query_params.get('org_tree', '').split(',')
        name = self.request.query_params.get('name')
        rank = self.request.query_params.get('rank')
        search = self.request.query_params.get('search')

        orgset = ifxuser_models.Organization.objects.all()
        if org_trees and org_trees[0]:
            orgset = orgset.filter(org_tree__in=org_trees)
        if name:
            orgset = orgset.filter(name=name)
        if rank:
            orgset = orgset.filter(rank=rank)
        if search:
            orgset = orgset.filter(Q(rank__icontains=search)| Q(name__icontains=search))

        return orgset.order_by('org_tree', 'name')


class UserAffiliationSerializer(serializers.ModelSerializer):
    '''
    Read only serializer for adding organizations to user records
    '''
    organization = serializers.SlugRelatedField(slug_field='slug', queryset=ifxuser_models.Organization.objects.all())

    class Meta:
        model = ifxuser_models.UserAffiliation
        fields = '__all__'


class UserAccountSerializer(serializers.ModelSerializer):
    '''
    User accounts
    '''
    account = ifxbilling_serializers.AccountSerializer(read_only=True)

    class Meta:
        model = ifxbilling_models.UserAccount
        fields = ('id', 'account', 'is_valid')


class UserProductAccountSerializer(serializers.ModelSerializer):
    '''
    User product accounts
    '''
    account = ifxbilling_serializers.AccountSerializer(read_only=True)
    product = ifxbilling_serializers.ProductSerializer(read_only=True)

    class Meta:
        model = ifxbilling_models.UserProductAccount
        fields = ('id', 'account', 'product', 'percent', 'is_valid')


class UserSerializer(ifxuser_serializers.UserSerializer):
    '''
    Add accounts to user information
    '''
    accounts = UserAccountSerializer(many=True, read_only=True, source='useraccount_set')
    product_accounts = UserProductAccountSerializer(many=True, read_only=True, source='userproductaccount_set')

    class Meta:
        model = ifxuser_models.IfxUser
        fields = (
            'username',
            'email',
            'is_staff',
            'first_name',
            'last_name',
            'full_name',
            'ifxid',
            'is_active',
            'groups',
            'last_update',
            'date_joined',
            'id',
            'affiliations',
            'primary_affiliation',
            'contacts',
            'accounts',
            'product_accounts',
        )
        read_only_fields = ('id', 'last_update', 'date_joined', 'ifxid', 'username')

    @transaction.atomic
    def update(self, instance, validated_data):
        '''
        Ensure that account information is updated
        '''
        instance = super().update(instance, validated_data)
        instance.useraccount_set.all().delete()
        return instance


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    '''
    ViewSet for users
    '''
    serializer_class = UserSerializer
    permission_classes = [permissions.HersUserViewSetPermissions]

    def get_queryset(self):
        if Roles.userIsAdmin(self.request.user):
            groupstr = self.request.query_params.get('groups')
            username = self.request.query_params.get('username')
            search = self.request.query_params.get('search')
            exclude_application_users = self.request.query_params.get('exclude_application_users', 'true').upper() == 'TRUE'
            # Include disabled if specifically request or with non-GET methods
            include_disabled = self.request.query_params.get('include_disabled', 'false').upper() == 'TRUE' or self.request.method != 'GET'
            if username:
                users = get_user_model().objects.filter(username=username)
            elif search:
                users = get_user_model().objects.filter(
                    Q(username__icontains=search) |
                    Q(full_name__icontains=search) |
                    Q(email__icontains=search)
                )
            else:
                users = get_user_model().objects.all()
            if groupstr is not None:
                groups = groupstr.strip().split(',')
                users = users.filter(groups__name__in=groups)
            if exclude_application_users:
                users = users.exclude(ifxid__isnull=True).exclude(ifxid='')
            if not include_disabled:
                users = users.filter(is_active=True)
        else:
            users = get_user_model().objects.filter(username=self.request.user.username)
        return users.order_by('last_name', 'first_name')
