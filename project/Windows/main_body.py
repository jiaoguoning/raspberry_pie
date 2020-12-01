from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
import qtawesome
import cv2
import os
import time
import shutil
import daochu

def film(model_name,video_name,video_label):
    model_path = '../resoure/graph/'
    video_path = '../resoure/video/原始视频/'
    model = os.listdir(model_path)
    videos = os.listdir(video_path)
    if model_name in model and video_name in videos:
        args = {'video':video_path+video_name,
                'model': model_path + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio':2.0,
                'camera': 0}
        daochu.show_video(args, '../resoure/video/模型标记视频/'+video_label)
    else:
        print('模型名称错误')

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.left_close.clicked.connect(self.closes)
        self.left_visit.clicked.connect(self.big)
        self.left_mini.clicked.connect(self.mini)

    def initUI(self):


        #左侧部分
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格

        #窗口操作的部分
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        #左侧边栏
        self.left_label_1 = QtWidgets.QPushButton("运动锻炼")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("电影推荐")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("关于我们")
        self.left_label_3.setObjectName('left_label')

        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.calendar', color='white'), "健身锻炼")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.rss', color='white'), "热门推荐")
        self.left_button_2.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "在线观影")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "下载管理")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "本地收藏")
        self.left_button_6.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.group', color='white'), "客服热线")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "问题反馈")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        self.left_widget.setStyleSheet('''
            QPushButton{border:none;color:white;}
            QPushButton#left_label{
                border:none;
                border-bottom:1px solid white;
                font-size:18px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            QWidget#left_widget{
                background:gray;
                border-top:1px solid white;
                border-bottom:1px solid white;
                border-left:1px solid white;
                border-top-left-radius:10px;
                border-bottom-left-radius:10px;
            }
        ''')



        #右侧部分
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格

        DaoRu = QtWidgets.QToolButton()
        DaoRu.setText('导入视频')  # 设置按钮文本
        DaoRu.setIcon(QIcon('./resoure/image/文件导入.png'))  # 设置按钮图标
        DaoRu.setIconSize(QtCore.QSize(100,50))  # 设置图标大小
        DaoRu.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.right_layout.addWidget(DaoRu,0,0)
        DaoRu.clicked.connect(self.add_video)

        self.recommend_button = list()
        path = '../resoure/video/模型标记视频/'
        videoss = [i for i in os.listdir(path) if i[-4:]=='.avi']
        print(videoss)
        for i in range(len(videoss)):
            self.recommend_button.append(QtWidgets.QToolButton())
            recommend_button_ = self.recommend_button[-1]
            recommend_button_.setText(videoss[i])  # 设置按钮文本

            cam = cv2.VideoCapture(path+videoss[i])

            #读取第二帧作为封面
            ret_val, image = cam.read()
            ret_val, image = cam.read()
            if ret_val:
                cv2.imwrite('./resoure/video_img/img'+str(i)+'.jpg', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

                recommend_button_.setIcon(QIcon('./resoure/video_img/img'+str(i)+'.jpg'))  # 设置按钮图标

                recommend_button_.setIconSize(QtCore.QSize(150, 100))  # 设置图标大小
                recommend_button_.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
                self.right_layout.addWidget(recommend_button_, i//4+1, i%4 )



        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            }
        ''')

        #主窗口部分
        self.setFixedSize(900, 650)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.main_layout.addWidget(self.left_widget,0,0,12,2) # 左侧部件在第0行第0列，占8行3列
        self.main_layout.addWidget(self.right_widget,0,2,12,10) # 右侧部件在第0行第3列，占8行9列
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        self.setWindowOpacity(1)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)

    @pyqtSlot()
    def add_video(self):

        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', '')
        filepath, fullflname = os.path.split(openfile_name[0])
        if fullflname.split('.')[-1] == 'mp4':
            #复制视频
            shutil.copyfile(openfile_name[0], '../resoure/video/原始视频/'+fullflname)
            QMessageBox.information(self, "提示", "文件导入成功",QMessageBox.Yes)
            #训练视频
            videossss = os.listdir('../resoure/video/原始视频/')
            if fullflname in videossss:
                QMessageBox.information(self, "提示", "模型载入中，请稍等...")
                times = time.time()
                film('mobilenet_thin', fullflname , fullflname.split('.')[0]+'.avi')
                QMessageBox.information(self, "提示", "模型载入成功,用时:"+str(time.time()-times)+'s',QMessageBox.Yes)

                path = '../resoure/video/模型标记视频/'
                video = [i for i in os.listdir(path) if i[-4:] == '.avi']

                t = QtWidgets.QToolButton()
                t.setText(fullflname.split('.')[0]+'.avi')  # 设置按钮文本

                print('../resoure/video/模型标记视频/'+fullflname.split('.')[0]+'.avi')
                cam = cv2.VideoCapture('../resoure/video/模型标记视频/'+fullflname.split('.')[0]+'.avi')
                # 读取第二帧作为封面
                ret_val, image = cam.read()
                ret_val, image = cam.read()
                if ret_val:
                    cv2.imwrite('./resoure/video_img/'+fullflname.split('.')[0]+'.jpg', image,
                                [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
                    t.setIcon(QIcon('./resoure/video_img/'+fullflname.split('.')[0]+'.jpg'))  # 设置按钮图标
                    t.setIconSize(QtCore.QSize(150, 100))  # 设置图标大小
                    t.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文

                    self.right_layout.addWidget(t, len(video)//4 + 1, len(video)%4)
                    QApplication.processEvents()
                    time.sleep(0.5)
            else:
                QMessageBox.information(self, "提示", "原始视频文件夹中无此文件，请重新导入。", QMessageBox.Yes)
        else:
            QMessageBox.information(self, "提示", "文件不是mp4格式文件，请重新选择。", QMessageBox.Yes)

    @pyqtSlot()
    def closes(self):
        self.close()
    @pyqtSlot()
    def big(self):
        if self.windowState()==Qt.WindowMaximized:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowMaximized)
    @pyqtSlot()
    def mini(self):
        self.setWindowState(Qt.WindowMinimized)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    sys.exit(app.exec_())