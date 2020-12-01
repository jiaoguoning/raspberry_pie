'''模块加载部分'''
print('模块加载中......')
import os
from module.estimator import TfPoseEstimator
import cv2
import time
import numpy as np
print('模块加载完成......')

'''运行部分'''
print('开始运行......')
def show_video(args):
    # 获取w,h
    w, h = [int(x) for x in args['resize'].split('x')]
    # 创建TfPoseEstimator对象
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    #打开摄像头
    print('打开视频......')
    cam1 = cv2.VideoCapture(args['video'][0])
    cam2 = cv2.VideoCapture(args['video'][1])
    ret_val1, image1 = cam1.read()
    ret_val2, image2 = cam2.read()
    count = 0
    while True and ret_val2 :
        time1 = time.time()
        if count%5 == 0:
            humans = e.inference(image1, upsample_size=args['resize_out_ratio'])
            image1 = TfPoseEstimator.draw_humans(image1, humans)
            image2,image1 = image2[:,350:-350,:],image1[:,350:-350,:]
            image = np.concatenate((image1,image2), axis = 1)
            cv2.imshow('frame1', image)   #显示标记结果
            print('fps:',time.time()-time1)
        count += 1
        cv2.waitKey(1)
        ret_val1, image1 = cam1.read()
        ret_val2, image2 = cam2.read()
    cv2.destroyAllWindows()
    print('视频关闭......')
    print('一共%d帧画面'%count)

def video(model_name,video_name,video_name2):
    model_path = './resoure/graph/'
    video_path1 = './resoure/video/原始视频/'
    video_path2 = './resoure/video/模型标记视频/'
    model = os.listdir(model_path)
    videos1 = os.listdir(video_path1)
    videos2 = os.listdir(video_path2)
    if model_name in model and video_name in videos1 and video_name2 in videos2:
        args = {'video':[video_path1+video_name,video_path2+video_name2],
                'model': model_path + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio':2.0,
                'camera': 0}
        show_video(args)
    else:
        print('模型名称错误')

#模型地址，原视频地址，保存视频的名称
video('mobilenet_thin','demo1.mp4','demo2.avi')

print('运行完成......')