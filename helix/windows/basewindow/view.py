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

"""Contains the common attributes used in the windows in the app.

'BaseMainWindowView' contains common settings and signals for each main
window of the application. The class inherits 'QMainWindow', so only
the base window class needs to be inherited. The class should be
inherited after the window widget builder class, if there is one.

Example Usage:
    >>> # Note: No QMainWindow inherit
    >>> class Window(Ui_Window, BaseMainWindowView):
    ...
    ...     def __init__(self, *args, **kwargs) -> None:
    ...         super().__init__()

If importing all (i.e. 'from view import *'), only 'BaseMainWindowView'
will be imported as defined in the '__all__' attribute.
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function


__all__ = ["BaseMainWindowView"]


from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow


class BaseMainWindowView(QMainWindow):
    """Contains common settings and signals used in the main window.

    Attributes:
        closed (:obj:`pyqtSignal`):
            The signal fired when a close event is detected. The close
            event is sent through the signal.
        keypressed (:obj:`pyqtSignal`):
            The signal fired when a keypress is detected. The keypress
            event is sent through the signal.
    """

    closed = pyqtSignal(QCloseEvent)
    keypressed = pyqtSignal(QKeyEvent)

    def __init__(self) -> None:
        super().__init__()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.closed.emit(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keypressed.emit(event)
