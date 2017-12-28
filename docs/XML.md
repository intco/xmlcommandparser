# XML formatters

Since Python is strongly typed we need a way to perform data types casting. Here come the formatters.

Formatters are implemented using xml namespaces. There are four predefined formatters:

- int: if your method requires an int 
- float: if your method requires a float 
- json: if your method requires any of other types (bool, list, dict) 
- path: converts a relative path to an absolute path.

```xml
<mydocument xmlns:int="int" xmlns:json="json" xmlns:float="float" xmlns:path="path">

</mydocument>
```

To getting started see the [`simple/simple.py` example](../samples/simple/README.md)

For more information on how to write your own formatter [the `formatters/formatter.py` example](../samples/formatters/README.md)
