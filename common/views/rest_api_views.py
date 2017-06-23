# -*- coding: utf-8 -*-
"""
Put views for rest apis in common here. These views should return json format.

Any views that take input should NEVER take sensitive information in the url.
"""
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

from common.models import Country
