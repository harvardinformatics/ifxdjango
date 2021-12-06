# -*- coding: utf-8 -*-

'''
serializers for request objects

Created on  {% now "Y-m-d" %}

@copyright: 2020 The Presidents and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
from django.db import transaction
from django.db.models import Prefetch
from rest_framework import serializers, viewsets
from ifxrequest.models import Request, RequestState, RequestComment
from ifxuser import serializers as ifxuser_serializers


logger = logging.getLogger(__name__)


class RequestStateSerializer(serializers.ModelSerializer):
    '''
    Serializer for Request States
    '''
    user = ifxuser_serializers.UserSerializer(read_only=True, many=False)
    approvers = serializers.SlugRelatedField(
        slug_field='username', many=True, read_only=True)
    queryset = RequestState.objects.all().order_by('-created')

    class Meta:
        model = RequestState
        fields = ('__all__')


class RequestCommentSerializer(serializers.ModelSerializer):
    '''
    Serializer for Request States
    '''
    author = serializers.CharField(max_length=50, read_only=True)
    created = serializers.DateTimeField(read_only=True)
    text = serializers.CharField(max_length=2000, required=True)

    class Meta:
        model = RequestComment
        fields = ('__all__')

    def create(self, validated_data):
        '''
        Set the "author" field to the request.user
        '''
        http_request = self.context.get("request")
        author = http_request.user.username
        validated_data['author'] = author
        logger.debug('Validated data %s', str(validated_data))

        instance = RequestComment(**validated_data)
        instance.save()

        return instance


    def update(self, instance, validated_data):
        '''
        Set the "author" field to the request.user
        '''
        pass


class RequestSerializer(serializers.ModelSerializer):
    '''
    Serializer for all request types.  Approvers, requestor, and approver_contact
    are returned as full objects for read purposes.  approver_usernames, request_username,
    and approver_contact_name are used in create / update.

    Approvers may be automatically set if not provided, e.g. for Account Requests,
    using the appropriate Group membership.
    '''
    request_type = serializers.CharField(max_length=100, required=True)
    current_state = serializers.CharField(
        max_length=100, read_only=True)
    result = serializers.CharField(
        max_length=100, required=False, allow_null=True)
    processor = serializers.CharField(max_length=100, required=True)
    requestor = ifxuser_serializers.UserSerializer(read_only=True)
    approvers = ifxuser_serializers.UserSerializer(many=True, read_only=True)
    data = serializers.JSONField(required=False)
    request_states = RequestStateSerializer(source='requeststate_set', many=True, read_only=True)
    request_comments = RequestCommentSerializer(source='requestcomment_set', many=True, read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Request
        fields = (
            'id',
            'request_type',
            'current_state',
            'result',
            'processor',
            'requestor',
            'approvers',
            'auto_approve',
            'data',
            'request_states',
            'request_comments',
            'created',
            'updated'
        )

    @transaction.atomic
    def create(self, validated_data):
        '''
        Create comments if they are included
        '''
        pass

    @transaction.atomic
    def update(self, instance, validated_data):
        '''
        Create new comments if they are included
        Does not update current_state or request_states; that should be done with the setState endpoint

        '''
        for key in [
            'request_type',
            'result',
            'processor',
            'requestor',
            'auto_approve',
            'data',
        ]:
            setattr(instance, key, validated_data.get(key))

        # instance.approvers.set(validated_data.get('approvers', []))

        # Collect current and updated ids.  Difference will be the deletables
        request_comment_ids = {rc.id for rc in instance.requestcomment_set.all()}
        updated = set()
        request_comments_data = self.initial_data.get('request_comments')
        for request_comment_data in request_comments_data:
            if 'id' in request_comment_data and request_comment_data['id']:
                pk = request_comment_data['id']
                request_comment = RequestComment.objects.get(id=pk)
                request_comment.text = request_comment_data['text']
                updated.add(pk)
            else:
                request_comment = RequestCommentSerializer(
                    data=request_comment_data,
                    context={'request': self.context.get('request')}
                )
                request_comment.is_valid(raise_exception=True)
            request_comment.save()

        to_delete = request_comment_ids - updated
        for pk in to_delete:
            RequestComment.objects.get(id=pk).delete()

        return instance


class RequestViewSet(viewsets.ModelViewSet):
    '''
    Viewset for Requests
    '''
    serializer_class = RequestSerializer
    queryset = Request.objects.all().prefetch_related(
        Prefetch('requestcomment_set', queryset=RequestComment.objects.all().order_by('-created'))
    )
