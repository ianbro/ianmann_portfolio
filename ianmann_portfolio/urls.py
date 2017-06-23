"""
ianmann_portfolio URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^helm/', admin.site.urls),
    url(r'^common/api/rest/', include("common.urls.rest_api_urls", namespace="common_rest_api")),
]
