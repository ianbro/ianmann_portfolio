# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import ianmann.utils.custom_model_fields as cmf
from common.models import Organization

class Involvement(models.Model):

    description = cmf.RequiredTextField(max_length=500)
    organization = cmf.RequiredForeignKey(Organization)

class Employment (models.Model):

    title = cmf.RequiredCharField(max_length=50)
    organization = cmf.RequiredForeignKey(Organization)
    description = cmf.RequiredTextField(max_length=500)

class ProfessionalProject(models.Model):

    name = cmf.RequiredCharField(max_length=100)
    description = cmf.RequiredTextField(max_length=300)
    employment = cmf.RequiredForeignKey(Employment)

    github_link = models.CharField(max_length=100)
