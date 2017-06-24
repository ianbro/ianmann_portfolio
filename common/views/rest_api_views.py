# -*- coding: utf-8 -*-
"""
Put views for rest apis in common here. These views should return json format.

Any views that take input should NEVER take sensitive information in the url.
"""
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from common.models import Country
from ianmann.utils.api import ApiView

class CountryCrudView(ApiView):

    allowed_methods = ("POST", "GET", "PUT", "DELETE")

    def get(self, request, *args, **kwargs):
        country = get_object_or_404(Country, pk=kwargs.get("pk", None))
        return country.json()
