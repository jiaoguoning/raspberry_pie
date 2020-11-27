import tensorflow as tf
from module.smoother import Smoother
import numpy as np
from module.common import CocoPart
from module import common
import cv2
import importlib

#导入c语言编译的模块
pkg = __name__.rpartition('.')[0]
mname = '.'.join((pkg, '_pafprocess')).lstrip('.')
pafprocess = importlib.import_module(mname)
_swig_property = property


class Human:
    __slots__ = ('body_parts', 'pairs', 'uidx_list', 'score')
    def __init__(self, pairs):
        self.body_parts = {}
        self.score = 0.0

class BodyPart:
    __slots__ = ('uidx', 'part_idx', 'x', 'y', 'score')
    def __init__(self, uidx, part_idx, x, y, score):
        self.uidx = uidx                #人的ID
        self.part_idx = part_idx        #人的特征点ID
        self.x, self.y = x, y           #人的特征点坐标
        self.score = score              #score
    def get_part_name(self):
        return CocoPart(self.part_idx)
    def __str__(self):
        return 'BodyPart:%d-(%.2f, %.2f) score=%.2f' % (self.part_idx, self.x, self.y, self.score)
    def __repr__(self):
        return self.__str__()

class PoseEstimator:
    def __init__(self):
        pass
    @staticmethod
    def estimate_paf(peaks, heat_mat, paf_mat):
        pafprocess.process_paf(peaks, heat_mat, paf_mat)
        humans = []  #检测到人就往里面添加
        for human_id in range(pafprocess.get_num_humans()):
            human = Human([])  #如果检测到人，生成一个Human对象
            is_added = False
            for part_idx in range(18):
                c_idx = int(pafprocess.get_part_cid(human_id, part_idx))#获得id
                if c_idx < 0:   #如果没有检测到人的特征点，则放弃添加此人到Humans列表
                    continue    #否则生成此人特征点的坐标信息和特征点ID，并将此人添加到Humans列表中
                is_added = True
                human.body_parts[part_idx] = BodyPart(    #身体每个部分坐标以及特征点ID
                    '%d-%d' % (human_id, part_idx), part_idx,
                    float(pafprocess.get_part_x(c_idx)) / heat_mat.shape[1],
                    float(pafprocess.get_part_y(c_idx)) / heat_mat.shape[0],
                    pafprocess.get_part_score(c_idx)
                )
            if is_added:#识别出人体特征点，将Human添加到Humans列表中
                score = pafprocess.get_score(human_id)
                human.score = score
                humans.append(human)
        return humans

