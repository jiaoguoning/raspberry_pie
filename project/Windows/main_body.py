from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot,Qt
from PyQt5.QtGui import QIcon,QImage, QPixmap
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox,QLabel
import qtawesome
import cv2
import os
import time
import shutil
import matplotlib.pyplot as plt
import threading
import sys
sys.path.append("..")
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
        self.setWindowIcon(QIcon('./resoure/image/瑜伽.png'))

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

        #self.right_widget.setStyleSheet('''background-color:rgb(155, 150, 100);border-radius: 5px; color: rgb(255, 255, 255);''')

        self.right_recommend_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_recommend_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_recommend_widget.setLayout(self.right_recommend_layout)
        self.right_layout.addWidget(self.right_recommend_widget)

        #self.right_recommend_widget.setStyleSheet('''background-color:green;border-radius: 5px; color: rgb(255, 255, 255);''')

        self.stats = 'first'

        self.right_ds_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_ds_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_ds_widget.setLayout(self.right_ds_layout)
        self.right_recommend_layout.addWidget(self.right_ds_widget,0,0,1,12)


        self.right_ds_widget.setStyleSheet('''background-color:rgb(211,211,211);border-radius: 5px; color: rgb(255, 255, 255);''')

        DaoRu = QtWidgets.QToolButton()
        DaoRu.setText('导入视频')  # 设置按钮文本
        DaoRu.setIcon(QIcon('./resoure/image/import.png'))  # 设置按钮图标
        DaoRu.setIconSize(QtCore.QSize(600,25))  # 设置图标大小
        DaoRu.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
        self.right_ds_layout.addWidget(DaoRu)
        DaoRu.clicked.connect(self.add_video)

        self.right_d_widget = QtWidgets.QWidget()  # 推荐封面部件
        self.right_d_layout = QtWidgets.QGridLayout() # 推荐封面网格布局
        self.right_d_widget.setLayout(self.right_d_layout)
        self.right_recommend_layout.addWidget(self.right_d_widget,2,0,10,12)

        self.right_d_widget.setStyleSheet('''background-color:rgb(211,211,211);border-radius: 5px; color: rgb(255, 255, 255);''')

        self.H = list()
        for i in range(12):
            right_H_widget = QtWidgets.QWidget()  # 推荐封面部件
            right_H_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            right_H_widget.setLayout(right_H_layout)
            self.H.append(right_H_layout)
            self.right_d_layout.addWidget(right_H_widget, i//4, i%4, 1, 1)
            right_H_widget.setStyleSheet('''background-color:white;border-radius: 5px; color: rgb(255, 255, 255);''')


        self.recommend_button = list()
        path = '../resoure/video/模型标记视频/'
        biaoji = [i for i in os.listdir(path) if i[-4:]=='.avi']
        for i in range(len(biaoji)):
            self.recommend_button.append(QtWidgets.QToolButton())
            recommend_button_ = self.recommend_button[-1]

            recommend_button_.clicked.connect(self.into)

            recommend_button_.setObjectName(biaoji[i])

            recommend_button_.setText(biaoji[i])  # 设置按钮文本
            cam = cv2.VideoCapture(path+biaoji[i])
            #读取第二帧作为封面
            ret_val, image = cam.read()
            ret_val, image = cam.read()
            if ret_val:
                image = cv2.resize(image,(125,100))
                cv2.imwrite('./resoure/video_img/img'+str(i)+'.jpg', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

                recommend_button_.setIcon(QIcon('./resoure/video_img/img'+str(i)+'.jpg'))  # 设置按钮图标

                recommend_button_.setIconSize(QtCore.QSize(150, 100))  # 设置图标大小
                recommend_button_.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
                self.H[i].addWidget(recommend_button_, 0,0,1,1)

                recommend_button_.setStyleSheet('''background-color:rgb(169,169,169);border-radius: 5px; color: rgb(255, 255, 255);''')

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
            yuanshi = os.listdir('../resoure/video/原始视频/')
            biaoji = os.listdir('../resoure/video/模型标记视频')
            if fullflname in yuanshi:
                QMessageBox.information(self, "提示", "模型载入中，请稍等...")
                times = time.time()
                film('mobilenet_thin', fullflname , fullflname.split('.')[0]+'.avi')
                QMessageBox.information(self, "提示", "模型载入成功,用时:"+str(time.time()-times)+'s',QMessageBox.Yes)

                if fullflname.split('.')[0]+'.avi'  not in biaoji:

                    t = QtWidgets.QToolButton()

                    t.clicked.connect(self.into)

                    t.setText(fullflname.split('.')[0]+'.avi')  # 设置按钮文本

                    t.setObjectName(fullflname.split('.')[0]+'.avi')

                    cam = cv2.VideoCapture('../resoure/video/模型标记视频/'+fullflname.split('.')[0]+'.avi')
                    # 读取第二帧作为封面
                    ret_val, image = cam.read()
                    ret_val, image = cam.read()
                    if ret_val:
                        image = cv2.resize(image, (125, 100))
                        cv2.imwrite('./resoure/video_img/'+fullflname.split('.')[0]+'.jpg', image,
                                    [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
                        t.setIcon(QIcon('./resoure/video_img/'+fullflname.split('.')[0]+'.jpg'))  # 设置按钮图标
                        t.setIconSize(QtCore.QSize(150, 100))  # 设置图标大小
                        t.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文

                        self.H[len(biaoji)-1].addWidget(t,0,0,1,1)

                        t.setStyleSheet('''background-color:rgb(169,169,169);border-radius: 5px; color: rgb(255, 255, 255);''')

                        self.recommend_button.append(t)

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
            self.setWindowState(Qt.WindowMazximized)

    @pyqtSlot()
    def mini(self):
        self.setWindowState(Qt.WindowMinimized)

    @pyqtSlot()
    def into(self):
        #打开视频
        video_name = self.sender().objectName()
        path = '../resoure/video/模型标记视频/'
        file_path = path + video_name
        #self.video = cv2.VideoCapture(path+video_name)
        #self.ret_val1, self.image1 = self.video.read()
        #self.ret_val1, self.image1 = self.video.read()

        #打开摄像头对象
        #self.camera = cv2.VideoCapture(0)
        #ret_val2, image2 = self.video.read()

        #页面加载
        self.right_recommend_widget.hide()
        if self.stats != 'first':
            self.right_recommend_widget_video.hide()
        else:
            self.right_recommend_widget_video = QtWidgets.QWidget()  # 推荐封面部件
            self.right_recommend_layout_video = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_recommend_widget_video.setLayout(self.right_recommend_layout_video)
            self.right_layout.addWidget(self.right_recommend_widget_video)

            self.right_ps_widget = QtWidgets.QWidget()  # 推荐封面部件
            self.right_ps_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_ps_widget.setLayout(self.right_ps_layout)
            self.right_recommend_layout_video.addWidget(self.right_ps_widget, 0, 0, 1, 5)

            self.right_ps_widget.setStyleSheet(
                '''background-color:rgb(211,211,211);border-radius: 5px; color: rgb(255, 255, 255);''')

            Dao = QtWidgets.QToolButton()
            Dao.setText('回退')  # 设置按钮文本
            Dao.setIcon(QIcon('./resoure/image/back.png'))  # 设置按钮图标
            Dao.setIconSize(QtCore.QSize(25,25))  # 设置图标大小
            Dao.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)  # 设置按钮形式为上图下文
            self.right_ps_layout.addWidget(Dao,0,0)
            Dao.clicked.connect(self.back)
            self.stats == 'second'

            Daos = QtWidgets.QToolButton()
            Daos.setIconSize(QtCore.QSize(600, 25))  # 设置图标大小
            self.right_ps_layout.addWidget(Daos, 0, 1)

            self.right_p_widget = QtWidgets.QWidget()  # 推荐封面部件
            self.right_p_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_p_widget.setLayout(self.right_p_layout)
            self.right_recommend_layout_video.addWidget(self.right_p_widget, 1, 0, 10, 5)

            self.right_p_widget.setStyleSheet('''background-color:rgb(211,211,211);border-radius: 5px; color: rgb(255, 255, 255);''')




            #底部暂停按键
            self.right_an_widget = QtWidgets.QWidget()  # 推荐封面部件
            self.right_an_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_an_widget.setLayout(self.right_an_layout)
            self.right_p_layout.addWidget(self.right_an_widget, 10, 0, 1, 2)

            self.right_an_widget.setStyleSheet('''background-color:rgb(245,245,245);border-radius: 5px; color: rgb(255, 255, 255);''')

            #播放按键
            self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
            self.right_process_bar.setValue(0)
            self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
            self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

            self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
            self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
            self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

            self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
            self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
            self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='#F76677', font=18), "")
            self.console_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.pause', color='#F76677', font=18), "")

            self.console_button_3.setIconSize(QtCore.QSize(30, 30))
            self.console_button_4.setIconSize(QtCore.QSize(30, 30))


            self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
            self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
            self.right_playconsole_layout.addWidget(self.console_button_4, 0, 1)
            self.console_button_4.hide()
            self.but_status = 'play'
            self.right_playconsole_layout.addWidget(self.console_button_3, 0, 1)
            self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

            self.right_an_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
            self.right_an_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)



            #摄像头
            self.right_she_widget = QtWidgets.QWidget()  # 推荐封面部件
            self.right_she_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_she_widget.setLayout(self.right_she_layout)
            self.right_p_layout.addWidget(self.right_she_widget, 0 , 1, 9, 1)

            self.right_she_widget.setStyleSheet('''background-color:rgb(245,245,245);border-radius: 5px; color: rgb(255, 255, 255);''')

            self.shexiang = QtWidgets.QLabel()
            self.right_she_layout.addWidget(self.shexiang)

            self.she = Display(self,file_path=None)


            #标准视频
            self.right_biao_widget = QtWidgets.QWidget()  # 推荐封面部件
            self.right_biao_layout = QtWidgets.QGridLayout()  # 推荐封面网格布局
            self.right_biao_widget.setLayout(self.right_biao_layout)
            self.right_p_layout.addWidget(self.right_biao_widget, 0, 0, 9, 1)

            self.right_biao_widget.setStyleSheet('''background-color:rgb(245,245,245);border-radius: 5px; color: rgb(255, 255, 255);''')

            self.shiping = QtWidgets.QLabel()
            self.right_biao_layout.addWidget(self.shiping)

            self.dis = Display(self,file_path)
            self.console_button_3.clicked.connect(self.open)
            self.console_button_4.clicked.connect(self.close)






    @pyqtSlot()
    def back(self):
        self.right_recommend_widget_video.hide()
        self.right_recommend_widget.show()

    @pyqtSlot()
    def open(self):
        self.console_button_3.hide()
        self.console_button_4.show()
        self.but_status = 'pause'
        self.dis.Open()
        self.she.Open()
    @pyqtSlot()
    def close(self):
        self.console_button_4.hide()
        self.console_button_3.show()
        self.but_status = 'play'
        self.dis.Close()
        self.she.Close()


    @pyqtSlot()
    def backword(self):
        pass
    @pyqtSlot()
    def forword(self):
        pass



