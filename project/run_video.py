'''模块加载部分'''
print('模块加载中......')
import os
from module.estimator import TfPoseEstimator
import cv2
import time
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
    cam = cv2.VideoCapture(args['video'])
    ret_val, image = cam.read()
    count = 0
    while ret_val:
        if count%3 == 0 and count >= 200:
            time1 = time.time()
            humans = e.inference(image, upsample_size=args['resize_out_ratio'])
            image = TfPoseEstimator.draw_humans(image, humans)
            cv2.imshow('tf-pose-estimation result', image)
            print('fps:',time.time()-time1)
        count += 1
        cv2.waitKey(1)
        ret_val, image = cam.read()
    cv2.destroyAllWindows()
    print('视频关闭......')
    print('一共%d帧画面'%count)

def video(model_name,video_name):
    model_path = './resoure/graph'
    video_path = './resoure/video'
    model = os.listdir(model_path)
    videos = os.listdir(video_path)
    if model_name in model and video_name in videos:
        args = {'video':'./resoure/video/'+video_name,
                'model': './resoure/graph/' + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio':2.0,
                'camera': 0}
        show_video(args)
    else:
        print('模型名称错误')

video('mobilenet_v2_small','dance.mp4')

print('运行完成......')