class TfPoseEstimator:
    def __init__(self,graph_path,target_size=(320,240),
                 tf_config=None,trt_bool=False):
        self.target_size = target_size
        #读取模型文件
        print('读取模型中......')
        with tf.io.gfile.GFile(graph_path,'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
        print('读取模型完成......')

        self.graph = tf.compat.v1.get_default_graph()
        tf.import_graph_def(graph_def,name='TfPoseEstimator')
        self.persistent_sess = tf.compat.v1.Session(graph=self.graph,config=tf_config)
        self.tensor_image = self.graph.get_tensor_by_name('TfPoseEstimator/image:0')
        self.tensor_output = self.graph.get_tensor_by_name('TfPoseEstimator/Openpose/concat_stage7:0')
        self.tensor_heatMat = self.tensor_output[:, :, :, :19]
        self.tensor_pafMat = self.tensor_output[:, :, :, 19:]
        self.upsample_size = tf.compat.v1.placeholder(dtype=tf.int32, shape=(2,), name='upsample_size')
        self.tensor_heatMat_up = tf.compat.v1.image.resize_area(self.tensor_output[:, :, :, :19], self.upsample_size,
                                                      align_corners=False, name='upsample_heatmat')
        self.tensor_pafMat_up = tf.compat.v1.image.resize_area(self.tensor_output[:, :, :, 19:], self.upsample_size,
                                                     align_corners=False, name='upsample_pafmat')
        smoother = Smoother({'data': self.tensor_heatMat_up}, 25, 3.0, 19)
        gaussian_heatMat = smoother.get_output()
        max_pooled_in_tensor = tf.nn.pool(gaussian_heatMat, window_shape=(3, 3), pooling_type='MAX', padding='SAME')#Tensor("max_pool:0", shape=(?, ?, ?, 19), dtype=float32)
        self.tensor_peaks = tf.where(tf.equal(gaussian_heatMat, max_pooled_in_tensor), gaussian_heatMat,
                                     tf.zeros_like(gaussian_heatMat))
        self.heatMat = self.pafMat = None
        self.persistent_sess.run(tf.compat.v1.variables_initializer(
            [v for v in tf.compat.v1.global_variables() if
             v.name.split(':')[0] in [x.decode('utf-8') for x in
                                      self.persistent_sess.run(tf.compat.v1.report_uninitialized_variables())]
             ])
        )
        self.persistent_sess.run(
            [self.tensor_peaks, self.tensor_heatMat_up, self.tensor_pafMat_up],
            feed_dict={
                self.tensor_image: [np.ndarray(shape=(target_size[1], target_size[0], 3), dtype=np.float32)],
                self.upsample_size: [target_size[1], target_size[0]]
            }
        )
        self.persistent_sess.run(
            [self.tensor_peaks, self.tensor_heatMat_up, self.tensor_pafMat_up],
            feed_dict={
                self.tensor_image: [np.ndarray(shape=(target_size[1], target_size[0], 3), dtype=np.float32)],
                self.upsample_size: [target_size[1] // 2, target_size[0] // 2]
            }
        )
        self.persistent_sess.run(
            [self.tensor_peaks, self.tensor_heatMat_up, self.tensor_pafMat_up],
            feed_dict={
                self.tensor_image: [np.ndarray(shape=(target_size[1], target_size[0], 3), dtype=np.float32)],
                self.upsample_size: [target_size[1] // 4, target_size[0] // 4]
            }
        )

    def _get_scaled_img(self, npimg, scale):# npimg, None            # 改变为目标尺寸大小
        if npimg.shape[:2] != (self.target_size[1], self.target_size[0]):#target_size = [432,368]
            npimg = cv2.resize(npimg, self.target_size, interpolation=cv2.INTER_CUBIC)
        return npimg

    @staticmethod
    def draw_humans(npimg, humans):  #对于找到Human中已经找到的特征点在图片中进行描点
        image_h, image_w = npimg.shape[:2]
        centers = {}
        for human in humans:
            for i in range(common.CocoPart.Background.value):
                if i not in human.body_parts.keys():
                    continue
                body_part = human.body_parts[i]
                center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
                centers[i] = center
                cv2.circle(npimg, center, 5, common.CocoColors[i], thickness=-1, lineType=8, shift=0)

            for pair_order, pair in enumerate(common.CocoPairsRender):
                if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                    continue
                cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
        return npimg

    def inference(self, npimg, upsample_size=1.0):
        #这一步暂时不知道作用
        upsample_size = [int(self.target_size[1] / 8 * upsample_size), int(self.target_size[0] / 8 * upsample_size)]

        img = self._get_scaled_img(npimg, None)   #改变到目标大小之后的npimg

        #peaks, heatMat_up, pafMat_up识别特征点的重要数据，暂时不知道用法
        peaks, heatMat_up, pafMat_up = self.persistent_sess.run(
            [self.tensor_peaks, self.tensor_heatMat_up, self.tensor_pafMat_up], feed_dict={
                self.tensor_image: [img], self.upsample_size: upsample_size
            })
        peaks = peaks[0]
        self.heatMat = heatMat_up[0]
        self.pafMat = pafMat_up[0]

        #PoseEstimator.estimate_paf函数返回检测到的人体的列表
        #而其中每一个Human对象包括描述他特征点信息的bodypart对象和score
        #每一个bodypart对象由：人体编号-特征点编号-特征点坐标x-特征点坐标y-以及score组成
        humans = PoseEstimator.estimate_paf(peaks, self.heatMat, self.pafMat)

        return humans