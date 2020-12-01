'''模块加载部分'''
print('模块加载中......')
import os
from module.estimator import TfPoseEstimator
import cv2
import time
print('模块加载完成......')

'''运行部分'''
def show_video(args,video_label):
    # 获取w,h
    w, h = [int(x) for x in args['resize'].split('x')]
    # 创建TfPoseEstimator对象
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    #打开摄像头
    print('打开视频......')
    cam = cv2.VideoCapture(args['video'])
    ret_val, image = cam.read()
    count = 0
    #写出到.mp4文件
    ret_val, image = cam.read()
    shape = (image.shape[1],image.shape[0])
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWrite = cv2.VideoWriter(video_label, fourcc, 20.0, shape)
    while ret_val :
        if count%50 == 0:
            time1 = time.time()
            humans = e.inference(image, upsample_size=args['resize_out_ratio'])
            image = TfPoseEstimator.draw_humans(image, humans)[0]
            videoWrite.write(image)  #输出到.mp4文件
            print('fps:',time.time()-time1,';',count)

        cv2.waitKey(1)
        count += 1
        ret_val, image = cam.read()
    videoWrite.release()
    cv2.destroyAllWindows()
    print('视频关闭......')
    print('一共%d帧画面'%count)

def video(model_name,video_name,video_label):
    model_path = './resoure/graph/'
    video_path = './resoure/video/原始视频/'
    model = os.listdir(model_path)
    videos = os.listdir(video_path)
    if model_name in model and video_name in videos:
        args = {'video':video_path+video_name,
                'model': model_path + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio':5.0,
                'camera': 0}
        show_video(args,video_label)
    else:
        print('模型名称错误')

#模型地址，原视频地址，保存视频的名称
<<<<<<< HEAD:project/导出视频.py
video('mobilenet_thin','demo1.mp4','demo1.avi')

print('运行完成......')
=======
#video('mobilenet_thin','demo2.mp4','./resoure/video/模型标记视频/'+'demo2.avi')
>>>>>>> d1cd463a322b88b1a99d63ef9e1f1e3e4427d19b:project/daochu.py
