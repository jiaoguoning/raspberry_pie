print('加载模块中......')
from module.common import read_imgfile
from module.estimator import TfPoseEstimator
import cv2
from PIL import Image
import os
print('模块加载完成......')

print('开始运行......')
def show_image(args):
        #获取w,h
        w,h = [int(x) for x in args['resize'].split('x')]
        #获取图片
        image = read_imgfile(args['image'], None, None)

        #创建TfPoseEstimator对象
        e = TfPoseEstimator(args['model'], target_size=(w, h))

        #调用TfPoseEstimator对象的inference方法
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args['resize_out_ratio'])
        #调用TfPoseEstimator静态方法draw_hunmans
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        #展示图片的时候将BGR模式图片转化为RGB图片
        imgg = Image.fprint('加载模块中......')
from module.common import read_imgfile
from module.estimator import TfPoseEstimator
import cv2
from PIL import Image
import os
import time
print('模块加载完成......')

print('开始运行......')
def show_image(args):
        #获取w,h
        w,h = [int(x) for x in args['resize'].split('x')]
        #获取图片
        image = read_imgfile(args['image'], None, None)
        #创建TfPoseEstimator对象
        e = TfPoseEstimator(args['model'], target_size=(w, h))
        #调用TfPoseEstimator对象的inference方法
        time1 = time.time()
        humans = e.inference(image,upsample_size=args['resize_out_ratio'])
        #调用TfPoseEstimator静态方法draw_hunmans
        image = TfPoseEstimator.draw_humans(image, humans)
        #展示图片的时候将BGR模式图片转化为RGB图片
        imgg = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        imgg.show()
        print('Use time:%.2f'%(time.time()-time1))

def image_show(model_name,imag):
        img_path = './resoure/image'
        file = os.listdir(img_path)
        image = [i for i in file if i.split('.')[-1]=='jpg']
        model_path = './resoure/graph'
        model = os.listdir(model_path)
        if model_name in model and imag in image:
                args = {'image': img_path + '/' + imag ,
                        'model': './resoure/graph/'+model_name+'/graph_opt.pb',
                        'resize': '432x368',
                        'resize_out_ratio': 2.0}
                show_image(args)
        else:
                print('图片名称或者模型名称错误')

#image_show('mobilenet_v2_small','apink2.jpg')
image_show('mobilenet_v2_small','hand1.jpg')

print('运行完成......')romarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        imgg.show()

def image(model_name,imag):
        img_path = './resoure/image'
        file = os.listdir(img_path)
        image = [i for i in file if i.split('.')[-1]=='jpg']
        model_path = './resoure/graph'
        model = os.listdir(model_path)
        if model_name in model and imag in image:
                args = {'image': img_path + '/' + imag ,
                        'model': './resoure/graph/'+model_name+'/graph_opt.pb',
                        'resize': '432x368',
                        'resize_out_ratio': 4.0}
                show_image(args)
        else:
                print('图片名称或者模型名称错误')

image('mobilenet_v2_small','golf.jpg')


print('运行完成......')