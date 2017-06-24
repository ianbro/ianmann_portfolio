from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View

class IanmannJsonResponse(JsonResponse):
    """
    Adds some extra things to the base JsonResponse object. This is used to
    maintain consistancy accross the project. Views should never use the raw
    JsonResponse. Instead, they should use this.
    """

    def __init__(self, json, *args, **kwargs):
        """
        Adds the following to the input:
            * json is wrapped in a dictionary at the key "response".
            * the super constructor is automatically sent a value for indenting
            the resulting json. Even if the user tries to override this in
            kwargs, this will just ignore that.
        """
        indent_arg = {"indent": 4}
        altered_kw = {"json_dumps_params": {}}
        altered_kw.update(kwargs)
        altered_kw["json_dumps_params"].update(indent_arg)

        json = {"response": json}
        super(IanmannJsonResponse, self).__init__(json, *args, **altered_kw)

def valid_method(request, allowed_methods):
    """
    Searches allowed_methods to see if request.method is in the list. If so,
    then the request is permitted to use this method. Otherwise, it is assumed
    that the request should not be allowed.

    Returns True if the request uses a valid verb. False otherwise
    """
    return request.method in allowed_methods

def respond_bad_request_verb(request):
    """
    Returns a 400 error response to be used if the request was made with a verb
    that is not allowed by the view.
    """
    return HttpResponseBadRequest("This page does not support the method \"{0}\"".format(request.method))

class RestApiGetParameter:
    """
    Wraps a get parameter in a class that has parsed values. Get parameters for
    REST APIs can be expected to be in the following format: 'name::type=value'.
    When wrapped as a RestApiGetParameter instance, the parts in the parameter
    are parsed into attribute_name, attribute_type and attribute_value
    corresponding to name, type and value respctively in the parameter.

    For example, if the parameter is 'age::int:21', then the instance will
    populate the fields as so:

        attribute_name: "age"
        attribute_type: "int"
        attribute_value: 21 (It's type is dependant on attribute_type. So 'int'
                            will cause the value to be converted to an int while
                            'bool' will cause the value to be converted to a
                            boolean.)
    """

    _NAME_TYPE_DELIMITER = "::"
    _VALID_PARAM_TYPES = ("int", "str", "bool", "date", "fk", "fl")
    _VALID_PYTHON_TYPES = (int, str, bool, datetime, models.Model, float)

    _attribute_name = ""
    _attribute_type = ""
    _attribute_value = ""

    def _bad_param_key_format_error(self, get_param_key):
        """
        Returns an error that should be thrown when teh key is not in a valid
        format.
        """
        return ValueError("Error on GET parameter key: {0}. The key must be in the format 'name::type' where type is one of ['{1}'].".format(get_param_key, "', '".join(_VALID_PARAM_TYPES)))

    def _bad_python_value_error(self, py_obj):
        """
        Returns an error that should be thrown when the python objects type is
        not supported by this class.
        """
        return ValueError(
            "Error on creating GET parameter with value: {0}. The object type must be one of ['{1}'], not {2}.".format(
                get_param_key,
                "', '".join([t.__name__ for t in self._VALID_PYTHON_TYPES]),
                py_obj.__class__.__name__
            )
        )

    def _parse_param_key(self, get_param_key):
        """
        Seperate the GET parameter key into the corresponding attributes name
        and data type.

        This method assumes that the key is in the format name::type. If this is
        not so, then a ValueError is thrown.
        """
        param_key_parts = get_param_key.split(_NAME_TYPE_DELIMITER)
        if not len(param_key_parts) == 2 or "" in param_key_parts:
            raise self._bad_param_key_format_error(get_param_key)

        self._attribute_name = param_key_parts[0]

        if param_key_parts[1] in _VALID_PARAM_TYPES:
            self._attribute_type = param_key_parts[1]
        else:
            raise self._bad_param_key_format_error(get_param_key)

    def _parse_param_value(self, get_param_value):
        """
        Parses get_param_value into the desired value based on
        self._attribute_type. Depending on the value of the type, value will be
        converted to the appropriate datatype.

        Some manipulation may be needed
        to properly convert from a string to certain datatypes. Datetime objects
        are an example of this.
        """
        if self._attribute_type == "int":
            # Assume value is in integer format. (All numeric, no decimal point)
            self._attribute_value = int(get_param_value)
        elif self._attribute_type == "str"
            # Convert value to a string.
            self._attribute_value = str(get_param_value)
        elif self._attribute_type == "bool":
            # Assume value is in integer format. 0 = False. 1+ = True.
            self._attribute_value = get_param_value > 0
        elif self._attribute_type == "date":
            # ex: "21/11/06 16:30"
            self._attribute_value = datetime.strptime(get_param_value, "%d/%m/%Y %H:%M")
        elif self._attribute_type == "fk":
            # Assume value is a pk and is in integer format.
            self._attribute_value = int(get_param_value)
        elif self._attribute_type == "fl":
            # Assume value is all numeric.
            self._attribute_value = float(get_param_value)
        else:
            raise self._bad_param_key_format_error("::".join([self._attribute_name, self._attribute_type]))

    def _parse(self, get_param_key, get_param_value):
        """Wrapper for parsing everything in the GET parameter."""
        self._parse_param_key(get_param_key)
        self._parse_param_value(get_param_value)

    def _set_value_and_type_from_python_object(self, py_obj):
        """
        Sets self._attribute_value as a string and self._attribute_type as a
        string that represent the value and data type of py_obj.

        If py_obj is not of a type supported in this method, a ValueError will
        be thrown.
        """
        obj_class = py_obj.__class__
        if issubclass(obj_class, int):
            # Set value as an int
            self._attribute_type = "int"
            self._attribute_value = py_obj
        elif issubclass(obj_class, str):
            # Set value as a string
            self._attribute_type = "str"
            self._attribute_value = py_obj
        elif issubclass(obj_class, bool):
            # Set value as a boolean
            self._attribute_type = "bool"
            self._attribute_value = py_obj
        elif issubclass(obj_class, datetime):
            # Set value as a date
            self._attribute_type = "date"
            self._attribute_value = py_obj
        elif issubclass(obj_class, models.Model):
            # Set value as the objects pk
            self._attribute_value = self._attribute_value + "__pk" # The actual field to be referenced here is the FK'd objects pk, not the object itself.
            self._attribute_type = "fk"
            self._attribute_value = py_obj.pk
        elif issubclass(obj_class, float):
            # Set value as a float
            self._attribute_type = "fl"
            self._attribute_value = py_obj
        else:
            raise self._bad_python_value_error(py_obj)

    def _format_value_to_get_parameter_value(self):
        """
        Converts the value to a string to be set as a GET parameter. Some
        manipulation of the data may be necessary in order to correctly convert
        the value from a python object to a string representation of itself.

        It is assumed that self._attribute_type will always be a valid option.
        This is because by the time it gets to this point, it should have
        already been validated.
        """
        if self._attribute_type == "int":
            # Assume value is an int
            return str(self._attribute_value)
        elif self._attribute_type == "str"
            # Convert value to a string.
            return str(self._attribute_value)
        elif self._attribute_type == "bool":
            # Assume value is a boolean.
            return str(int(self._attribute_value))
        elif self._attribute_type == "date":
            # ex: "21/11/06 16:30". Assume value is a string
            return self._attribute_value.strftime("%d/%m/%Y %H:%M")
        elif self._attribute_type == "fk":
            # Assume value is an int
            return str(self._attribute_value)
        elif self._attribute_type == "fl":
            # Assume value is a float
            return str(self._attribute_value)

    def __init__(self, input_method, *args):
        """
        Creates a RestApiGetParameter instance from the given data. This
        constructor supports input in the following formats:
            input_method == 1:
                GET parameter string where the key (in args[0]) is expected to be in
                the format "name::type" and the value (in args[1]) is expected to be
                a string representation that can be converted correctly into it's
                python representation (See self._parse_param_value for format
                info).

            input_method == 2:
                String (in args[0]) that is the key name and a python object
                (in args[1]) (see self._set_value_and_type_from_python_object
                for acceptable types) that will take on the value. The type
                string will also be determined from the object in args[1].

        Each of these input formats is mutually exclusive (Only one input
        format).
        """
        if input_method == 1:
            get_param_key = args[0]
            get_param_value = args[1]
            self._parse(get_param_key, get_param_value)
        elif input_method == 2:
            self._attribute_name = args[0]
            self._set_value_and_type_from_python_object(args[1])

    def format(self):
        """
        Return the key and value in a tuple in that order. The key and value are
        string representations of themselves that are ready to be used in GET
        parameters and converted back to a RestApiGetParameter object.
        """
        return "{0}::{1}".format(self._attribute_name, self._attribute_type), "{0}".format(self._value_to_get_parameter_value())

    def key_value(self):
        """
        Returns this parameter as a key_value entry. This is used for the actual
        querying using this instance. This is ready to be sent as a kwarg to any
        model filter.
        """
        return {self._attribute_name: self._attribute_value}

