"""ifxdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from rest_framework import routers
from ifxuser.views import get_org_names
from ifxuser import serializers as ifxuser_serializers
from ifxbilling import serializers as ifxbilling_serializers
from ifxbilling import views as ifxbilling_views
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


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path(r'{{project_name}}/djadmin/', admin.site.urls),
    path(r'{{project_name}}/api/mock-errors/<int:pk>/', views.mock_error),
    path(r'{{project_name}}/api/users/get-nanite-login/', views.get_ifxapp_nanite_login),
    path(r'{{project_name}}/api/onboard-requests/<int:pk>/', request_views.onboard_requests),
    path(r'{{project_name}}/api/onboard-requests/', request_views.onboard_requests),
    path(r'{{project_name}}/api/users/update-person/', views.update_person),
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
    path(r'{{project_name}}/api/get-org-names/', get_org_names),
    path(r'{{project_name}}/api/', include(router.urls)),
    url(r'^{{project_name}}/.*$', TemplateView.as_view(template_name="index.html")),
]
