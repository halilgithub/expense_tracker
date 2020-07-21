import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

class CustomQWidget(QWidget):
    def __init__(self, label_str, parent=None):
        super(CustomQWidget, self).__init__(parent)
        label = QLabel(label_str)
        label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

def show_warning(message_text, informative_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message_text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Warning")
    msg.exec_()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow.ui', self)

        # prepare save printout icon
        save_printout_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_DriveFDIcon))
        save_printout_button_action = QAction(save_printout_icon, "Save printout", self)
        save_printout_button_action.setStatusTip("This is save printout button")
        save_printout_button_action.triggered.connect(self.save_printout)
        save_printout_button_action.setCheckable(True)
        self.toolBar.addAction(save_printout_button_action)

        # prepare trash printout icon
        trash_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_TrashIcon))
        trash_button_action = QAction(trash_icon, "Trash printout", self)
        trash_button_action.setStatusTip("This is trash printout button")
        trash_button_action.triggered.connect(self.trash_printout)
        trash_button_action.setCheckable(True)
        self.toolBar.addAction(trash_button_action)
        self.amount = None
        self.description = None
        self.row_str = None
        self.item = None
        self.blank = ' ' * 40

        self.handel_buttons()

    def handel_buttons(self):
        self.addExpenseButton.clicked.connect(self.add_item_as_expense)
        self.addDepositButton.clicked.connect(self.add_item_as_deposit)
        self.removeItemButton.clicked.connect(self.remove_item)

    def clear_inputs(self):
        self.amountText.setText('')
        self.descriptionText.setText('')
        self.amount = None
        self.description = None
        self.row_str = None
        self.item = None

    def add_item_as_expense(self):
        try:
            self.amount = float(self.amountText.text())
        except ValueError:
            show_warning('Amount is Invalid', 'Please input a Valid amount')
            self.clear_inputs()
            return

        if self.amount != 0.0:
            self.amount = -1 * self.amount
        self.description = self.descriptionText.text()
        self.amount = str(self.amount)

        self.description = '{:>40}'.format(self.description)
        self.amount = '{:>40}'.format(self.amount)
        self.row_str = self.description + self.amount + self.blank
        print(self.row_str)
        self.item = QListWidgetItem(self.listWidget)
        item_widget = CustomQWidget(self.row_str)
        self.item.setSizeHint(item_widget.sizeHint())
        self.listWidget.addItem(self.item)
        self.listWidget.setItemWidget(self.item, item_widget)

        self.clear_inputs()

    def add_item_as_deposit(self):
        try:
            self.amount = float(self.amountText.text())
        except ValueError:
            show_warning('Amount is Invalid', 'Please input a Valid amount')
            self.clear_inputs()
            return

        self.description = self.descriptionText.text()
        
        self.clear_inputs()

    def remove_item(self):
        pass

    def save_printout(self):
        pass

    def trash_printout(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
