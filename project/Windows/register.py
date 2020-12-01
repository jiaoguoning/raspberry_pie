import sys
import main_body as ma

from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import Qt,pyqtSlot,QCoreApplication
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont, QIcon,QActionEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QHBoxLayout, QFormLayout, \
    QPushButton, QLineEdit,QAction,QMessageBox


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.user = list()#储存用户密码
        with open('user_name.txt','r') as f:  #读入用户账户和密码信息
            line = f.readlines()
            for i in line:
                self.user.append(i.rstrip())
        self.initUI()

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setObjectName("loginWindow")
        self.setStyleSheet('#loginWindow{background-color:#DCDCDC}')
        self.setFixedSize(650, 400)
        self.setWindowTitle("登录")
        self.setWindowIcon(QIcon('./resoure/image/瑜伽.png'))

        self.text = "       智能AI瑜伽教练"

        # 添加顶部logo图片
        pixmap = QPixmap("./resoure/image/背景.png")
        scaredPixmap = pixmap.scaled(650, 140)
        label = QLabel(self)
        label.setPixmap(scaredPixmap)

        # 绘制顶部文字
        lbl_logo = QLabel(self)
        lbl_logo.setText(self.text)
        lbl_logo.setStyleSheet("QWidget{color:white;font-weight:600;background: transparent;font-size:30px;}")
        lbl_logo.setFont(QFont("Microsoft YaHei"))
        lbl_logo.move(150, 50)
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.raise_()

        # 登录表单内容部分
        login_widget = QWidget(self)
        login_widget.move(0, 140)
        login_widget.setGeometry(0, 140, 650, 260)

        hbox = QHBoxLayout()
        # 添加左侧logo
        logolb = QLabel(self)
        logopix = QPixmap("./resoure/image/插画.jpg")
        logopix_scared = logopix.scaled(200, 200)
        logolb.setPixmap(logopix_scared)
        logolb.setAlignment(Qt.AlignCenter)
        hbox.addWidget(logolb, 1)

        # 添加右侧表单
        fmlayout = QFormLayout()
        lbl_workerid = QLabel("用户名")
        lbl_workerid.setFont(QFont("Microsoft YaHei"))
        led_workerid = QLineEdit()
        self.username = led_workerid
        led_workerid.setFixedWidth(270)
        led_workerid.setFixedHeight(38)

        lbl_pwd = QLabel("密码")
        lbl_pwd.setFont(QFont("Microsoft YaHei"))
        led_pwd = QLineEdit()
        self.password = led_pwd
        led_pwd.setEchoMode(QLineEdit.Password)
        led_pwd.setFixedWidth(270)
        led_pwd.setFixedHeight(38)

        btn_login = QPushButton("登录")
        self.btn = btn_login
        btn_login.setFixedWidth(270)
        btn_login.setFixedHeight(40)
        btn_login.setFont(QFont("Microsoft YaHei"))
        btn_login.setObjectName("login_btn")
        btn_login.setStyleSheet("#login_btn{background-color:#2c7adf;color:white;border:none;border-radius:4px;}")

        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

        fmlayout.addRow(lbl_workerid, led_workerid)
        fmlayout.addRow(lbl_pwd, led_pwd)
        fmlayout.addWidget(btn_login)
        hbox.setAlignment(Qt.AlignCenter)
        # 调整间距
        fmlayout.setHorizontalSpacing(20)
        fmlayout.setVerticalSpacing(12)

        hbox.addLayout(fmlayout, 2)

        login_widget.setLayout(hbox)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginForm()
    ui.show()
    sys.exit(app.exec_())