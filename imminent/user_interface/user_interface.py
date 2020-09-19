import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from imminent.setting.setting_handling import JSON
from imminent.utilities.file_handling import FileHandler
from imminent.user_interface.pop_up import PopUpWindow


class Ui_MainWindow(object):

    def __init__(self, MainWindow):
        self.tmp_dir = os.path.join(
            Path.home(),
            'Kugar\'s Guild Management Tool')
        FileHandler().make_directory(self.tmp_dir)
        self.main_window = MainWindow
        self._init_main_window()
        self._init_widgets()

    def _init_main_window(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(697, 298)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.main_window.sizePolicy().hasHeightForWidth())
        self.main_window.setSizePolicy(sizePolicy)
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate(
            "MainWindow", "Kugar\'s Guild Management Tool"))

    def _init_widgets(self):
        self._create_central_grid()
        self._create_select_guild_label()
        self._create_guild_combobox()
        self._create_add_guild_button()
        self._create_separator_line()
        self._create_character_list_label()
        self._create_add_character_button()
        self._create_delete_characters_button()
        self._create_generate_report_button()
        self._create_cancel_button()
        self._create_scrolled_area()
        self._create_character_checkboxes()
        self._create_status_bar()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def _create_central_grid(self):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

    def _create_select_guild_label(self):
        self.select_guild_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.select_guild_label.sizePolicy().hasHeightForWidth())
        self.select_guild_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.select_guild_label.setFont(font)
        self.select_guild_label.setObjectName("select_guild_label")
        self.gridLayout.addWidget(self.select_guild_label, 0, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.select_guild_label.setText(
            _translate("MainWindow", "Select Guild :"))

    def _create_guild_combobox(self):
        self.guild_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.guild_comboBox.setObjectName("comboBox")
        self.guild_comboBox.clear()
        _translate = QtCore.QCoreApplication.translate
        lista = self._get_list_of_guilds()
        self.guild_comboBox.addItems(lista)
        self.gridLayout.addWidget(self.guild_comboBox, 0, 1, 1, 1)

    def _get_list_of_guilds(self):
        return os.listdir(self.tmp_dir)

    def _create_add_guild_button(self):
        self.add_guild_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.add_guild_button.sizePolicy().hasHeightForWidth())
        self.add_guild_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.add_guild_button.setFont(font)
        self.add_guild_button.setObjectName("add_guild_button")
        self.gridLayout.addWidget(self.add_guild_button, 0, 2, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.add_guild_button.setText(
            _translate("MainWindow", "Add Guild"))
        self.add_guild_button.clicked.connect(self._add_guild_button_action)

    def _create_separator_line(self):
        self.line = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.line.setFont(font)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)

    def _create_character_list_label(self):
        self.character_list_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.character_list_label.sizePolicy().hasHeightForWidth())
        self.character_list_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.character_list_label.setFont(font)
        self.character_list_label.setObjectName("character_list_label")
        self.gridLayout.addWidget(self.character_list_label, 2, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.character_list_label.setText(
            _translate("MainWindow", "Character List:"))

    def _create_add_character_button(self):
        self.add_character_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.add_character_button.sizePolicy().hasHeightForWidth())
        self.add_character_button.setSizePolicy(sizePolicy)
        self.add_character_button.setObjectName("add_character_button")
        self.gridLayout.addWidget(self.add_character_button, 4, 0, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.add_character_button.setText(
            _translate("MainWindow", "Add Character"))
        self.add_character_button.clicked.connect(
            self._add_character_button_action)

    def _create_delete_characters_button(self):
        self.delete_characters_button = QtWidgets.QPushButton(
            self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.delete_characters_button.sizePolicy().hasHeightForWidth())
        self.delete_characters_button.setSizePolicy(sizePolicy)
        self.delete_characters_button.setObjectName("delete_characters_button")
        self.gridLayout.addWidget(self.delete_characters_button, 4, 1, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.delete_characters_button.setText(_translate(
            "MainWindow", "Delete Characters"))
        self.delete_characters_button.clicked.connect(
            self._delete_button_action)

    def _create_generate_report_button(self):
        self.generate_report_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.generate_report_button.sizePolicy().hasHeightForWidth())
        self.generate_report_button.setSizePolicy(sizePolicy)
        self.generate_report_button.setObjectName("generate_report_button")
        self.gridLayout.addWidget(self.generate_report_button, 4, 2, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.generate_report_button.setText(
            _translate("MainWindow", "Generate Report"))

    def _create_cancel_button(self):
        self.cancel_button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.cancel_button.sizePolicy().hasHeightForWidth())
        self.cancel_button.setSizePolicy(sizePolicy)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 4, 3, 1, 1)
        _translate = QtCore.QCoreApplication.translate
        self.cancel_button.setText(_translate("MainWindow", "Cancel"))
        self.cancel_button.clicked.connect(
            self._cancel_button_action)

    def _create_scrolled_area(self):
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(
            QtCore.QRect(0, 0, 677, 158))
        self.scrollAreaWidgetContents_3.setObjectName(
            "scrollAreaWidgetContents_3")
        self.scrollArea_gridLayout = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_3)
        self.scrollArea_gridLayout.setObjectName("scrollArea_gridLayout")

    def _create_character_checkboxes(self):
        self.checkbox_list = []
        _translate = QtCore.QCoreApplication.translate
        guild = str(self.guild_comboBox.currentText())
        roster_path = os.path.join(
            self.tmp_dir, guild, 'roster', 'roster.json')
        if not os.path.isfile(roster_path):
            self._create_template_roster_file(guild)
        roster = JSON(roster_path)
        roster.load_setting()
        vertical_position_counter = 0
        for _ in roster.values['roster']:
            charname = _.split('/')[7].capitalize()
            setattr(self, 'char_checkbox' + charname,
                    QtWidgets.QCheckBox(self.scrollAreaWidgetContents_3))
            sizePolicy = QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                getattr(self, 'char_checkbox' + charname).sizePolicy(
                ).hasHeightForWidth())
            getattr(self, 'char_checkbox' +
                    charname).setSizePolicy(sizePolicy)
            getattr(self, 'char_checkbox' +
                    charname).setObjectName('char_checkbox'
                                            + charname)
            self.scrollArea_gridLayout.addWidget(
                getattr(self, 'char_checkbox' + charname),
                vertical_position_counter, 0, 1, 1)
            self.checkbox_list.append(
                getattr(self, 'char_checkbox' + charname))
            getattr(self, 'char_checkbox' +
                    charname).setText(_translate("MainWindow",
                                                 charname))
            vertical_position_counter += 1
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.gridLayout.addWidget(self.scrollArea, 3, 0, 1, 4)
        self.main_window.setCentralWidget(self.centralwidget)
        self.guild_comboBox.currentTextChanged.connect(
            self._refresh_scrollArea_gridLayout)

    def _refresh_scrollArea_gridLayout(self):
        if hasattr(self, 'scrollArea_gridLayout'):
            for i in reversed(range(self.scrollArea_gridLayout.count())):
                self.scrollArea_gridLayout.itemAt(i).widget().setParent(None)
        self._create_character_checkboxes()

    def _create_status_bar(self):
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

    def _create_template_roster_file(self, guild):
        roster_dir = os.path.join(
            self.tmp_dir, guild, 'roster')
        roster_path = os.path.join(roster_dir, 'roster.json')
        FileHandler().make_directory(roster_dir)
        roster = JSON(roster_path)
        roster.values = {'roster': []}
        roster.save_setting()

    def _add_new_guild(self, guild):
        guild_dir = os.path.join(self.tmp_dir, guild)
        if not os.path.isdir(guild_dir):
            FileHandler().make_directory(guild_dir)
            self._create_template_roster_file(guild)

    def _add_guild_button_action(self):
        PopUpWindow('guild', self)
        self._create_guild_combobox()

    def _add_character_button_action(self):
        PopUpWindow('character', self)
        self._refresh_scrollArea_gridLayout()

    def _add_new_character(self, armory_link):
        guild = str(self.guild_comboBox.currentText())
        roster_path = os.path.join(
            self.tmp_dir, guild, 'roster', 'roster.json')
        if not os.path.isfile(roster_path):
            self._create_template_roster_file(guild)
        roster = JSON(roster_path)
        roster.load_setting()
        roster.values['roster'].append(armory_link)
        roster.save_setting()

    def _cancel_button_action(self):
        self.main_window.close()

    def _delete_button_action(self):
        delete_list = []
        for _ in self.checkbox_list:
            if _.isChecked():
                delete_list.append(_.text())
        self._delete_roster_entries(delete_list)
        self._refresh_scrollArea_gridLayout()

    def _delete_roster_entries(self, delete_list):
        guild = str(self.guild_comboBox.currentText())
        roster_path = os.path.join(
            self.tmp_dir, guild, 'roster', 'roster.json')
        roster = JSON(roster_path)
        roster.load_setting()
        for _ in delete_list:
            for link in roster.values['roster']:
                if _.lower() in link:
                    index = roster.values['roster'].index(link)
                    roster.values['roster'].pop(index)
                    break
        roster.save_setting()
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
