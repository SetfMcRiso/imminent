import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from imminent.utilities.file_handling import FileHandler


class PopUpWindow(QtWidgets.QDialog):

    def __init__(self, window_type, parent):
        super().__init__()
        self.window_type = window_type
        self.parent = parent
        self.setModal(True)
        self.resize(363, 119)
        self._create_layout()
        self._create_text_edit()
        self._create_label()
        self._create_buttons_layout()
        self._create_buttons()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.exec()

    def _create_layout(self):
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)

    def _create_text_edit(self):
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 0, 1, 1)

    def _create_label(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

    def _create_buttons_layout(self):
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

    def _create_buttons(self):
        self.add_button = QtWidgets.QPushButton(self)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.add_button.clicked.connect(self._add_button_clicked)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancel_button = QtWidgets.QPushButton(self)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.cancel_button.clicked.connect(self._cancel_button_clicked)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)

    def _add_button_clicked(self):
        if self.window_type == 'guild':
            guild = self.lineEdit.text()
            self.parent._add_new_guild(guild)
            self.parent._create_template_roster_file(guild)
            self.accept()
        else:
            armory_link = self.lineEdit.text()
            self.parent._add_new_character(armory_link)
            self.lineEdit.setText('')

    def _cancel_button_clicked(self):
        self.reject()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(
            "self", "Add " + self.window_type + " window"))
        if self.window_type == 'guild':
            self.label.setText(_translate(
                "self",
                "Please insert the name of the guild " +
                "that you would like to create"))
            self.add_button.setText(_translate("self", "Add Guild"))
        else:
            self.label.setText(_translate(
                "self",
                "Please insert the armory link of the character :"))
            self.add_button.setText(_translate("self", "Add Character"))
        self.cancel_button.setText(_translate("self", "Cancel"))
