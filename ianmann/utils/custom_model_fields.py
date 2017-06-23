"""
Contains subclasses of certain model fields with meta data that is commonly
used.

For example, models.CharField(blank=False, null=False) is used alot to
add a required CharField, so in here, there is RequiredCharField which
automatically uses blank and null as False.
"""
from django.db import models

class RequiredCharField(models.CharField):
    """
    Extension of models.CharField.

    Instances of this class will set blank and null to False by default.
    """

    def __init__(self, *args, **kwargs):
        """
        If blank and null are not passed in through kwargs, then this will send
        False to the super constructor in their place. This will default the
        values for blank and null to False, essentially making this a required
        field.

        If blank and null are passed through kwargs, then this constructor will
        simply pass them on with the given value to the super constructor.
        """
        blank = kwargs.pop("blank", False)
        null = kwargs.pop("null", False)

        return super(RequiredCharField, self).__init__(*args, blank=blank, null=null, **kwargs)


class RequiredForeignKey(models.ForeignKey):
    """
    Extension of models.ForeignKey.

    Instances of this class will set blank and null to False by default.
    """

    def __init__(self, *args, **kwargs):
        """
        If blank and null are not passed in through kwargs, then this will send
        False to the super constructor in their place. This will default the
        values for blank and null to False, essentially making this a required
        field.

        If blank and null are passed through kwargs, then this constructor will
        simply pass them on with the given value to the super constructor.
        """
        blank = kwargs.pop("blank", False)
        null = kwargs.pop("null", False)

        return super(RequiredForeignKey, self).__init__(*args, blank=blank, null=null, **kwargs)


class RequiredIntegerField(models.IntegerField):
    """
    Extension of models.IntegerField.

    Instances of this class will set blank and null to False by default.
    """

    def __init__(self, *args, **kwargs):
        """
        If blank and null are not passed in through kwargs, then this will send
        False to the super constructor in their place. This will default the
        values for blank and null to False, essentially making this a required
        field.

        If blank and null are passed through kwargs, then this constructor will
        simply pass them on with the given value to the super constructor.
        """
        blank = kwargs.pop("blank", False)
        null = kwargs.pop("null", False)

        return super(RequiredIntegerField, self).__init__(*args, blank=blank, null=null, **kwargs)
