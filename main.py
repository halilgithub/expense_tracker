import sys
from os import path
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from decimal import Decimal


def show_warning(message_text, informative_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message_text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Warning")
    msg.exec_()


class CustomQWidget(QWidget):
    def __init__(self, label_str_list, parent=None):
        super(CustomQWidget, self).__init__(parent)
        layout = QHBoxLayout()
        for label_str in label_str_list:
            label = QLabel(label_str)
            label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('mainwindow.ui', self)

        # self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)

        # prepare save printout icon
        save_printout_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_DriveFDIcon))
        save_printout_button_action = QAction(save_printout_icon, "Save printout", self)
        save_printout_button_action.setStatusTip("This is save printout button")
        save_printout_button_action.triggered.connect(self.save_printout)
        save_printout_button_action.setCheckable(False)
        self.toolBar.addAction(save_printout_button_action)

        # prepare trash printout icon
        trash_icon = QIcon(QApplication.style().standardIcon(QStyle.SP_TrashIcon))
        trash_button_action = QAction(trash_icon, "Trash printout", self)
        trash_button_action.setStatusTip("This is trash printout button")
        trash_button_action.triggered.connect(self.trash_printout)
        trash_button_action.setCheckable(False)
        self.toolBar.addAction(trash_button_action)
        self.amount = None
        self.description = None
        self.blank = ' ' * 40
        self.label_str_list = []
        self.item = None
        self.balance = 0.0
        self.handel_buttons()

    def handel_buttons(self):
        self.addExpenseButton.clicked.connect(self.add_item_as_expense)
        self.addDepositButton.clicked.connect(self.add_item_as_deposit)
        self.removeItemButton.clicked.connect(self.remove_sel_item)

    def clear_inputs(self):
        self.amountText.setText('')
        self.descriptionText.setText('')
        self.amount = None
        self.description = None
        self.label_str_list = []
        self.item = None

    def add_item_as_expense(self):
        try:
            self.amount = float(self.amountText.text())
            if self.amount == 0.0:
                raise ValueError
        except ValueError:
            show_warning('Amount is Invalid or Zero', 'Please enter a Valid amount other than zero and use .(point) for decimals')
            self.clear_inputs()
            return

        self.description = self.descriptionText.text()
        amount_give = abs(self.amount)
        if amount_give <= self.balance:
            self.balance -= amount_give
        else:
            self.balance = -1 * (amount_give - self.balance)
        num = Decimal(str(self.balance))
        self.balance = float(round(num, 2))
        self.amount = '-' + str(abs(self.amount))
        self.description = '{:>40}'.format(self.description)
        self.amount = '{:>40}'.format(self.amount)

        self.label_str_list.append(self.description)
        self.label_str_list.append(self.amount)
        self.label_str_list.append(self.blank)

        self.item = QListWidgetItem(self.listWidget)
        item_widget = CustomQWidget(self.label_str_list)
        self.item.setSizeHint(item_widget.sizeHint())
        self.item.setWhatsThis(self.amount)
        self.item.setData(QtCore.Qt.UserRole, self.label_str_list)
        self.listWidget.addItem(self.item)
        self.listWidget.setItemWidget(self.item, item_widget)
        self.update_balance()
        self.clear_inputs()

    def add_item_as_deposit(self):
        try:
            self.amount = float(self.amountText.text())
            if self.amount == 0.0:
                raise ValueError
        except ValueError:
            show_warning('Amount is Invalid', 'Please enter a Valid amount other than zero and use .(point) for decimals')
            self.clear_inputs()
            return

        self.description = self.descriptionText.text()
        amount_give = abs(self.amount)
        if self.balance >= 0.0:
            self.balance += amount_give
        elif abs(self.balance) <= amount_give:
            self.balance = amount_give - abs(self.balance)
        else:
            self.balance = -1 * (abs(self.balance) - amount_give)
        num = Decimal(str(self.balance))
        self.balance = float(round(num, 2))
        self.amount = '+' + str(abs(self.amount))
        self.description = '{:>40}'.format(self.description)
        self.amount = '{:>40}'.format(self.amount)

        self.label_str_list.append(self.description)
        self.label_str_list.append(self.blank)
        self.label_str_list.append(self.amount)

        self.item = QListWidgetItem(self.listWidget)
        item_widget = CustomQWidget(self.label_str_list)
        self.item.setSizeHint(item_widget.sizeHint())
        self.item.setWhatsThis(self.amount)
        self.item.setData(QtCore.Qt.UserRole, self.label_str_list)
        self.listWidget.addItem(self.item)
        self.listWidget.setItemWidget(self.item, item_widget)
        self.update_balance()
        self.clear_inputs()

    def remove_sel_item(self):
        list_items = self.listWidget.selectedItems()
        if not list_items:
            show_warning('No item is selected', 'Please select an item to remove')
            return
        for item in list_items:
            self.listWidget.takeItem(self.listWidget.row(item))
            amount = float(item.whatsThis())
            self.balance -= amount
            num = Decimal(str(self.balance))
            self.balance = float(round(num, 2))

        self.update_balance()

    def update_balance(self):
        self.balanceEdit.setText(str(self.balance))

    def get_file_name(self):
        # dialog = QInputDialog()
        # dialog.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        text, ok_pressed = QInputDialog().getText(self, "Save as txt", "Please enter name of txt file:",
                                                  QLineEdit.Normal,
                                                  "")
        if ok_pressed and text != '':
            return text
        elif ok_pressed and text == '':
            show_warning('Invalid file name', 'Try the menu button again !')
            return ''
        else:
            return ''

    def save_printout(self):
        if self.listWidget.count() == 0:
            show_warning('There is no printout to save', 'Please prepare a printout first!')
            return
        file_name = self.get_file_name()
        if file_name == '':
            return
        file_name = 'txt/' + file_name + '.txt'
        if path.exists(file_name):
            show_warning('It already exists', 'Please enter a unique File name !')
            return
        items = []
        for index in range(self.listWidget.count()):
            items.append(self.listWidget.item(index))
        with open(file_name, 'w') as f:
            for item in items:
                f.write(''.join(item.data(QtCore.Qt.UserRole)))
                f.write('\n')

            balance = 'Balance: ' + str(self.balance) + ' \u20ac'
            under_score = '_' * len(balance)
            f.write('{:>120}'.format(under_score))
            f.write('\n')
            f.write('{:>120}'.format(balance))

    def trash_printout(self):
        self.clear_inputs()
        self.listWidget.clear()
        self.balanceEdit.setText('')
        self.balance = 0.0


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
