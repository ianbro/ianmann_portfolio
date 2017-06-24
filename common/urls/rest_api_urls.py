"""
Put urls that are used for a REST api for this app here. These urls should not
be used by a user, only by the website code (javascript specifically).

All urls in this file should return views in "common/views/rest_api_views.py".
"""
from django.conf.urls import url

from common.views.rest_api_views import CountryCrudView

urlpatterns = [
    url(r'^crud/country(?:/(?P<pk>\d+)/)?', CountryCrudView.as_view(), name="country_crud"),
]