class ApiView(View):
    """
    Provides commonly used functionality for api views. This includes things
    such as validation of requests and other things.

    Fields:

        allowed_methods - tuple of strings
            List of verbs that this view can accept. Any requests made for this view
            must be made with a method contained in this list.

            For example, if this list only allows "PUT" and "GET" but the request was
            made with a "POST" verb, then that request should not be processed.

            The possible verbs for this are POST, GET, PUT, and DELETE
    """

    allowed_methods = ()

    def dispatch(self, request, *args, **kwargs):
        """
        Override of the super classes dispatch.
        This implementation of dispatch validates the method of the request.

        If the method verb is not allowed for this view based on the
        allowed_methods, then the 400 error in respond_bad_request_verb is
        returned and the view does not go any further than this method. This
        way, requests with verbs that are not allowed are not processed.
        """
        if not self.valid_method():
            return respond_bad_request_verb(self.request)
        else:
            return super(ApiView, self).dispatch(request, *args, **kwargs)

    def valid_method(self):
        """
        Simple wrapper for calling valid_method from this module, sending it
        self.request and self.allowed_methods by default.
        """
        return valid_method(self.request, self.allowed_methods)

class ModelCrudApiView(ApiView):

    model = None

    instance_pk = 0

    def dispatch(self, request, *args, **kwargs):
        """
        Override of the super classes dispatch.
        This implementation simply gets the pk from the url parameters and sets
        it to the attribute instance_pk.

        If no pk is supplied to the url, then the attribute instance_pk defaults
        to 0.

        This is optional because the request may be trying to create a new
        object, not retreive an existing one. In that case, a pk would not be
        sent to the url parameters.
        """
        self.instance_pk = kwargs.get("pk", 0)
        return super(ModelCrudApiView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Retreives the object from the database that is of the type designated by
        self.model and has the id of self.instance_pk.

        If no object with those conditions is found, then a 404 error is thrown.
        """
        return get_object_or_404(self.model, pk=self.instance_pk)

    def get_object_json(self):
        """
        Simply gets the views object using self.get_object and returns its
        implementation of the json method.
        """
        return self.get_object().json()

    def get_object_list(self, queries):
        pass

    def get(self, request, *args, **kwargs):

        return IanmannJsonResponse(self.get_object_json())
