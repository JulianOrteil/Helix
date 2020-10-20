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

"""Tests importing and running functions for the utilities module.

This file is meant to be ran using the pytest framework.
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function


def test_loading_configs() -> None:

    from helix.utils.configs import logging_config


def test_dictutils() -> None:

    from helix.utils.dictutils import Maps

    d = {"hello": "world", "should_be_int": "32"}
    maps = Maps(d)

    assert maps.hello and isinstance(maps.hello, str)
    assert maps.should_be_int and isinstance(maps.should_be_int, int)
