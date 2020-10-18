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

"""Contains the view managing the main window of the application.
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function


from helix.windows.basewindows import BaseMainWindowView
from .ui import Ui_Helix

class HelixWindowView(Ui_Helix, BaseMainWindowView):

    def __init__(self) -> None:
        super().__init__()

        self.setup_ui(self)
