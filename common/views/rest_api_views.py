# -*- coding: utf-8 -*-
"""
Put views for rest apis in common here. These views should return json format.

Any views that take input should NEVER take sensitive information in the url.
"""
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from common.models import (Country,
                            Region,
                            City,
                            Street,
                            Address,
                            Organization)
from ezi.views import ApiView, ModelCrudApiView

class CountryCrudView(ModelCrudApiView):

    model = Country

    allowed_methods = ("GET", "PUT", "DELETE")

class RegionCrudView(ModelCrudApiView):

    model = Region

    allowed_methods = ("GET", "PUT", "DELETE")

class CityCrudView(ModelCrudApiView):

    model = City

    allowed_methods = ("GET", "PUT", "DELETE")

class StreetCrudView(ModelCrudApiView):

    model = Street

    allowed_methods = ("GET", "PUT", "DELETE")

class AddressCrudView(ModelCrudApiView):

    model = Address

    allowed_methods = ("GET", "PUT", "DELETE")

class OrganizationCrudView(ModelCrudApiView):

    model = Organization

    allowed_methods = ("GET", "PUT", "DELETE")
