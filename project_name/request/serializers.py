# -*- coding: utf-8 -*-

'''
serializers for request objects

Created on  2021-12-03

@copyright: 2021 The President and Fellows of Harvard College.
All rights reserved.
@license: GPL v2.0
'''
import logging
from django.db import transaction
from django.db.models import Prefetch
from rest_framework import serializers, viewsets
from ifxrequest.models import Request, RequestState, RequestComment, RequestFile, RequestFileCategory
from ifxuser import serializers as ifxuser_serializers
from ifxuser import models as ifxuser_models


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
        fields = '__all__'


class RequestCommentSerializer(serializers.ModelSerializer):
    '''
    Serializer for Request States
    '''
    author = serializers.CharField(max_length=50, read_only=True)
    created = serializers.DateTimeField(read_only=True)
    text = serializers.CharField(max_length=2000, required=True)

    class Meta:
        model = RequestComment
        fields = '__all__'

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


class RequestFileSerializer(serializers.ModelSerializer):
    '''
    serializer for RequestFiles
    '''
    request = serializers.PrimaryKeyRelatedField(queryset=Request.objects.all())
    file = serializers.FileField()
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=RequestFileCategory.objects.all()
    )

    class Meta:
        model = RequestFile
        fields = (
            'request',
            'file',
            'id',
            'category',
        )



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
    request_files = RequestFileSerializer(source='requestfile_set', many=True, read_only=True)

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
            'updated',
            'request_files',
        )


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
        requestor_data = self.initial_data.get('requestor')
        if requestor_data:
            try:
                requestor_id = requestor_data.get('id')
                requestor = ifxuser_models.IfxUser.objects.get(id=requestor_id)
                instance.requestor = requestor
            except ifxuser_models.IfxUser.DoesNotExist as dne:
                raise serializers.ValidationError(f'Requestor with id {requestor_id} does not exist') from dne

        approvers_data = self.initial_data.get('approvers')
        instance.approvers.clear()
        if approvers_data:
            for approver_data in approvers_data:
                try:
                    approver = ifxuser_models.IfxUser.objects.get(id=approver_data.get('id'))
                    instance.approvers.add(approver)
                except ifxuser_models.IfxUser.DoesNotExist as dne:
                    raise serializers.ValidationError(f'Approver with id {approver_data.get("id")} does not exist') from dne

        request_states_data = self.initial_data.get('request_states')
        for request_state_data in request_states_data:
            # You only add request states when updating, never remove
            if not request_state_data.get('id'):
                request_state = RequestStateSerializer(
                    data=request_state_data,
                    context={'request': self.context.get('request')}
                )
                request_state.is_valid(raise_exception=True)
                request_state.save()

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

        instance.save()

        return instance


class RequestViewSet(viewsets.ModelViewSet):
    '''
    Viewset for Requests
    '''
    serializer_class = RequestSerializer
    queryset = Request.objects.all().prefetch_related(
        Prefetch('requestcomment_set', queryset=RequestComment.objects.all().order_by('-created'))
    )
