"""
A bridge between an xml document (formerly a jinja2 template) and a python object
"""
from jinja2 import Environment, FileSystemLoader
from xmlcommandparser.parser import XmlCommandParser
from xmlcommandparser.helpers import tojson, sanitize_filepath

class LoaderWithMacro(FileSystemLoader):
    """Custom jinja2 loader that injects macro from string"""
    def __init__(self, searchpath, encoding='utf-8', macro=""):
        super(LoaderWithMacro, self).__init__(searchpath, encoding)
        self.macro = macro

    def get_source(self, environment, template):
        """ .. see http://jinja.pocoo.org/docs/2.10/api/#loaders"""
        source_tuple = super(LoaderWithMacro, self).get_source(environment, template)
        source_with_macro = self.macro+source_tuple[0]
        return (
            source_with_macro,
            source_tuple[1],
            source_tuple[2]
        )

class XmlDocument(object):
    """An instance of XmlDocument is a bridge between an xml document and a python object"""
    # pylint: disable=too-many-instance-attributes,too-many-arguments,line-too-long
    def __init__(self, path, name, args=None, filters=None, macro="", parser=None, loader=None):
        """:param str: path the path to the jinja2 templates folder
        :param str: name template name to parse
        :param dict: args template args
        :param dict: filters custom filters for the template
        :param str: macro custom macro for the template
        :param XmlCommandParser: parser which parser must be used to parse the commands
        :param jinja2.BaseLoader: loader jinja2 loader to use

            .. see also: http://jinja.pocoo.org/docs/2.10/api/#loaders
        """

        if not parser:
            parser = XmlCommandParser

        if not loader:
            loader = LoaderWithMacro

        self.document_args = args
        self.document_path = path
        self.document_name = name
        self.filters = filters
        self.source = ''
        self.macro = macro
        self.env_loader = loader
        self.parser_obj = parser
        self.parser = None
        self.env = None

    def get_environment(self):
        """builds and return the jinja2 environment using the provided :self.loader:
        the default loader adds filters and macro
        :return: jinja2.Environment instance
        """
        loader = self.env_loader(self.document_path, macro=self.macro)
        self.env = Environment(loader=loader, autoescape=True, trim_blocks=True, lstrip_blocks=True)
        self.env.filters['tojson'] = tojson
        self.env.filters['filepath'] = sanitize_filepath

        if self.filters:
            self.env.filters.update(self.filters)

        return self.env

    def get_parser(self):
        """
        creates and return an instance of the provided :self.parser:
        :return: a self.parser instance
        """
        env = self.get_environment()
        tmpl = env.get_template(self.document_name)

        if not self.document_args:
            self.document_args = {}

        self.source = tmpl.render(**self.document_args)
        self.parser = self.parser_obj(self)
        return self.parser
