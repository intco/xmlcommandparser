## Hooks

While processing the XML document the parser calls some hooks.

You can implement the hooks by adding methods whose names matches the hook name to your Business Logic class

Browse the `samples` folder and launch the `beforeaftercommands.py` example inside the `beforeaftercommands` folder. [More information](../samples/beforeaftercommands/README.md)

There are four predefined hooks:

#### before_commands
Called when a section is about to be processed. Its signature is `def before_commands(self, container)`:

|Argument|Type|Description|
|---|---|---|
|`container`|`lxml.etree._Element`|the section about to be processed|
|*return value*||__no return value is expected__|

#### before_command
Called when a command is about to be processed. Its signature is `def before_command(self, container, element, kwargs)`:

|Argument|Type|Description|
|---|---|---|
|`container`|`lxml.etree._Element`|the section of the command about to be processed|
|`element`|`lxml.etree._Element`|the command about to be processed|
|`kwargs`|`dict`|attributes of the `element` already formatted|
|*return value*|`dict`|the `kwargs` to be passed to the Business Logic class|

#### after_command
Called after a command was processed. Its signature is `def after_command(self, container, element, kwargs)`:

|Argument|Type|Description|
|---|---|---|
|`container`|`lxml.etree._Element`|the section of the command about to be processed|
|`element`|`lxml.etree._Element`|the command about to be processed|
|`kwargs`|`dict`|attributes of the `element` already formatted|
|*return value*||__no return value is expected__|

#### after_commands
Called after all commands in a section were processed. Its signature is `def after_commands(self, container)`:

|Argument|Type|Description|
|---|---|---|
|`container`|`lxml.etree._Element`|the section about to be processed|
|*return value*||__no return value is expected__|
