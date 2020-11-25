'''模块加载部分'''
print('模块加载中......')
import os
from module.estimator import TfPoseEstimator
import cv2
import time

print('模块加载完成......')

'''运行部分'''
print('开始运行......')


def show_camera(args, filename):
    # 获取w,h
    w, h = [int(x) for x in args['resize'].split('x')]

    # 创建TfPoseEstimator对象
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    # 打开摄像头
    print('开启摄像头......')
    if filename == None:
        cam = cv2.VideoCapture(args['camera'])
    else:
        cam = cv2.VideoCapture(filename)

    ret_val, image = cam.read()
    count = 0

    while ret_val:

        if count % 1 == 0:
            time1 = time.time()
            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args['resize_out_ratio'])
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.imshow('tf-pose-estimation result', image)
        count += 1
        cv2.waitKey(1)

        ret_val, image = cam.read()

    cv2.destroyAllWindows()
    print('摄像头关闭......')


def camera(model_name, filename=None):
    model_path = './resoure/graph'
    model = os.listdir(model_path)
    if model_name in model:
        args = {'model': './resoure/graph/' + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio': 4.0,
                'camera': 0}
        show_camera(args, filename)
    else:
        print('模型名称错误')


# camera('mobilenet_thin')
camera('mobilenet_thin', './resoure/video/dance.mp4')

print('运行完成......')