## Custom formatters

The `formatters.py` example show how to provide a custom formatter. It is based on the `simple.py` code so be sure to give it a look before reading on.

In order to write your own formatter you should follow these simple steps:

#### 1. Add the appropriate namespace to the xml root element

Add the `xmlns:<formatname>` attribute to the root element of your xml file (`xmlns:shop` in the example)

#### 2. Prepend the namespace to the attribute you wish to format

The line `<heading shop:txt="12" />` tells the parser to apply the `{shop}` formatter before invoking the `heading` method

#### 3. Write your formatting method

Subclass the `XmlCommandParser` class and add your formatting logic to the `apply_formatter` method (see the `MyParser` class)

#### 4. Pass your custom parser to the `XmlDocument` instance

The line `doc = MyDocument(path='.', name='formatter.xml', args=document_args, parser=MyParser)`