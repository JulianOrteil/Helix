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

"""Builds the main window of the application.

'Ui_Helix' is the builder class and is meant to be inherited before a
window type. Importing everything from this module will only import the
builder class (as defined by the '__all__' attribute).

Example Usage:
    >>> class Window(Ui_Helix, QMainWindow):
    >>>     ...
"""


from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function


__all__ = ["Ui_Helix"]


from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QToolButton,
    QVBoxLayout,
    QWidget
)


class Ui_Helix(object):
    """Contains the widgets used in the main window of the application.

    Call :meth:`setup_ui` to build the widgets used in the window.

    Attributes:
        central_widget (:obj:`QWidget`):
            The container widget of everything in the window.
        central_layout (:obj:`QGridLayout`):
            The primary layout organizing each component of the window.
        navbar (:obj:`navbar`):
            The widget containing each button navigating to the
            different modes of the application.
        navbar_layout (:obj:`navbar_layout`):
            The layout organizing each button of the navbar.
        home_btn (:obj:`QToolButton`):
            The button, when clicked, redirecting the user to the home
            window.
        annotation_btn (:obj:`QToolButton`):
            The button, when clicked, redirecting the user to the
            annotation window.
        train_btn (:obj:`QToolButton`):
            The button, when clicked, redirecting the user to the model
            train window.
        eval_btn (:obj:`QToolButton`):
            The button, when clicked, redirecting the user to the
            evaluation window.
        navbar_spcaer (:obj:`QSpacerItem`):
            The spacer pushing all buttons to the top of the navbar.
        topbar (:obj:`QFrame`):
            The topbar containing the application logo and the minimize,
            maximize, and close buttons.
        topbar_layout (:obj:`topbar_layout`):
            The layout organizing each widget of the topbar.
        helix_logo (:obj:`QLabel`):
            The widget containing the double helix part of the logo.
        helix_logo_text(:obj:`QLabel`):
            The widget containing the 'HELIX' part of the logo.
        topbar_spcaer (:obj:`QSpacerItem`):
            The spacer pushing the logo and buttons apart.
        minimize_btn (:obj:`QToolButton`):
            The button minimizing the application.
        maximize_btn (:obj:`QToolButton`):
            The button maximizing the application.
        close_btn (:obj:`QToolButton`):
            The button closing the application.
        main_content (:obj:`QFrame`):
            The content container for each separate window.
        main_content_layout (:obj:`QHBoxLayout`):
            The layout organizing each window.
        content_bar (:obj:`QFrame`):
            The widget between the navbar and content container hosting
            each button for each window.
        content_bar_layout (:obj:`QVBoxLayout`):
            The layout organizing each button for each window.
        content_bar_spacer (:obj:`QSpacerItem`):
            The spcaer pushing each menu button to the top of the
            content_bar.
        content (:obj:`QLabel`):
            A default content window. Meant to be replaced.
    """

    central_widget: QWidget
    central_layout: QGridLayout

    navbar: QFrame
    navbar_layout: QVBoxLayout
    home_btn: QToolButton
    annotation_btn: QToolButton
    train_btn: QToolButton
    eval_btn: QToolButton
    navbar_spacer: QSpacerItem

    topbar: QFrame
    topbar_layout: QHBoxLayout
    helix_logo: QLabel
    helix_logo_text: QLabel
    topbar_spacer: QSpacerItem
    minimize_btn: QToolButton
    maximize_btn: QToolButton
    close_btn: QToolButton

    main_content: QFrame
    main_content_layout: QHBoxLayout
    content_bar: QFrame
    content_bar_layout: QVBoxLayout
    # open_file_btn: QToolButton
    # open_dataset_btn: QToolButton
    # next_image_btn: QToolButton
    # previous_image_btn: QToolButton
    content_bar_spacer: QSpacerItem
    content: QLabel

    def setup_ui(self, Helix: QMainWindow) -> None:
        """Builds the widgets for the window.

        Args:
            Helix (:obj:`QMainWindow`):
                The child window inheriting this builder class. The
                child will hold the references to every widget built in
                this class.

        Example Usage:
            >>> class Window(Ui_Helix, QMainWindow):
            ...
            ...     def __init__(self) -> None:
            ...         super().__init__()
            ...
            ...         self.setup_ui(self)
        """

        # Create base window
        Helix.resize(1920, 1080)
        Helix.setMinimumSize(QSize(800, 600))
        Helix.setObjectName("Helix")

        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(Helix.sizePolicy().hasHeightForWidth())

        Helix.setSizePolicy(size_policy)
        Helix.setStyleSheet(
            "* {    \n"
            "    background-color: rgb(60, 62, 83);\n"
            "    color: white;\n"
            "}\n"
            "\n"
            "QFrame, QToolButton {\n"
            "    background-color: rgb(42, 43, 64);\n"
            "    border: none;\n"
            "}\n"
            "\n"
            "QToolButton:hover {\n"
            "    background-color: rgb(26, 30, 50);\n"
            "}\n"
            "\n"
            "QToolButton:pressed {\n"
            "    background-color: rgb(60, 62, 83);\n"
            "}\n"
            "\n"
            "#image {\n"
            "    background-color: rgb(26, 30, 50);\n"
            "}\n"
            "\n"
            "#main_content {\n"
            "    background-color: rgb(26, 30, 50);\n"
            "}"
        )

        self._setup_central_widgets(Helix)
        self._setup_navbar()
        self._setup_topbar()
        self._setup_central_content()

        Helix.setCentralWidget(self.central_widget)
        self._retranslate_ui(Helix)

    def _setup_central_widgets(self, Helix: QMainWindow) -> None:
        # Create the central widget
        self.central_widget = QWidget(Helix)
        self.central_widget.setObjectName("central_widget")

        # Create the central layout
        self.central_layout = QGridLayout(self.central_widget)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setHorizontalSpacing(3)
        self.central_layout.setObjectName("central_layout")
        self.central_layout.setVerticalSpacing(0)

    def _setup_navbar(self) -> None:
        # Create the navbar
        self.navbar = QFrame(self.central_widget)
        self.navbar.setFrameShadow(QFrame.Raised)
        self.navbar.setFrameShape(QFrame.StyledPanel)
        self.navbar.setMinimumSize(QSize(45, 0))
        self.navbar.setObjectName("navbar")

        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(23)
        size_policy.setHeightForWidth(self.navbar.sizePolicy().hasHeightForWidth())

        self.navbar.setSizePolicy(size_policy)

        # Create the navbar layout
        self.navbar_layout = QVBoxLayout(self.navbar)
        self.navbar_layout.setContentsMargins(0, 0, 0, 0)
        self.navbar_layout.setObjectName("navbar_layout")

        # Create the home btn
        self.home_btn = QToolButton(self.navbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/home_icon_sml.png"),
            QIcon.Normal,
            QIcon.Off
        )

        self.home_btn.setIcon(icon)
        self.home_btn.setIconSize(QSize(45, 45))
        self.home_btn.setMinimumSize(QSize(45, 45))
        self.home_btn.setObjectName("home_btn")

        size_policy = QSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.home_btn.sizePolicy().hasHeightForWidth())

        self.home_btn.setSizePolicy(size_policy)
        self.home_btn.setText('')

        # Create the annotation btn
        self.annotation_btn = QToolButton(self.navbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/annotate_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )
        self.annotation_btn.setIcon(icon)
        self.annotation_btn.setIconSize(QSize(45, 45))
        self.annotation_btn.setMinimumSize(QSize(45, 45))
        self.annotation_btn.setObjectName("annotation_btn")

        size_policy = QSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.annotation_btn.sizePolicy().hasHeightForWidth())

        self.annotation_btn.setSizePolicy(size_policy)
        self.annotation_btn.setText('')

        # Create the train btn
        self.train_btn = QToolButton(self.navbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/train_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )
        self.train_btn.setIcon(icon)
        self.train_btn.setIconSize(QSize(45, 45))
        self.train_btn.setMinimumSize(QSize(45, 45))
        self.train_btn.setObjectName("train_btn")

        size_policy = QSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.train_btn.sizePolicy().hasHeightForWidth())

        self.train_btn.setSizePolicy(size_policy)
        self.train_btn.setText('')

        # Create the eval btn
        self.eval_btn = QToolButton(self.navbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/evaluate_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )
        self.eval_btn.setIcon(icon)
        self.eval_btn.setIconSize(QSize(45, 45))
        self.eval_btn.setMinimumSize(QSize(45, 45))
        self.eval_btn.setObjectName("eval_btn")

        size_policy = QSizePolicy(
            QSizePolicy.Minimum,
            QSizePolicy.Fixed
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.eval_btn.sizePolicy().hasHeightForWidth())

        self.eval_btn.setSizePolicy(size_policy)
        self.eval_btn.setText('')

        # Create the bottom spacer
        self.navbar_spacer = QSpacerItem(
            20,
            40,
            QSizePolicy.Minimum,
            QSizePolicy.Expanding
        )

        # Add the widgets to the navbar layout
        self.navbar_layout.addWidget(self.home_btn)
        self.navbar_layout.addWidget(self.annotation_btn)
        self.navbar_layout.addWidget(self.train_btn)
        self.navbar_layout.addWidget(self.eval_btn)
        self.navbar_layout.addItem(self.navbar_spacer)

        # Add the navbar to the central laytout
        self.central_layout.addWidget(
            self.navbar,
            1, 0, 1, 1
        )

    def _setup_topbar(self) -> None:
        # Create the topbar
        self.topbar = QFrame(self.central_widget)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.topbar.setFrameShape(QFrame.StyledPanel)
        self.topbar.setMinimumSize(QSize(0, 45))
        self.topbar.setObjectName("topbar")

        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(1)
        size_policy.setHeightForWidth(self.topbar.sizePolicy().hasHeightForWidth())

        self.topbar.setSizePolicy(size_policy)

        # Create the topbar layout
        self.topbar_layout = QHBoxLayout(self.topbar)
        self.topbar_layout.setContentsMargins(0, 0, 0, 0)
        self.topbar_layout.setObjectName("topbar_layout")

        # Create the Helix logo
        self.helix_logo = QLabel(self.topbar)
        self.helix_logo.setAlignment(Qt.AlignCenter)
        self.helix_logo.setMinimumSize(QSize(45, 45))
        self.helix_logo.setObjectName("helix_logo")
        self.helix_logo.setPixmap(QPixmap(":/images/images/helix_icon_sml.png"))
        self.helix_logo.setScaledContents(True)
        self.helix_logo.setText('')
        self.helix_logo.setWordWrap(False)

        # Create the Helix logo text
        self.helix_logo_text = QLabel(self.topbar)
        self.helix_logo_text.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter
        )

        font = QFont()
        font.setFamily("Arial Black")
        font.setItalic(True)
        font.setPointSize(16)
        font.setWeight(50)

        self.helix_logo_text.setFont(font)
        self.helix_logo_text.setObjectName("helix_logo_text")
        self.helix_logo_text.setStyleSheet('')

        # Create the topbar spacer
        self.topbar_spacer = QSpacerItem(
            40,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        # Create the minimize btn
        self.minimize_btn = QToolButton(self.topbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/minimize_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )

        self.minimize_btn.setIcon(icon)
        self.minimize_btn.setIconSize(QSize(20, 20))
        self.minimize_btn.setMinimumSize(QSize(45, 45))
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setText('')

        # Create the maximize btn
        self.maximize_btn = QToolButton(self.topbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/maximize_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )

        self.maximize_btn.setIcon(icon)
        self.maximize_btn.setIconSize(QSize(20, 20))
        self.maximize_btn.setMinimumSize(QSize(45, 45))
        self.maximize_btn.setObjectName("maximize_btn")
        self.maximize_btn.setText('')

        # Create the close btn
        self.close_btn = QToolButton(self.topbar)

        icon = QIcon()
        icon.addPixmap(
            QPixmap(":/images/images/close_icon.png"),
            QIcon.Normal,
            QIcon.Off
        )

        self.close_btn.setIcon(icon)
        self.close_btn.setIconSize(QSize(20, 20))
        self.close_btn.setMinimumSize(QSize(45, 45))
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setText('')

        # Add the widgets to the topbar layout
        self.topbar_layout.addWidget(self.helix_logo)
        self.topbar_layout.addWidget(self.helix_logo_text)
        self.topbar_layout.addItem(self.topbar_spacer)
        self.topbar_layout.addWidget(self.minimize_btn)
        self.topbar_layout.addWidget(self.maximize_btn)
        self.topbar_layout.addWidget(self.close_btn)

        # Add the topbar to the central layout
        self.central_layout.addWidget(
            self.topbar,
            0, 0, 1, 2
        )

    def _setup_central_content(self) -> None:
        # Create the main content container
        self.main_content = QFrame(self.central_widget)
        self.main_content.setFrameShadow(QFrame.Raised)
        self.main_content.setFrameShape(QFrame.StyledPanel)
        self.main_content.setObjectName("main_content")

        size_policy = QSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        size_policy.setHorizontalStretch(42)
        size_policy.setHeightForWidth(self.main_content.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)

        self.main_content.setSizePolicy(size_policy)
        self.main_content.setStyleSheet('')

        # Create the main content layout
        self.main_content_layout = QHBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setObjectName("main_content_layout")
        self.main_content_layout.setSpacing(0)

        # Create the content_bar
        self.content_bar = QFrame(self.main_content)
        self.content_bar.setFrameShadow(QFrame.Raised)
        self.content_bar.setFrameShape(QFrame.StyledPanel)
        self.content_bar.setObjectName("content_bar")

        size_policy = QSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Preferred
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setHeightForWidth(self.content_bar.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)

        self.content_bar.setSizePolicy(size_policy)

        # Create the content_bar layout
        self.content_bar_layout = QVBoxLayout(self.content_bar)
        self.content_bar_layout.setObjectName("content_bar_layout")

        # Create the open single file btn
        # self.open_file_btn = QToolButton(self.content_bar)
        # self.open_file_btn.setAutoRaise(False)
        # self.open_file_btn.setEnabled(False)

        # font = QFont()
        # font.setFamilies("Segoe UI")
        # font.setPointSize(10)

        # self.open_file_btn.setFont(font)

        # icon = QIcon()
        # icon.addPixmap(
        #     QPixmap(":/images/images/open_file_icon_sml.png"),
        #     QIcon.Normal,
        #     QIcon.Off
        # )

        # self.open_file_btn.setIcon(icon)
        # self.open_file_btn.setIconSize(QSize(60, 60))
        # # self.open_file_btn.setObjectName("open_file_btn")
        # self.open_file_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Create the open dataset btn
        # self.open_dataset_btn = QToolButton(self.content_bar)
        # self.open_dataset_btn.setAutoRaise(False)
        # self.open_dataset_btn.setEnabled(False)

        # font = QFont()
        # font.setFamilies("Segoe UI")
        # font.setPointSize(10)

        # self.open_dataset_btn.setFont(font)

        # icon = QIcon()
        # icon.addPixmap(
        #     QPixmap(":/images/images/open_directory_icon_sml.png"),
        #     QIcon.Normal,
        #     QIcon.Off
        # )

        # self.open_dataset_btn.setIcon(icon)
        # self.open_dataset_btn.setIconSize(QSize(60, 60))
        # # self.open_dataset_btn.setObjectName("open_dataset_btn")
        # self.open_dataset_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Create the next image btn
        # self.next_image_btn = QToolButton(self.content_bar)
        # self.next_image_btn.setAutoRaise(False)
        # self.next_image_btn.setEnabled(False)

        # font = QFont()
        # font.setFamilies("Segoe UI")
        # font.setPointSize(10)

        # self.next_image_btn.setFont(font)

        # icon = QIcon()
        # icon.addPixmap(
        #     QPixmap(":/images/images/arrow_right_sml.png"),
        #     QIcon.Normal,
        #     QIcon.Off
        # )

        # self.next_image_btn.setIcon(icon)
        # self.next_image_btn.setIconSize(QSize(60, 60))
        # # self.next_image_btn.setObjectName("next_image_btn")
        # self.next_image_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Create the previous image btn
        # self.previous_image_btn = QToolButton(self.content_bar)
        # self.previous_image_btn.setAutoRaise(False)
        # self.previous_image_btn.setEnabled(False)

        # font = QFont()
        # font.setFamilies("Segoe UI")
        # font.setPointSize(10)

        # self.previous_image_btn.setFont(font)

        # icon = QIcon()
        # icon.addPixmap(
        #     QPixmap(":/images/images/arrow_left_sml.png"),
        #     QIcon.Normal,
        #     QIcon.Off
        # )

        # self.previous_image_btn.setIcon(icon)
        # self.previous_image_btn.setIconSize(QSize(60, 60))
        # # self.previous_image_btn.setObjectName("previous_image_btn")
        # self.previous_image_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # Create the content_bar spacer
        self.content_bar_spacer = QSpacerItem(
            40,
            20,
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        # Create the content
        self.content = QLabel(self.main_content)
        self.content.setAlignment(Qt.AlignCenter)

        font = QFont()
        font.setFamily("Arial Black")
        font.setItalic(True)
        font.setKerning(True)
        font.setPointSize(20)

        self.content.setFont(font)
        self.content.setObjectName("content")

        size_policy = QSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Preferred
        )
        size_policy.setHorizontalStretch(6)
        size_policy.setHeightForWidth(self.content.sizePolicy().hasHeightForWidth())
        size_policy.setVerticalStretch(0)

        self.content.setSizePolicy(size_policy)

        # Add the widgets to the content_bar layout
        # self.content_bar_layout.addWidget(self.open_file_btn)
        # self.content_bar_layout.addWidget(self.open_dataset_btn)
        # self.content_bar_layout.addWidget(self.next_image_btn)
        # self.content_bar_layout.addWidget(self.previous_image_btn)
        self.content_bar_layout.addItem(self.content_bar_spacer)

        # Add the widgets to the main content layout
        self.main_content_layout.addWidget(self.content_bar)
        self.main_content_layout.addWidget(self.content)

        # Add the main content container to the central layout
        self.central_layout.addWidget(
            self.main_content,
            1, 1, 1, 1
        )

    def _retranslate_ui(self, Helix: QMainWindow) -> None:
        _translate = QCoreApplication.translate

        Helix.setWindowTitle(_translate("Helix", "Helix"))
        self.helix_logo_text.setText(_translate("Helix", "HELIX"))
        self.close_btn.setText(_translate("Helix", "X"))
        # self.open_file_btn.setShortcut(_translate("Helix", "Ctrl+O"))
        # self.open_file_btn.setText(_translate("Helix", "Open Single File\n(Ctrl + O)"))
        # self.open_dataset_btn.setShortcut(_translate("Helix", "Ctrl+Shift+O"))
        # self.open_dataset_btn.setText(
        #     _translate("Helix", "Open Dataset Directory\n(Ctrl + Shift + O)")
        # )
        # self.next_image_btn.setShortcut(_translate("Helix", "d"))
        # self.next_image_btn.setText(_translate("Helix", "Next Image (d)"))
        # self.previous_image_btn.setShortcut(_translate("Helix", "a"))
        # self.previous_image_btn.setText(_translate("Helix", "Previous Image (a)"))
        self.content.setText(_translate("Helix", "THIS DEFAULT CONTENT WINDOW SHOULD BE REPLACED."))
