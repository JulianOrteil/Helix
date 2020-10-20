# -*- coding: utf-8 -*-

# **********************************************************************
# * Copyright 2020 Julian_Orteil
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *    http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# * implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# **********************************************************************

"""Converts dictionaries to dot notation and vice versa.

Slightly modified version of drgrib's 'DotMap' library to better fit the
specific needs of this application and enhance its functionality.
drgrib's GitHub: https://github.com/drgrib/dotmap

'Maps' is the coversion class that converts dictionaries. It also has a
'parse_ini' function to parse and convert the configparser object to a
dictionary or Maps object.

Importing everything from this module will only import the Maps class
(as defined by the '__all__' attribute).
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function


__all__ = ["Maps"]


import ast
import os
import re
from collections import OrderedDict
from collections.abc import MutableMapping
from configparser import ConfigParser
from inspect import ismethod
from typing import Any, Callable, Generator, Iterable, Iterator, NoReturn, Optional, Tuple, Union


class Maps(MutableMapping):
    """
    Converts a dictionary of key:value pairs into a dotted
    representation of those keys. Normal string representation of
    keys is still accessible via normal dictionary indexing.

    Note:
        If a key contains non-alphanumeric characters
        (!@#$%, etc, including spaces), they will be replaced with
        an underscore (_).

    Examples:
        >>> # Normal usage
        >>> test = {"hello": "world"}
        >>> print(Maps(test))

        Output: Maps(hello="world")

        >>> test = {"hello": "world"}
        >>> maps = Maps(test)
        >>> print(maps.hello)

        Output: "world"

        >>> test = {"hello": "world"}
        >>> maps = Maps(test)
        >>> print(maps["hello"])

        Output: "world"

        >>> # If a dictionary key has non-alphanumeric characters
        >>> # Notice how a series of special characters is replaced
        >>> # by only a single underscore
        >>> test = {"hello joh*&^n": "hi computer"}
        >>> maps = Maps(test)
        >>> print(maps)

        Output: Maps(hello_joh_n="hi computer")

    Raises:
        ValueError:
            An argument is of a legal type but is, or contains, an
            illegal value.
    """

    # Class-level variables
    _dynamic: bool
    _map: OrderedDict

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self._dynamic = True
        self._map = OrderedDict()

        if kwargs:
            for key, value in self._get_items(kwargs):
                key = re.sub('[^0-9a-zA-Z]+', '_', key)
                if key != '_dynamic':
                    self._map[key] = value
                else:
                    self._dynamic = value

        if args:
            dictionary = args[0]

            if not isinstance(dictionary, dict):
                raise ValueError(
                    "object passed to constructor must be of type 'dict': "
                    f"'{type(dictionary).__name__}'"
                )

            # Recursive handling
            tracked_ids = {id(dictionary): self}
            for key, value in self._get_items(dictionary):
                if isinstance(key, str):
                    key = re.sub('[^0-9a-zA-Z]+', '_', key)

                value_id = id(value)
                if isinstance(value, dict):
                    if value_id in tracked_ids:
                        value = tracked_ids[value_id]
                    else:
                        value = self.__class__(value, _dynamic=self._dynamic)
                        tracked_ids[value_id] = value

                if isinstance(value, list):
                    listed_items = []

                    for item in value:
                        temp_item = item
                        if isinstance(item, dict):
                            temp_item = self.__class__(item, _dynamic=self._dynamic)
                        listed_items.append(temp_item)

                    value = listed_items
                try:
                    self._map[key] = ast.literal_eval(value)
                except NameError:
                    if value.lower() == "false":
                        self._map[key] = False
                    elif value.lower() == "true":
                        self._map[key] = True
                    else:
                        self._map[key] = value
                except (SyntaxError, ValueError):
                    # Cannot eval this value
                    self._map[key] = value

    # Dunder methods

    def __add__(self, value: object) -> Union[Any, NoReturn]:
        if self.empty():
            return value
        else:
            self_type = type(self).__name__
            value_type = type(value).__name__
            raise TypeError(f"unsupported operand type(s) for +: '{self_type}' and '{value_type}'")

    def __cmp__(self, value: object) -> Any:
        value = Maps.parse_value(value)
        return self._map.__cmp__(value)

    def __contains__(self, name: str) -> bool:
        return self._map.__contains__(name)

    def __copy__(self) -> Maps:
        return self.__class__(self)

    def __deepcopy__(self) -> Maps:
        return self.copy()

    def __delitem__(self,
                    key: str,
                    dict_delitem: Optional[Callable[..., Any]] = dict.__delitem__) -> Any:
        return self._map.__delitem__(key, dict_delitem=dict_delitem)

    def __dir__(self) -> Iterable:
        return self.keys()

    def __eq__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        if not isinstance(value, dict):
            return False
        return self._map.__eq__(value)

    def __ge__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        return self._map.__ge__(value)

    def __gt__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        return self._map.__gt__(value)

    def __iter__(self) -> Iterable:
        return self._map.__iter__()

    def __le__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        return self._map.__le__(value)

    def __len__(self) -> int:
        return self._map.__len__()

    def __lt__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        return self._map.__lt__(value)

    def __ne__(self, value: Any) -> bool:
        value = Maps.parse_value(value)
        return self._map.__ne__(value)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        items = []

        for key, value in self._get_items(self._map):

            # Recursive assignment case
            if id(value) == id(self):
                items.append("{0}={1}(...)".format(key, self.__class__.__name__))
            else:
                items.append("{0}={1}".format(key, repr(value)))

        joined = ", ".join(items)
        return "{0}({1})".format(self.__class__.__name__, joined)

    def __delattr__(self, name: str) -> None:
        self._map.__delitem__(name)

    def __getattr__(self, name: str) -> Any:
        if name in ('_map', '_dynamic', "_ipython_canary_method_should_not_exist_"):
            return super().__getattr__(name)

        try:
            return super(self.__class__, self).__getattribute__(name)
        except AttributeError:
            pass

        return self[name]

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ('_map', '_dynamic', "_ipython_canary_method_should_not_exist_"):
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __getitem__(self, name: str) -> Union[Any, Maps]:
        if (
            name not in self._map and
            self._dynamic and
            name != "_ipython_canary_method_should_not_exist_"
        ):
            self[name] = self.__class__()

        return self._map[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self._map[name] = value

    def __getstate__(self) -> dict:
        return self.__dict__

    def __setstate__(self, value: dict) -> None:
        self.__dict__.update(value)

    # Internal methods

    def _get_items(self, item: Any) -> Iterable:
        if hasattr(item, 'iteritems') and ismethod(getattr(item, 'iteritems')):
            return item.iteritems()
        else:
            return item.items()

    # Public methods

    def clear(self) -> None:
        """Remove all items from the Maps object."""

        self._map.clear()

    def copy(self) -> Maps:
        """Makes a copy of the Maps object in memory."""

        return self.__copy__()

    def empty(self) -> bool:
        """Returns whether the Maps object is empty."""

        return (not any(self))

    @classmethod
    def fromkeys(cls, iterable: Iterable, value: Optional[Any] = None) -> Iterable:
        """Returns a new :obj:`Maps` object with keys supplied from an
        iterable setting each key in the object with :term:`value`.

        Args:
            iterable (:obj:`Iterable`):
                Any iterable.
            value (:obj:`obj`, optional):
                The value to set for the keys.
                Default is :obj:`None`.

        Returns:
            Maps:
                The :obj:`Maps` object.
        """

        maps = cls()
        maps.map = OrderedDict.fromkeys(iterable, value)

        return maps

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Returns the value of 'key'.

        If :term:`key` does not exist, :term:default` is returned
        instead.

        Args:
            key (:obj:`str`):
                The key to get the value needed from the dict.
            default (:obj:`obj`, optional):
                The value to return if :term:`key` does not exist.

        Returns:
            Any:
                The value at :term:`key` or :term:default`.
        """

        return self._map.get(key, default)

    def has_key(self, key: str) -> bool:
        return key in self._map

    def items(self) -> Generator[Tuple[str, Any]]:
        """Returns a generator yielding a (key, value) pair."""

        return self._get_items(self._map)

    def iteritems(self) -> Iterator:
        """
        Returns an iterator over the Maps oject's (key, value)
        pairs.
        """

        return self.items()

    def iterkeys(self) -> Iterator:
        """Returns an iterator over the Maps object's keys."""

        return self._map.iterkeys()

    def itervalues(self) -> Iterator:
        """Returns an iterator over the Maps object's values."""

        return self._map.itervalues()

    def keys(self) -> Iterable:
        """Returns the keys of the Maps object."""

        return self._map.keys()

    def next(self) -> str:
        """Returns the next key in the dictionary."""

        return self._map.next()

    @classmethod
    def parse_ini(cls, ini_dict: ConfigParser, to_maps=False) -> Union[dict, Maps]:
        """
        Converts the values from an INI file from all strings to their
        actual Python base-types (i.e. int, float, bool, etc).

        If the value cannot be converted, it is kept as a string.
        If a value of the key:value pairs is not a string, its type is
        maintained.

        Note:
            Any meant-to-be-bool values in the key:value pairs that are
            not exactly 'False' or 'True', but are similar like 'false'
            or 'tRue' for example, will be converted to bools.

        Args:
            ini_dict (:obj:`ConfigParser`):
                The dictionary returned by configparser when an INI file
                is loaded.
            to_maps (:obj:`bool`):
                Return a :obj:`Maps` object instead of a :obj:`dict`.

        Returns:
            dict or Maps:
                A dictionary maintaining the same key:value pairs as the
                input dictionary; however, the values are their Python
                base-types. If :obj:`to_maps` is :obj:`True`, return a
                :obj:`Maps` object.

        Raises:
            TypeError:
                An argument is of an illegal type.
        """

        # Check for dict because of recursion; ini_dict is only meant
        # to be a dict when the function recursively converts the values
        # from a ConfigParser
        if not isinstance(ini_dict, (dict, ConfigParser)):
            raise TypeError(
                "argument 'ini_dict' must be of type 'ConfigParser': "
                f"{type(ini_dict).__name__}"
            )
        if isinstance(ini_dict, ConfigParser):
            ini_dict_ = {}
            for section in ini_dict.sections():
                ini_dict_[section] = {}
                for option in ini_dict.options(section):
                    # Parse using configparser
                    option_value = ini_dict.get(section, option)

                    # Parse using os environ
                    matches = [(m.start(0), m.end(0)) for m in re.finditer("&", option_value)]
                    if len(matches) > 0 and len(matches) % 2 == 0:
                        i = 0
                        while True:
                            try:
                                index_end = matches.pop(i + 1)[1]
                                index_start = matches.pop(i)[0]
                                sub = option_value[index_start:index_end]
                                sub_replace = os.environ[sub[1:-1]]
                                option_value = option_value.replace(sub, sub_replace)
                            except IndexError:
                                break
                            except KeyError:
                                pass
                    ini_dict_[section][option] = option_value
            ini_dict = ini_dict_

        for key, value in ini_dict.items():
            if isinstance(value, dict):
                # Recursively parse dict
                ini_dict[key] = Maps.parse_ini(value, to_maps=to_maps)
            else:
                if not isinstance(value, str):
                    continue
                try:
                    ini_dict[key] = ast.literal_eval(value)
                except NameError:
                    if value.lower() == "false":
                        ini_dict[key] = False
                    elif value.lower() == "true":
                        ini_dict[key] = True
                    else:
                        ini_dict[key] = value
                except (SyntaxError, ValueError):
                    # Cannot eval this value
                    ini_dict[key] = value
        return Maps(ini_dict) if to_maps else ini_dict

    @classmethod
    def parse_value(cls, value: Any) -> Any:
        """
        Checks if :term:`value` subclasses :obj:`Maps`. If so, it
        returns the :obj:`Maps` object; otherwise the :term:`value`
        itself.

        Args:
            value (:obj:`Any`):
                The value to parse.

        Returns:
            Any:
                :obj:`OrderedDict` if :term:`value` subclasses
                :obj:`Maps`, otherwise :term:`value`.
        """

        if issubclass(type(value), Maps):
            return value.map
        else:
            return value

    def pop(self, key: str, default: Optional[Any] = None) -> Union[Any, NoReturn]:
        """
        Removes and returns the value in the Maps object at 'key'. If
        'key' does not exist, then 'default' is returned.

        Args:
            key (:obj:`str`):
                The key to use to remove a value from the Maps object.
            default (:obj:`obj`, optional):
                The value to return if :term:`key` does not exist in the
                :obj:`Maps` object.

        Returns:
            Any:
                The value at :term:`key`, otherwise :term:`default`.
        """

        return self._map.pop()

    def popitem(self) -> Any:
        """Removes and returns an arbitrary (key, value) pair from the
        :obj:`Maps` object.

        Returns:
            Any:
                The arbitrary (key, value) pair.

        Raises:
            KeyError:
                The :obj:`Maps` object is empty.
        """

        return self._map.popitem()

    def setdefault(self, key: str, default=None) -> Any:
        """
        Returns a value of the 'key' in the Maps object.

        If 'key' is not found, then 'default' is inserted at 'key' into
        the Maps object and then returns that value.

        Args:
            key: The key to return the value of.
            default (:obj:`obj`, optional): The value to insert if 'key'
                                            does not exist. Defaults to
                                            none.

        Returns:
            object: The object at 'key' in the Maps object, default'
                    otherwise.
        """

        return self._map.setdefault(key, default)

    def to_dict(self) -> Union[dict, NoReturn]:
        """Converts the :obj:`Maps` object to a stdlib dictionary.

        Returns:
            dict:
                The converted :obj:`Maps` object as a dictionary.
        """

        new_dict = {}

        for key, value in self.items():
            if issubclass(type(value), Maps):
                if id(value) == id(self):
                    value = new_dict
                else:
                    value = value.to_dict()
            elif isinstance(value, (tuple, list)):
                new_list = []

                for item in value:
                    temp_item = item
                    if issubclass(type(item), Maps):
                        temp_item = item.to_dict()
                    new_list.append(temp_item)

                if isinstance(value, tuple):
                    value = tuple(new_list)
                else:
                    value = new_list

            new_dict[key] = value
        return new_dict

    def update(self, *args, **kwargs) -> None:
        """Adds or changes existing values using a dictionary or
        iterator of key:value pairs."""

        if len(args) != 0:
            self._map.update(*args)
        self._map.update(kwargs)

    def values(self) -> Any:
        """Returns the values of the :obj:`Maps` object."""

        return self._map.values()

    def viewitems(self) -> Any:
        """Returns a new view of the :obj:`Maps` object's items
        (key:value pairs)."""

        return self._map.viewitems()

    def viewkeys(self) -> Any:
        """Returns a new view of the :obj:`Maps` object's keys."""

        return self._map.viewkeys()

    def viewvalues(self) -> Any:
        """Returns a new view of the :obj:`Maps` object's values."""

        return self._map.viewvalues()
