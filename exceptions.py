"""
exceptions raised by the document or the parser
"""
class InvalidPathException(Exception):
    """Exception raised when an invalid path is specified"""

class InvalidCommandException(Exception):
    """Exception raised when an invalid command is specified"""

class InvalidAttrException(Exception):
    """Exception raised when an invalid attribute is specified"""

class InvalidSourceException(Exception):
    """Exception raised when an invalid source is supplied"""

class InvalidFormatterSpecified(Exception):
    """Exception raised when an invalid formatter is specified"""
