import csv
import importlib.resources as pkg_resources
import json

from . import data

_files = [
    {
        "name": "gccs",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "gccs.tsv"),
        "config": {
            "column_from_keys": ["Big5Alternate"],
            "column_key_to": "Unicode",
        },
    },
    {
        "name": "hkscs1999",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "hkscs1999.tsv"),
        "config": {
            "column_from_keys": ["UnicodeAlternate"],
            "column_key_to": "Unicode",
        },
    },
    {
        "name": "hkscs2001",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "hkscs2001.tsv"),
        "config": {
            "column_from_keys": ["UnicodeAlternate"],
            "column_key_to": "Unicode",
        },
    },
    {
        "name": "hkscs2001_2",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "hkscs2001_2.tsv"),
        "config": {
            "column_from_keys": ["ISO/IEC_10646-1:1993", "ISO/IEC_10646-1:2000"],
            "column_key_to": "ISO/IEC_10646-2:2001",
        },
    },
    {
        "name": "hkscs2004",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "hkscs2004.tsv"),
        "config": {
            "column_from_keys": ["ISO/IEC_10646-1:1993", "ISO/IEC_10646-1:2000"],
            "column_key_to": "ISO/IEC_10646:2003_Amendment",
        },
    },
    {
        "name": "hkscs2008",
        "type": "tsv",
        "stream": pkg_resources.open_text(data, "hkscs2008.tsv"),
        "config": {
            "column_from_keys": ["ISO/IEC_10646-1:1993", "ISO/IEC_10646-1:2000"],
            "column_key_to": "ISO/IEC_10646:2003_Amendment",
        },
    },
    {
        "name": "hkscs2016",
        "type": "json",
        "stream": pkg_resources.open_text(data, "hkscs2016.json"),
        "config": {
            "column_from_keys": ["codepoint"],
            "column_key_to": "char",
        },
    },
]


def _format_key_value_pair(key, value):
    if not key or not value:
        return (None, None)

    # Strip off "U+" from the start of the keys and values
    if key.startswith("U+"):
        key = key[2:]
    if value.startswith("U+"):
        value = value[2:]

    # Special case for Ê̄, Ê̌, ê̄, ê̌ (<00CA,0304>, <00CA,030C>, <00EA,0304>, <00EA,030C>)
    # Strip the "<" and ">" characters, then parse each of the codepoints to a Unicode string
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
        values = map(lambda x: int(x, base=16), value.split(","))
        value = "".join([chr(x) for x in values])

    return (key, value)


def _create_mapping(items, columns_from, column_to):
    # Each key in this mapping should be a single codepoint, represented as all-caps hexadecimal string with no prefix
    # Each value should be EITHER a single codepoint represented in the same way as a key, OR a string (like Ê̄)
    mapping = {}

    for item in items:
        for column_from in columns_from:
            key, value = _format_key_value_pair(item[column_from], item[column_to])
            if key and value:
                mapping[key] = value

    return mapping


def _process_tsv(stream):
    items = []

    reader = csv.reader(stream, delimiter="\t")
    headers = next(reader)  # First line contains header titles

    for row in reader:
        data = {}
        for index, value in enumerate(row):
            if index >= len(headers):
                break
            data[headers[index]] = value
        items.append(data)

    return items


_mappings = []
# Start parsing the data files
for file in _files:
    # Each of the _process methods should return a list of dicts
    # Each dict represents a row; each key in the dict is the column name
    if file["type"] == "tsv":
        data = _process_tsv(file["stream"])
    else:
        data = json.load(file["stream"])

    # There might be multiple columns that we are interested in converting FROM
    # (e.g. in HKSCS2004,
    #  we want both ISO/IEC_10646-1:2000 -> ISO/IEC_10646:2003_Amendment AND
    #  ISO/IEC_10646-1:1993 -> ISO/IEC_10646:2003_Amendment)
    columns_from = file["config"]["column_from_keys"]
    column_to = file["config"]["column_key_to"]

    _mappings.append(_create_mapping(data, columns_from, column_to))


def convert_char(char):
    if not isinstance(char, str):
        raise TypeError("char argument must be str type")

    if len(char) > 1 or len(char) <= 0:
        raise ValueError("char argument must be exactly length 1")

    # Get the hex version of the codepoint for this char, without the "0x" prefix
    codepoint = "%X" % ord(char)

    # Find the corresponding value from the loaded data files
    corresponding_value = None
    for mapping in _mappings:
        if codepoint in mapping:
            corresponding_value = mapping[codepoint]

    # Leave the character unchanged if no corresponding codepoint is found
    if not corresponding_value:
        return char

    # The corresponding value might be a character
    # In which case, return it
    if isinstance(corresponding_value, str) and len(corresponding_value) == 1:
        return corresponding_value

    # Otherwise, find the correct character if the returned value is a codepoint
    # (Assume that any string that parses to a hex value is a valid codepoint)
    try:
        return chr(int(corresponding_value, 16))
    except:
        return char


def convert_string(string):
    if not isinstance(string, str):
        raise TypeError("string argument must be str type")

    return "".join([convert_char(char) for char in string])
