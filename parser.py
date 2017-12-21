"""An xml parser able to bind xml tags to an object methods"""
# pylint: disable=line-too-long
import re
from lxml import etree
from xmlcommandparser.helpers import fromjson, sanitize_filepath
from xmlcommandparser.exceptions import InvalidCommandException, InvalidAttrException, InvalidSourceException, InvalidFormatterSpecified

class XmlCommandParser(object):
    """An xml parser that acts as a bridge between xml tags and python methods"""
    def __init__(self, document):
        try:
            self.root = etree.fromstring(document.source)
        except Exception as err:
            errmsg = "-- Invalid source -- \n-- SOURCE START --\n{source}\n-- SOURCE END --\n{err}"
            raise InvalidSourceException(errmsg.format(source=document.source, err=err))

        self.document = document
        self.formatters = ['{int}', '{json}', '{float}', '{path}']

    def parse_commands(self, root_tag, obj):
        """Parse children of the specified :root_tag: element

        :param str: root_tag tag to parse (e.g. 'body')
        :param object: obj object whose methods can be used as xml tags
        """
        container = self.root.find(root_tag)

        if hasattr(obj, 'before_commands'):
            obj.before_commands(container=container, parent=root_tag)

        for command in container.getchildren():
            fnc = getattr(obj, command.tag, None)

            if not hasattr(fnc, '__xmlcommand__'):
                raise InvalidCommandException('Invalid command {}, does not match any callables'.format(command.tag))

            kwargs = self.normalize_xml_attributes(command)

            if hasattr(obj, 'before_command'):
                kwargs = obj.before_command(container=container, parent=root_tag, element=command, kwargs=kwargs)

            if fnc:
                try:
                    fnc(**kwargs)
                except Exception as err:
                    errmsg = "Error parsing command: {tag} with args {args}. {err}"
                    raise InvalidCommandException(errmsg.format(tag=command.tag, args=kwargs, err=err))
            else:
                raise InvalidCommandException("Invalid command: {tag} not found".format(tag=command.tag))

            if hasattr(obj, 'after_command'):
                obj.after_command(container=container, parent=root_tag, element=command, kwargs=kwargs)


        if hasattr(obj, 'after_commands'):
            obj.after_commands(container=container, parent=root_tag)

    def normalize_xml_attributes(self, element):
        """removes the namespace from the attribute name"""
        # pylint: disable=unused-variable
        attrs = {}
        for attrname, attrvalue in element.attrib.iteritems():
            attrname = attrname[attrname.find('}')+1:]
            # do not use attrvalue here
            attrs[attrname] = self.get_xml_attr(element, attrname)

        return attrs

    def get_xml_attr(self, element, attrname):
        """parse attribute value using the namespace"""
        attrvalue = element.get(attrname)
        if attrvalue:
            return attrvalue
        else:
            # has a namespace
            regex = re.compile(r'(^\{.*\})('+attrname+')')
            for name, value in element.attrib.iteritems():
                match = regex.search(name)
                if match:
                    attrkey = match.group(0)
                    formatter = match.group(1)
                    value = element.get(attrkey)
                    return self.apply_ns_format(formatter, value)

        raise InvalidFormatterSpecified('Can not parse value for {}'.format(attrname))

    def apply_ns_format(self, fmt, value):
        """format attribute value using the formatter specified in the namespace"""
        if fmt == '{int}':
            try:
                return int(value)
            except Exception as err:
                errmsg = "Can not parse {value} as int: {err}"
                raise InvalidAttrException(errmsg.format(value=value, err=err))
        elif fmt == '{json}':
            try:
                value = fromjson(value)
                try:
                    return value % self.document.document_args
                except TypeError:
                    return value
            except ValueError as err:
                errmsg = "Can not parse {value} as json: {err}"
                raise InvalidAttrException(errmsg.format(value=value, err=err))
        elif fmt == '{float}':
            try:
                return float(value)
            except Exception as err:
                errmsg = "Can not parse {value} as float: {err}"
                raise InvalidAttrException(errmsg.format(value=value, err=err))
        elif fmt == '{path}':
            try:
                return sanitize_filepath(self.document.env, value)
            except Exception as err:
                errmsg = "Can not parse {value} as path: {err}"
                raise InvalidAttrException(errmsg.format(value=value, err=err))
        else:
            return self.apply_formatter(fmt, value)

    def apply_formatter(self, fmt, value):
        # pylint: disable=unused-argument,no-self-use
        """extends this to use custom formatters"""
        errmsg = 'Formatter {} not found. Maybe you should extends the XmlCommandParser class'
        raise NotImplementedError(errmsg.format(fmt))
