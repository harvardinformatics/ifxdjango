"""
Django admin for {{project_name}}

Created on  {% now "Y-m-d" %}
"""
import csv
from django.http import HttpResponse
from django.contrib import admin
from django import forms
from ifxuser.admin import UserGroupInlineAdmin
from ifxuser.models import UserAffiliation
from ifxbilling.admin import UserAccountInlineAdmin
from {{project_name}} import models


admin.site.site_header = '{{project_name|upper}} Admin'
admin.site.site_url = '/{{project_name}}/'

class ExportCsvMixin:
    """
    Provide an export for Django admin tables
    """
    def export_as_csv(self, request, queryset):
        '''
        Export as csv
        '''

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"


class UserAffiliationInlineAdmin(admin.TabularInline):
    '''
    User affiliations inline
    '''
    model = UserAffiliation
    autocomplete_fields = ('user', 'organization')
    extra = 0


class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    '''
    IfxUser admin, includes {{project_name}}-specific fields
    '''
    fields = ('ifxid', 'username', 'email', 'first_name', 'last_name', 'full_name', 'primary_affiliation', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_update')
    list_display = ('id', 'ifxid', 'username', 'email', 'full_name', 'primary_affiliation', 'date_joined', 'last_update', 'get_token', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ('-is_active', '-is_staff', 'last_name', 'first_name')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'ifxid', 'primary_affiliation__slug')
    inlines = [UserGroupInlineAdmin, UserAffiliationInlineAdmin, UserAccountInlineAdmin]
    actions = ['export_as_csv']
    readonly_fields = ('last_update', 'date_joined')

    def get_token(self, obj):
        '''
        Returns users auth token
        '''
        if hasattr(obj, 'auth_token'):
            return obj.auth_token.key
        else:
            return ''
    get_token.short_description = 'Token'


admin.site.register(models.{{project_name|title}}User, UserAdmin)