class Display:
    def __init__(self,ui,file_path=None):
        self.ui = ui
        # 默认视频源为相机
        if file_path==None:
            self.isCamera = True
            self.cap = cv2.VideoCapture(0)
            success, frame = self.cap.read()
        else:
            self.isCamera = False
            self.file_path = file_path
        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()

    def Open(self):
        self.x = 0
        if not self.isCamera:
            self.cap = cv2.VideoCapture(self.file_path)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
            th = threading.Thread(target=self.Display)
            th.start()
            print('打开视频完成')
        else:
            th = threading.Thread(target=self.Display)
            th.start()
            print('开启摄像头完成')
        # 创建视频显示线程



    def Close(self):
        # 关闭事件设为触发，关闭视频播放
        self.stopEvent.set()

    def Display(self):
        while self.cap.isOpened():
            if self.x > 3:
                success, frame = self.cap.read()
                # RGB转BGR
                if success:
                    frame = cv2.resize(frame,(300,300))
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    if self.isCamera:
                        imagess = QPixmap.fromImage(img)
                        self.ui.shexiang.setPixmap(imagess)
                    else:
                        self.ui.shiping.setPixmap(QPixmap.fromImage(img))
                        time.sleep(1/self.frameRate)

                # 判断关闭事件是否已触发
                if True == self.stopEvent.is_set():
                    # 关闭事件置为未触发，清空显示label
                    self.stopEvent.clear()
                    if self.isCamera:
                        self.ui.shexiang.clear()
                    else:
                        self.ui.shiping.clear()
                    break
            else:
                path = './resoure/image/'
                img = cv2.imread(path+str(3-self.x)+'.png')
                frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                imgae = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.ui.shexiang.setPixmap(QPixmap.fromImage(imgae))
                self.ui.shiping.setPixmap(QPixmap.fromImage(imgae))
                time.sleep(1)
                self.ui.shexiang.clear()
                self.ui.shiping.clear()
                self.x += 1




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    sys.exit(app.exec_())