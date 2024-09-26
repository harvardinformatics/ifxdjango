"""ifxdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework import routers
from ifxuser.views import get_org_names, get_org_list
from ifxuser import serializers as ifxuser_serializers
from ifxbilling import serializers as ifxbilling_serializers
from ifxbilling import views as ifxbilling_views
from ifxreport.views import run_report
from ifxreport.serializers import ReportRunViewSet, ReportViewSet
from {{project_name}} import settings, serializers
from {{project_name}} import views
from {{project_name}}.request import views as request_views
from {{project_name}}.request import serializers as request_serializers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', serializers.UserViewSet, 'user')
router.register(r'groups', ifxuser_serializers.GroupViewSet, 'group')
router.register(r'requests', request_serializers.RequestViewSet)
router.register(r'contacts', serializers.ContactViewSet)
router.register(r'organizations', serializers.OrganizationViewSet, 'organization')
router.register(r'accounts', ifxbilling_serializers.AccountViewSet, 'account')
router.register(r'billing-records', ifxbilling_serializers.BillingRecordViewSet, 'billing-records')
router.register(r'products', ifxbilling_serializers.ProductViewSet, 'products')
router.register(r'facilities', ifxbilling_serializers.FacilityViewSet, 'facilities')
router.register(r'report-runs', ReportRunViewSet, 'report-run')
router.register(r'reports', ReportViewSet, 'report')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path(r'{{project_name}}/djadmin/', admin.site.urls),
    path(r'{{project_name}}/api/mock-errors/<int:pk>/', views.mock_error),
    path(r'{{project_name}}/api/users/get-nanite-login/', views.get_ifxapp_nanite_login),
    path(r'{{project_name}}/api/onboard-requests/<int:pk>/', request_views.onboard_requests),
    path(r'{{project_name}}/api/onboard-requests/', request_views.onboard_requests),
    path(r'{{project_name}}/api/requests/get-request-list/', request_views.get_request_list),
    path(r'{{project_name}}/api/requests/get-valid-processor-states/', request_views.get_valid_processor_states),
    path(r'{{project_name}}/api/requests/set-request-state/', request_views.set_request_state),
    path(r'{{project_name}}/api/requests/account-request/<int:pk>/', request_views.update_account_request),
    path(r'{{project_name}}/api/requests/account-request/', request_views.update_account_request),
    path(r'{{project_name}}/api/djvocab', include('djvocab.urls')),
    path(r'{{project_name}}/api/obtain-auth-token/', views.get_remote_user_auth_token),
    path(r'{{project_name}}/api/contacts/get-contact-list/', views.get_contact_list),
    path(r'{{project_name}}/api/get-location-info/', views.get_location_info),
    path(r'{{project_name}}/api/messages/', views.ifx_messages),
    path(r'{{project_name}}/api/messages/<int:pk>/', views.ifx_read_update_or_delete_message, name='read-update-delete-message'),
    path(r'{{project_name}}/api/mailings/', views.ifx_mailings),
    path(r'{{project_name}}/api/mailings/<int:pk>/', views.ifx_read_mailing, name='read-mailing'),
    path(r'{{project_name}}/api/send-mailing/', views.send_ifx_mailing),
    path(r'{{project_name}}/api/billing/expense-code-request/', ifxbilling_views.expense_code_request),
    path(r'{{project_name}}/api/billing/get-billing-record-list/', ifxbilling_views.get_billing_record_list),
    path(r'{{project_name}}/api/get-org-names/', get_org_names),
    path(r'{{project_name}}/api/get-org-list/', get_org_list),
    path(r'{{project_name}}/api/get-contactables/', views.get_contactables),
    path(r'{{project_name}}/api/billing-records/bulk-update/', ifxbilling_serializers.BillingRecordViewSet.bulk_update),
    path(r'{{project_name}}/api/billing/update-user-accounts/', views.update_user_accounts_view, name='update-user-accounts'),
    path(r'{{project_name}}/api/run-report/', run_report, name='run-report'),
    path(r'{{project_name}}/api/', include(router.urls)),
    re_path(r'^{{project_name}}/.*$', TemplateView.as_view(template_name="index.html")),
]
