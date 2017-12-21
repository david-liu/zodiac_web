# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""
This utils define three function to wrap rest reponse
success_response:
    All went well, and (usually) some data was returned.
    Required Return Keys: status, data

fail_response:
    There was a problem with the data submitted, or some pre-condition of the API call wasn't satisfied
    Required Return Keys: status, data

error_response:
    An error occurred in processing the request, i.e. an exception was thrown
    Required Return Keys: status, message


based on JSend on http://labs.omniti.com/labs/jsend

"""


def success_response(data):
    """ When an API call is successful, the function is used as a simple envelope for the results, 
    using the data key, as in the following:

    {
    	status : "success",
    	data : {
        	"posts" : [
            	{ "id" : 1, "title" : "A blog post", "body" : "Some useful content" },
            	{ "id" : 2, "title" : "Another blog post", "body" : "More content" },
        	]
     }

    required keys:
    	status: Should always be set to "success
    	data: Acts as the wrapper for any data returned by the API call. If the call returns no data (as in the last example), data should be set to null.

	"""

    return {'status': 'success', 'data': data}


def fail_response(data):
    """ When an API call is rejected due to invalid data or call conditions, 
    the function response's data key contains an object explaining what went wrong, 
    typically a hash of validation errors. For example:

    {
    	"status" : "fail",
    	"data" : { "title" : "A title is required" }
	}

    required keys:
    	status: Should always be set to "fail".
    	data: Again, provides the wrapper for the details of why the request failed. If the reasons for failure correspond to POST values, the response object's keys SHOULD correspond to those POST values.

	"""

    return {'status': 'fail', 'data': data}


def error_response(message):
    """ An error occurred in processing the request, i.e. an exception was thrown

    {
    	"status" : "error",
    	"message" : "Unable to communicate with database"
	}

    required keys:
    	status: Should always be set to "error".
		message: A meaningful, end-user-readable (or at the least log-worthy) message, explaining what went wrong.
	
	Optional keys:
		code: A numeric code corresponding to the error, if applicable
		data: A generic container for any other information about the error, i.e. the conditions that caused the error, stack traces, etc.
	
	"""

    return {'status': 'error', 'message': message}
