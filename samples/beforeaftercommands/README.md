## Hooks example

The `beforeaftercommands.py` example show how the parser calls hooks during processing. It is based on the `simple.py` code so be sure to give it a look before reading on.

The example uses all the available hooks to provide the following features:

- using the `before_commands` hook prints the count of the elements inside each section
- using the `before_command` hook formats the headings following these rules:
    - if in body make it capitalize()'d
    - if in header make it upper()'d
    - if in footer make it lower()'d
- using the `after_command` hook counts how many headings are in each section
- using the `after_commands` hook prints how many headings are in each section

Take a look at the source code for more details