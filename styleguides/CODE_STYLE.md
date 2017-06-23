## TODO:
### Sections:
Naming ==> Files/Modules ==> urls.py
Organization ==> Files/Modules ==> urls.py

## How to use this:
Headings represent sections. Some sections here reference other sections. To
denote the path to a section, use ==> to point to a subsection. For example,
if the reference is "Organization ==> Files", then it can be assumed that "Files"
is a subsection in "Organization".

## APIs

### Module locations

*urls.py location*
Each API interface should have its own url file. For example, if you are adding
a REST API, the url file for that API should be called rest_api_urls and should
be placed in the urls package in the API's corresponding app. See
"File Organization ==> urls.py" for more information on this.

All urls that are used as API calls should be in these url files. For example,
any REST API urls should be in the file "myapp/urls/rest_api_urls" (see
Naming ==> Files/Modules ==> urls.py).

*views.py location*
Each API interface should have its own url file. For example, if you are adding
a REST API, the url file for that API should be called rest_api_urls and should
be placed in the urls package in the API's corresponding app. See
"Organization ==> Files/Modules ==> urls.py" for more information on this.

### Format of API requests
Any requests made to an API should utilize appropriate request verbs (GET, POST,
PUT, etc...).

The usage for each verb is as follows:

*GET*
Used when the client is only asking to view data. No major changes
(besides minor adjustments) should be made in the database for this verb.

*PUT*
Used when the user is trying to create a resource such as a profile or
an item.

This is only used if the user specifically meant for a resource to be
created. For example, if it is assumed that the user doesn't know that a profile
will create an account object, then the API request to create that account
should be a POST request.

*POST*
Used when the server needs to process data and do something on the backend with
it.

This is also used when a resource need to be created or deleted but it is
assumed that the user either doesn't care or know about this action.

See the PUT method usage above for an example of this.

If the request can fit in both PUT and another verb, then it should be a POST
request.

*DELETE*
Used when the user requests that a resource is deleted. Again, this is only if
the user specifically just wants to delete a resource such as an order. Patments
for that order should be deleted in POST requests because the user doesn't care
about that being deleted.

### Format of API response
Any requests made to an API view should be in json format. to implement this,
views in the API views module should always return a JsonResponse.

### API views

*ApiView class based views*
This is a class based view that provides commonly used functionality for an API.

All API views should extend this class. For consistancy sake, this includes API
views that are tiny. Even if it seems unnecessary, the view should extend this
class.

### JSON Representations

*json() method*
Most models will have a method called json(). Any model object that is to be
returned to the client in json format should provide this method for serializing
the object into json format.

This method MUST return a key: value pair with only the following types:
* All keys MUST be strings
* Values can be
  * strings
  * dictionaries
  * ints
  * floats
  * booleans

Any other value types must be converted into a string representation of
themselves.

If this is not done, the JsonResponse instantiation for that json object will
not be converted to json. An error will be thrown instead when that response is
instantiated.
