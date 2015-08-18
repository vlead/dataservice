# module to hold all utilities/helper functions

import json

from flask import make_response


# return a list of dicts as json with correct mime types
# flask does not provide a jsonify for lists; hence this method
def jsonify_list(data):
    if type(data) is not list:
        raise Exception('jsonify_list function accepts only a list')

    return make_response(json.dumps(data), 200,
                         {'content-type': 'application/json'})


# take in a flask request object and try to parse out a dictionary from the
# request
# try to find if request is as JSON first, then look into forms, finally force
# find it.
# If not found return a dict; else return the parsed data
def parse_request(request):
    if request.json:
        # print 'found in request.json'
        data = request.get_json()

    elif request.data:
        # print 'found in request.data'
        data = json.loads(request.data)

    elif request.form:
        # print 'found in request.form'
        data = request.form.to_dict()
        # try to detect if form contains integers and boolean data and attempt
        # to convert them
        # FIXME: is this a good idea? Fix this to do it in a better way?
        for k in data:
            if is_number(data[k]):
                data[k] = int(data[k])
            if is_bool_in_str(data[k]):
                data[k] = str_to_bool(data[k])

            # print k, data[k]

    else:
        data = request.get_json(force=True)

    if not data:
        return False

    return data


# check if a given string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# check if in a given string python bool types are represented
def is_bool_in_str(s):
    if s == "True" or s == "False":
        return True
    return False


# convert python bool types in string to native bool types
def str_to_bool(s):
    if s == "True":
        return True
    if s == "False":
        return False
    return None


# decorator to do typechecking of arguments passed to functions
# usage: @typecheck(var1=<type>, var2=<type>, ..)
#        def yourfunc(var1, var2, ..):
#           ....
def typecheck(**typemap):
    # print "all valid types: %s" % typemap

    def make_wrapper(decorated_func):

        def wrapper(*arg_vals, **kw_vals):
            arg_names = decorated_func.func_code.co_varnames
            # print arg_names
            # print args
            for arg_name in arg_names:
                idx = arg_names.index(arg_name)
                arg = arg_vals[idx]
                # print "arg_name: %s, arg: %s, typemap[arg_name]: %s" %\
                #    (arg_name, arg, typemap[arg_name])
                if not isinstance(arg, typemap[arg_name]):
                    print "types are not fine"
                    raise TypeError("For %s type should have been %s. But "
                                    "provided: %s" % (arg_name,
                                                      typemap[arg_name],
                                                      type(arg)))

            return decorated_func(*arg_vals, **kw_vals)
        return wrapper

    return make_wrapper
