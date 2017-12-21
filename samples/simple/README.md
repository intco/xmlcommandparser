## Getting Started example

The `simple.py` example contains all the minimum code required in order to getting started. Simply `cd` to the `simple` directory and run python `simple.py`.

The `simple` example illustrates basic usage of the module as a receipt printer to `sys.stodut`.

There are two main classes (`MyDocument` and `ReceiptPrinter`) and a jinja2 template (`simple.xml`)

### MyDocument

The `MyDocument` class loads the `simple.xml` file as jinja2 template then render it using the provided `document_args` and finally applies all the commands from the `ReceiptPrinter` class.
Once done prints the result on `sys.stdout`.

### ReceiptPrinter

The `ReceiptPrinter` class contains all the commands that can be used in the `simple.xml` file. Each method that can be used as command is marked with the `@xmlcommand` decorator.

### simple.xml

The xml file is just a jinja2 template, it can contains filters, macros and all awesome stuff of jinja2. Once parsed from the jinja2 engine the xml document will be processed by the xml parser. For each tags recognized as command the parser will run the corresponding method.