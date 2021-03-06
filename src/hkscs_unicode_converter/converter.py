import csv
import importlib.resources as pkg_resources
import json

from . import data

with pkg_resources.open_text(data, "config.json") as config:
    _files = json.load(config)


def _format_key_value_pair(key, value):
    if (not key or not value) or (key == value):
        return (None, None)

    # Strip off "U+" from the start of the keys and values
    if key.startswith("U+"):
        key = key[2:]
    if value.startswith("U+"):
        value = value[2:]

    values = tuple([value])

    # Special case for Ê̄, Ê̌, ê̄, ê̌ (<00CA,0304>, <00CA,030C>, <00EA,0304>, <00EA,030C>)
    # Strip the "<" and ">" characters, then put each codepoint in the list
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
        values = tuple(value.split(","))

    return (key, values)


def _create_mapping(items, columns_from, column_to):
    # Each key in this mapping should be a single codepoint, represented as all-caps hexadecimal string with no prefix
    # Each value should be a list of corresponding codepoints (represented the same way as the keys)
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
        item = {}
        for index, value in enumerate(row):
            if index >= len(headers):
                break
            item[headers[index]] = value
        items.append(item)

    return items


_mappings = []
# Start parsing the data files
for file in _files:
    # Each of the _process methods should return a list of dicts
    # Each dict represents a row; each key in the dict is the column name
    with pkg_resources.open_text(data, f'{file["name"]}.{file["type"]}') as f:
        if file["type"] == "tsv":
            items = _process_tsv(f)
        else:
            items = json.load(f)

    # There might be multiple columns that we are interested in converting FROM
    # (e.g. in HKSCS2004,
    #  we want both ISO/IEC_10646-1:2000 -> ISO/IEC_10646:2003_Amendment AND
    #  ISO/IEC_10646-1:1993 -> ISO/IEC_10646:2003_Amendment)
    columns_from = file["config"]["column_from_keys"]
    column_to = file["config"]["column_key_to"]

    _mappings.append(_create_mapping(items, columns_from, column_to))


def convert_char(char):
    if not isinstance(char, str):
        raise TypeError("char argument must be str type")

    if len(char) > 1 or len(char) <= 0:
        raise ValueError("char argument must be exactly length 1")

    # Get the hex version of the codepoint for this char, without the "0x" prefix
    original_codepoint = "%X" % ord(char)

    # Find the matching codepoints from the loaded data files
    # Must loop through each of the files, because a codepoint may be remapped twice
    # e.g. EC77 (GCCS) -> 4CA4 (HKSCS-1999) -> 9FD0 (HKSCS-2016)
    matched = original_codepoint
    for mapping in _mappings:
        if matched in mapping:
            matched = mapping[matched]
            if len(matched) > 1:  # This should only occur for the <00CA,0304> edgecases
                break
            else:
                matched = matched[0]

    # Leave the character unchanged if no corresponding codepoints are found
    if not matched or matched == original_codepoint:
        return char

    # At this point, there are three possibilities:
    # - matched is a tuple length 2, for sequences like <00CA,0304>
    # - matched is a str length 1 and contains a Unicode literal, e.g. "亠"
    # - matched is a str length > 1, and contains a Unicode codepoint e.g. "39FB"
    if type(matched) is tuple and len(matched) > 1:
        try:
            return "".join([chr(int(codepoint, 16)) for codepoint in matched])
        except:
            return char
    elif type(matched) is str and len(matched) == 1:
        return matched
    elif type(matched) is str and len(matched) > 1:
        try:
            return chr(int(matched, 16))
        except:
            return char

    # Last resort: give up and return the original character
    return char


def convert_string(string):
    if not isinstance(string, str):
        raise TypeError("string argument must be str type")

    return "".join([convert_char(char) for char in string])
