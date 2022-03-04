from typing import List, Union, Tuple
import os

from symbtabhelp import SymbolTableBase

# bool not required since already converted to TYPE_INTEGER
TYPE_FLOAT = ["FLOAT", "DOUBLE", "LONG DOUBLE"]
TYPE_CHAR = [
    "CHAR",
    "SIGNED CHAR",
    "UNSIGNED CHAR",
]
TYPE_INTEGER = [
    "SHORT",
    "SHORT INT",
    "SIGNED SHORT",
    "SIGNED SHORT INT",
    "UNSIGNED SHORT",
    "UNSIGNED SHORT INT",
    "INT",
    "SIGNED INT",
    "UNSIGNED INT",
    "SIGNED",
    "UNSIGNED",
    "LONG",
    "LONG INT",
    "SIGNED LONG INT",
    "SIGNED LONG",
    "UNSIGNED LONG",
    "UNSIGNED LONG INT",
    "LONG LONG",
    "LONG LONG INT",
    "SIGNED LONG LONG",
    "SIGNED LONG LONG INT",
    "UNSIGNED LONG LONG",
    "UNSIGNED LONG LONG INT",
]
PRIMITIVE_TYPES = TYPE_CHAR + TYPE_FLOAT + TYPE_INTEGER
SIZE_OF_TYPE = {
    "VOID": 0,
    "CHAR": 4,  # Char is not 4 bytes, but this allows us to support all
    # unicode characters and also prevents potential alignment
    # issues
    "SIGNED CHAR": 4,
    "UNSIGNED CHAR": 4,
    "SHORT": 2,
    "SHORT INT": 2,
    "SIGNED SHORT": 2,
    "SIGNED SHORT INT": 2,
    "UNSIGNED SHORT": 2,
    "UNSIGNED SHORT INT": 2,
    "INT": 4,
    "SIGNED INT": 4,
    "UNSIGNED INT": 4,
    "SIGNED": 4,
    "UNSIGNED": 4,
    "LONG": 8,
    "LONG INT": 8,
    "SIGNED LONG INT": 8,
    "SIGNED LONG": 8,
    "UNSIGNED LONG": 8,
    "UNSIGNED LONG INT": 8,
    "LONG LONG": 8,
    "LONG LONG INT": 8,
    "SIGNED LONG LONG": 8,
    "SIGNED LONG LONG INT": 8,
    "UNSIGNED LONG LONG": 8,
    "UNSIGNED LONG LONG INT": 8,
    "FLOAT": 4,
    "DOUBLE": 8,
    "LONG DOUBLE": 16,
}
ERROR_MESSAGES = []
WARNING_MESSAGES = []


def error(err):
    global ERROR_MESSAGES
    ERROR_MESSAGES.append(err)
    return err


def warn(err):
    global WARNING_MESSAGES
    WARNING_MESSAGES.append(err)
    return err


def type_conversion(converted_from, converted_to):
    if converted_from == converted_to:
        return converted_from
    if (converted_from not in PRIMITIVE_TYPES) or (converted_to not in PRIMITIVE_TYPES):
        error(f"ERROR not in primitive types {converted_from}  or {converted_to}")
        return None
    if (converted_from in TYPE_FLOAT and converted_to not in TYPE_FLOAT) or SIZE_OF(
        converted_from
    ) > SIZE_OF(converted_from):
        warn(f"EXPLICIT type conversion posssible loss in data")
    return converted_to

