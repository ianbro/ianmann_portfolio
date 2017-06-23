# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import ianmann.utils.custom_model_fields as cmf
from common.models import Organization

class Company(models.Model):

    name = cmf.RequiredCharField(max_length=50)
    company_website = models.CharField(max_length=200)
    hq_address = models.CharField(max_length=10)

# Create your models here.
class Employment(models.Model):

    title = cmf.RequiredCharField(max_length=50)
    organization = cmf.RequiredForeignKey(Organization)
