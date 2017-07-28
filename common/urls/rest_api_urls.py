"""
Put urls that are used for a REST api for this app here. These urls should not
be used by a user, only by the website code (javascript specifically).

All urls in this file should return views in "common/views/rest_api_views.py".
"""
from django.conf.urls import url

from ezi.urls import crud_api_url_factory

from common.models import Country, Region
from common.views.rest_api_views import (RegionCrudView,
                                            CityCrudView,
                                            StreetCrudView,
                                            AddressCrudView,
                                            OrganizationCrudView)

urlpatterns = [
    url(r'^crud/city/(?:(?P<pk>\d+))?', CityCrudView.as_view(), name="city_crud"),
    url(r'^crud/street/(?:(?P<pk>\d+))?', StreetCrudView.as_view(), name="street_crud"),
    url(r'^crud/address/(?:(?P<pk>\d+))?', AddressCrudView.as_view(), name="address_crud"),
    url(r'^crud/organization/(?:(?P<pk>\d+))?', OrganizationCrudView.as_view(), name="organization_crud"),
]

urlpatterns.extend(crud_api_url_factory([
    Country,
    Region,
]))
