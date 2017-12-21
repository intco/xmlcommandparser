import sys
import StringIO
from xmlcommandparser.document import XmlDocument
from xmlcommandparser.helpers import xmlcommand

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
    doc = MyDocument(path='.', name='simple.xml', args=document_args)
    doc.render()
