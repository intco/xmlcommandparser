import sys
import StringIO
from xmlcommandparser.document import XmlDocument
from xmlcommandparser.helpers import xmlcommand


class InvalidDocument(Exception):
    """Raised when an invalid document is detected"""


class DocumentPrinter(object):
    def __init__(self, parser, row_width=64):
        self.rows = []
        self.header = StringIO.StringIO()
        self.body = StringIO.StringIO()
        self.footer = StringIO.StringIO()
        self.summary = StringIO.StringIO()
        
        self.default_align = 'left'
        self.current_section = None
        self.row_width = row_width
        self.parser = parser
        self.summaryData = {}

    def before_commands(self, container):
        tagname = container.tag
        if tagname in ['header', 'footer', 'body']:
            section_align = self.parser.get_xml_attr(container, 'align')
            children_length = len(container.getchildren())
            if not section_align:
                raise InvalidDocument('Section {} must provide a default align'.format(tagname))
        
            self.default_align = section_align
            self.current_section = tagname
            strheading ='{} ({}) element(s)'.format(tagname.capitalize(), children_length)
            self.heading(strheading, 'left')
        else:
            # other sections are not supported in this example
            # i.e. this code will never run
            self.current_section = None
            self.default_align = None

    def before_command(self, container, element, kwargs):
        """
        heading will be formatted following these rules:
            - if in body make it capitalize()'d
            - if in header make it upper()'d
            - if in footer make it lower()'d
        """
        if element.tag == 'heading':
            if container.tag == 'header':
                kwargs['txt'] = kwargs['txt'].upper()
            elif container.tag == 'footer':
                kwargs['txt'] = kwargs['txt'].lower()
            elif container.tag == 'body':
                kwargs['txt'] = kwargs['txt'].capitalize()
                
        return kwargs
    
    def after_command(self, container, element, kwargs):
        if element.tag == 'heading':
            section = container.tag
            heading_count = self.summaryData.get(section, 0)
            self.summaryData[section] = heading_count+1

    def after_commands(self, container):
        # reset section and align
        self.current_section = None
        self.default_align = None
        
        # write section summary
        section = container.tag
        strmsg = "Section {section} contains {heading_count} headings"
        self.summary.writelines([strmsg.format(section=section, heading_count=self.summaryData[section]), "\n"])

    def format_row(self, desc, align):
        if align == "left":
            alignattr = 'ljust'
        elif align == "right":
            alignattr = 'rjust'
        else:
            alignattr = 'center'

        return "{desc}|".format(desc=getattr(desc, alignattr)(self.row_width))
    
    @xmlcommand
    def heading(self, txt, align=None):
        if not self.current_section:
            raise InvalidDocument('Invalid section detected. Please check the xml template')
        
        if not align:
            if not self.default_align:
                raise InvalidDocument('Something went wrong. Please check the xml template')
            align = self.default_align
            
        section = getattr(self, self.current_section)
        section.writelines([self.format_row(txt, align=align), "\n"])
        

class MyDocument(XmlDocument):
    def render(self):
        parser = self.get_parser()
        # get the row_width from the root element xml
        row_width = parser.get_xml_attr(parser.root, 'row_width')
        if not row_width:
            printer = DocumentPrinter(parser)
        else:
            printer = DocumentPrinter(parser, row_width)
            
        parser.parse_commands('body', printer)
        parser.parse_commands('header', printer)
        parser.parse_commands('footer', printer)
        
        strout = "{header}--\n{body}--\n{footer}--\n{summary}"
        kwargs = {
            'header': printer.header.getvalue(),
            'body': printer.body.getvalue(),
            'footer': printer.footer.getvalue(),
            'summary': printer.summary.getvalue(),
            
        }
        sys.stdout.write(strout.format(**kwargs))

if __name__ == '__main__':
    import os, sys
    document_args = {
        
    }
    doc = MyDocument(path='.', name='beforeaftercommands.xml', args=document_args)
    doc.render()
