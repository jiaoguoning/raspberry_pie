'''模块加载部分'''
print('模块加载中......')
import os
from module.estimator import TfPoseEstimator
import cv2
print('模块加载完成......')




'''运行部分'''
print('开始运行......')
def show_camera(args):
    # 获取w,h
    w, h = [int(x) for x in args['resize'].split('x')]

    # 创建TfPoseEstimator对象
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    #打开摄像头
    print('开启摄像头......')
    cam = cv2.VideoCapture(args['camera'], cv2.CAP_DSHOW)

    ret_val, image = cam.read()
    count = 0

    while True:
        ret_val, image = cam.read()

        if count%3 == 0 :
            humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args['resize_out_ratio'])
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            cv2.imshow('tf-pose-estimation result', image)

        count += 1
        cv2.waitKey(1)

    cv2.destroyAllWindows()
    print('摄像头关闭......')


def camera(model_name):
    model_path = './resoure/graph'
    model = os.listdir(model_path)
    if model_name in model:
        args = {'model': './resoure/graph/' + model_name + '/graph_opt.pb',
                'resize': '432x368',
                'resize_out_ratio':4.0,
                'camera': 0}
        show_camera(args)
    else:
        print('模型名称错误')

camera('mobilenet_v2_small')

print('运行完成......')