import sys
import StringIO
from xmlcommandparser.document import XmlDocument
from xmlcommandparser.parser import XmlCommandParser
from xmlcommandparser.exceptions import InvalidCommandException
from xmlcommandparser.helpers import xmlcommand

class Shop(object):
    """Dummy shop lookup, this would be replace by query to db or something similar"""
    shops = {36:'My Beautiful shop', 12:'My Awesome Shop'}
    def findById(self, shopid):
        return self.shops[shopid]

class MyParser(XmlCommandParser):
    shop = None
    def apply_formatter(self, fmt, value):
        if fmt == '{shop}':
            shopid = None
            if not self.shop:
                self.shop = Shop()
                try:
                    shopid = int(value)
                except Exception as err:
                    errmsg = 'Invalid value {} for {}, must be an integer. '
                    raise InvalidCommandException(errmsg.format(value, fmt))

                try:
                    return self.shop.findById(shopid)
                except KeyError as err:
                    errmsg = 'Invalid shop id {} for {}. Not found'
                    raise InvalidCommandException(errmsg.format(value, fmt))
        else:
            errmsg = 'Formatter {} not found. Maybe you should extends the XmlCommandParser class'
            raise NotImplementedError(errmsg.format(fmt))


class ReceiptPrinter(object):
    def __init__(self):
        self.rows = []
        self.header = StringIO.StringIO()
        self.last_seen = 0
        self.grandtotal = 0
        
    def add_row(self, desc, amount=0, align="left"):
        self.rows.append((desc, amount, align))
        
        if amount:
            self.grandtotal += amount

    @xmlcommand
    def heading(self, txt, align="left"):
        self.header.writelines([self.format_row(txt, align=align), "\n"])
        
    @xmlcommand
    def row(self, desc, amount, align="left"):
        self.add_row(desc, amount, align)

    def format_row(self, desc, amount=None, align="left"):
        if align == "left":
            alignattr = 'ljust'
        elif align == "right":
            alignattr = 'rjust'
        else:
            alignattr = 'center'

        if amount:
            return "{desc}{amount:>12.2f}".format(desc=getattr(desc, alignattr)(30), amount=amount)
        else:
            return "{desc}".format(desc=getattr(desc, alignattr)(42))
    
    @xmlcommand
    def subtotal(self, label="Subtotal:"):
        rows = self.rows[self.last_seen:]
        total = 0
        for row in rows:
            desc, amount, align = row
            total += amount
            
        self.add_row('_'*42, amount=None)

        self.rows.append((label, total, 'right'))
        self.last_seen = len(self.rows)            
    
    @xmlcommand
    def total(self, label="Total:"):
        self.add_row('_'*42, amount=None)
        self.rows.append((label, self.grandtotal, 'right'))
        

class MyDocument(XmlDocument):
    def render(self):
        printer = ReceiptPrinter()
        parser = self.get_parser()
        parser.parse_commands('body', printer)

        sys.stdout.write(printer.header.getvalue())
        for desc, amount, align in printer.rows:
            formatted_row = printer.format_row(desc, amount, align)
            sys.stdout.write(formatted_row)
            sys.stdout.write("\n")    

if __name__ == '__main__':
    import os, sys
    document_args = {
        'number': 1,
        'date': '2017-12-08',
        'operator': 'John Doe',
        'coupon': {
            'code': 'ABC-123',
            'amount': -15
        },
        'items': [
            ('First item', 1),
            ('Second item', 2),
            ('Third item', 3),
            ('Fourth item', 10),
            ('Fifth item', 20)
        ]
    }
    doc = MyDocument(path='.', name='formatter.xml', args=document_args, parser=MyParser)
    doc.render()
