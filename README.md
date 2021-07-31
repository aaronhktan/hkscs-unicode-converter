# hkscs-unicode-converter

**hkscs-unicode-converter** is a utility for converting HKSCS characters assigned to Private Use Areas of Unicode to their equivalents in Unicode 4.1 onwwards.

```python
>>> from hkscs_unicode_converter import converter
>>> converter.convert_string("亂廿四") # Convert an entire string
'亂噏廿四'
>>> converter.convert_char("") # Convert a single character
'嘅'
>>> converter.convert_char(chr(0xE7D4)) # Convert from codepoint
'啱'
>>> converter.convert_char("\uE7D4") # Convert from Unicode literal
'啱'
>> hex(ord(converter.convert_char(chr(0xE7D4)))) # Get corresponding codepoint
'0x5571'
```

## Installing

hkscs-unicode-converter is available on PyPI and officially supports Python 3.7+:

```console
$ python3 -m pip install hkscs-unicode-converter
```

## Tests

Tests are located in the hkscs_unicode_converter submodule. Testing uses [tox](https://tox.readthedocs.io/en/latest/) to automate environment management and the built-in [unittest](https://docs.python.org/3/library/unittest.html) framework to run tests.

```console
$ tox
```

## Style Guide

Run [black](https://github.com/psf/black) before committing to master!