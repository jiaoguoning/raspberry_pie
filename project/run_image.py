import os
import cv2
from PIL import Image

from module.common import read_imgfile
from module.estimator import TfPoseEstimator
from module.evaluation import human_vector

def show_image(args):
    w, h = [int(x) for x in args['resize'].split('x')]
    image = read_imgfile(args['image'], None, None)
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    humans = e.inference(image, upsample_size=args['resize_out_ratio'])
    image, humans_points = TfPoseEstimator.draw_humans(image, humans)
    imgg = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    imgg.show()
    return humans_points


def image_show(model_name, imag):
    img_path = './resoure/image'
    file = os.listdir(img_path)
    image = [i for i in file if i.split('.')[-1] == 'jpg']
    model_path = './resoure/graph'
    model = os.listdir(model_path)
    humans = []
    for i in imag:
        if model_name in model and i in image:
            args = {'image': img_path + '/' + i,
                    'model': './resoure/graph/' + model_name + '/graph_opt.pb',
                    'resize': '432x368',
                    'resize_out_ratio': 2.0}
            humans_points = show_image(args)
            humans.append(humans_points)
        else:
            print('图片名称或者模型名称错误')
    return humans


imgs = ['apink1.jpg', 'apink1_crop.jpg']
back_points = image_show('mobilenet_thin', imgs)
juge = human_vector(back_points)
juge.compare_forward()
