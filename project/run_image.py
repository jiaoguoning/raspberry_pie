print('加载模块中......')
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
        image, humans_points = TfPoseEstimator.draw_humans(image, humans)
        #展示图片的时候将BGR模式图片转化为RGB图片
        imgg = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        imgg.show()
        print('Use time:%.2f'%(time.time()-time1))
        return humans_points

def image_show(model_name,imag):
        img_path = './resoure/image'
        file = os.listdir(img_path)
        image = [i for i in file if i.split('.')[-1]=='jpg']
        model_path = './resoure/graph'
        model = os.listdir(model_path)
        humans = []
        for i in imag:
                if model_name in model and i in image:
                        args = {'image': img_path + '/' + i ,
                                'model': './resoure/graph/'+model_name+'/graph_opt.pb',
                                'resize': '432x368',
                                'resize_out_ratio': 2.0}
                        humans_points = show_image(args)
                        humans.append(humans_points)
                else:
                        print('图片名称或者模型名称错误')
        return humans

def cal_line(point1, point2):
        '''计算两点之间的距离'''
        x1, y1 = point1[0], point2[1]
        x2, y2 = point2[0], point2[1]
        recose = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
        return recose

def error_rate(two_points_sets):
        origin_sets, pred_sets = two_points_sets[0], two_points_sets[1]
        origin_line = cal_line(origin_sets[0][2], origin_sets[0][5])
        pred_line = cal_line(pred_sets[0][2], pred_sets[0][5])
        # 从预测图像到标记图形的变换比例
        rate = pred_line / origin_line
        # 选取右肩膀的点作为基础点，测量原图点对距离该点的距离
        org_distance = []
        pred_distance = []
        for i in [x for x in range(19) if x != 2]:
                if origin_sets[0][i][0] != 0 and pred_sets[0][i][0] != 0 \
                        and origin_sets[0][i][1] != 0 and pred_sets[0][i][1] != 0:
                        t = cal_line(origin_sets[0][2], origin_sets[0][i])
                        d = cal_line(pred_sets[0][2], pred_sets[0][i])
                        org_distance.append(t)
                        pred_distance.append(d)
        pred_distance = [x / rate for x in pred_distance]
        sum = 0
        for i, j in zip(org_distance, pred_distance):
                sum += abs(i - j)
        print(sum)


        return sum


#image_show('mobilenet_v2_small','apink2.jpg')
imgs = ['hand1.jpg', 'hand1.jpg']
back_points = image_show('mobilenet_thin',imgs)
error_rate(back_points)
print('运行完成......')