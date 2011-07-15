"""
InputValidation.py: contains implementation of the input validation
functionality used in pycanlib.

Copyright (C) 2010 Dynamic Controls

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact details
---------------

Postal address:
    Dynamic Controls
    17 Print Place
    Addington
    Christchurch 8024
    New Zealand

E-mail: bpowell AT dynamiccontrols DOT com
"""
import types

class InputValidationError(Exception):
    def __init__(self, parameter_name, parameter_value, function_name, reason):
        self.__parameter_name = parameter_name
        self.__parameter_value = parameter_value
        self.__function_name = function_name
        self.__reason = reason

    @property
    def parameter_name(self):
        return self.__parameter_name

    @property
    def parameter_value(self):
        return self.__parameter_value

    @property
    def function_name(self):
        return self.__function_name

    @property
    def reason(self):
        return self.__reason

    def __str__(self):
        return "Bad parameter '%s' (%s, type %s) to function '%s' - reason '%s'" % (self.parameter_name, self.parameter_value, type(self.parameter_value), self.function_name, self.reason)

class ParameterTypeError(InputValidationError):
    pass

class ParameterRangeError(InputValidationError):
    pass

class ParameterValueError(InputValidationError):
    pass

def verify_parameter_type(function, parameter_name, parameter_value, allowable_types):
    if not isinstance(parameter_value, allowable_types):
        raise ParameterTypeError(parameter_name, parameter_value, function, ("Not one of the allowable types %s" % (allowable_types,)))
    return True

def verify_parameter_list_type(function, parameter_name, list_parameter_value, allowable_types):
    if not isinstance(list_parameter_value, list):
        raise ParameterTypeError(parameter_name, list_parameter_value, function, ("Not a list"))
    else:
        return all(verify_parameter_type(function, parameter_name+'[%d]'%i, obj, allowable_types) for (i, obj) in enumerate(list_parameter_value))

def verify_parameter_range(function, parameter_name, parameter_value, allowable_range):
    if parameter_value not in allowable_range:
        raise ParameterRangeError(parameter_name, parameter_value, function, ("Not in the allowable range %s" % (allowable_range,)))

def verify_parameter_min_value(function, parameter_name, parameter_value, min_value):
    if parameter_value < min_value:
        raise ParameterRangeError(parameter_name, parameter_value, function, ("Value less than minimum of %s" % (min_value,)))

def verify_parameter_max_value(function, parameter_name, parameter_value, max_value):
    if parameter_value > max_value:
        raise ParameterRangeError(parameter_name, parameter_value, function, ("Value greater than maximum of %s" % (max_value,)))

def verify_parameter_value_in_set(function, parameter_name, parameter_value, allowable_set):
    if parameter_value not in allowable_set:
        raise ParameterValueError(parameter_name, parameter_value, function, ("Value not in allowable set %s" % (allowable_set,)))

def verify_parameter_value_equal_to(function, parameter_name, parameter_value, allowable_value):
    verify_parameter_value_in_set(function, parameter_name, parameter_value, [allowable_value])
