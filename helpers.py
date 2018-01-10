"""various helper for both the document and the parser"""
import os
import json
from jinja2 import environmentfilter
from xmlcommandparser.exceptions import InvalidPathException

@environmentfilter
def sanitize_filepath(env, value):
    """a jinja2 filter that converts relative to absolute path
    :return: str the absolute path to the resource
    """
    norm_value = os.path.normpath(value)

    for loader_path in env.loader.searchpath:
        abspath = os.path.abspath(loader_path)
        filepath = os.path.join(abspath, norm_value)

        if os.path.isfile(filepath):
            return filepath

    raise InvalidPathException("Path is not a valid filename: {}".format(norm_value))

def tojson(value):
    """converts a value in json format escaping the quote '"' symbol
    :param mixed: value
    :return: str the value in json format
    """

    if hasattr(value, 'replace'):
        value = value.replace('"', '&quot;')

    return json.dumps(value)

def fromjson(value):
    """decode a value from json format escaping the quote '"' symbol
    :param mixed: value
    :return: str the value in json format
    """
    return json.loads(value.replace('&quot;', '"'))

def xmlcommand(fnc):
    """Decorator for marking functions as xml command"""
    fnc.__xmlcommand__ = True
    return fnc

MACRO="""
{%- macro attr_json(key, value) -%}
    json:{{key}}="{{value|tojson}}"
{%- endmacro -%}

{%- macro attr_int(key, value) -%}
   int:{{key}}="{{value|string}}"
{%- endmacro -%}

{%- macro attr_float(key, value) -%}
   float:{{key}}="{{value|string}}"
{%- endmacro -%}

{%- macro attr_path(key, value) -%}
   path:{{key}}="{{value|string}}"
{%- endmacro -%}
"""