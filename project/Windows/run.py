from Windows.register import LoginForm
from Windows.main_body import MainUi

# run.py

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox

class mywindow(LoginForm):
    def __init__(self):
        super(mywindow, self).__init__()
        self.btn.clicked.connect(self.printState)

    @pyqtSlot()
    def printState(self):
        users = self.username.text()+' '+self.password.text()
        if users in self.user:
            print('密码正确')
            self.close()
            gi.show()
        else:
            self.username.setText('')
            self.password.setText('')
            QMessageBox.about(self, "提示", "账号或者密码错误！请重新输入。")


class window_ok(MainUi):
    def __init__(self):
        super(window_ok, self).__init__()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = mywindow()
    gi = window_ok()
    ui.show()
    sys.exit(app.exec_())