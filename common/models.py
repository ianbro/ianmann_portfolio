# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import ianmann.utils.custom_model_fields as cmf

"""
ADDRESS MODELS

Allows the website to track addresses of organizations. As the website is used
more and more, the use of models will be more and more usefull. More data will
be populated so a user can search and use an already existing address rather
than type in their own address.

It will also allow better validation on things like cities and countries than
would be available if simple CharFields were used.
"""

class Country(models.Model):
    """
    Represents a country that will be used in addresses for organizations and
    personal addresses.
    """
    name = cmf.RequiredCharField(max_length=50)

    def json(self):
        """
        Returns a json representation of this object.
        See "styleguides/CODe_STYLE.md" for more information on this method.
        """
        return {
            "name": self.name
        }

class Region(models.Model):
    """
    Represents a region in a country that will be used in addresses for
    organizations and personal addresses.

    A region can be any one of the following types:
        - State (example: U.S. states)
        - Region
        - Province (example: old France regional breakdown)
    """
    REGION_TYPES = (
        ("ST", "State"),
        ("RE", "Region"),
        ("PR", "Province")
    )

    name = cmf.RequiredCharField(max_length=50)
    region_type = cmf.RequiredCharField(max_length=2, choices=REGION_TYPES, default="ST")
    country = cmf.RequiredForeignKey(Country)

class City(models.Model):
    """
    Represents a city in a region that will be used in addresses for
    organizations and personal addresses.
    """
    name = cmf.RequiredCharField(max_length=50)
    region = cmf.RequiredForeignKey(Region)


class Street(models.Model):
    """
    Represents a street in a city that will be used in addresses for
    organizations and personal addresses.
    """
    name = cmf.RequiredCharField(max_length=50)
    city = cmf.RequiredForeignKey(City)

class Address(models.Model):
    """
    Represents a location of a building for an organization or a personal
    address.

    To get city, state and contry, use street. This class is related to those
    instances indirectly through street.

    For example, to get the country of this address, call
    "street.city.region.country".
    """
    building_number = cmf.RequiredIntegerField()
    street = cmf.RequiredForeignKey(Street)

"""
END ADDRESS MODELS
"""

class Organization(models.Model):
    """
    Represents an organization used to record experience history for a user and
    where he or she has worked or volunteered.
    """
    name = cmf.RequiredCharField(max_length=50)
    website_homepage = models.CharField(max_length=200)
    hq_address = cmf.RequiredForeignKey(Address)
