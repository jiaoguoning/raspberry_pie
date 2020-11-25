from enum import Enum
import cv2

class CocoPart(Enum):
    Nose = 0#鼻子
    Neck = 1#脖子
    RShoulder = 2#右肩
    RElbow = 3#右肘
    RWrist = 4#右手腕
    LShoulder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8#右臀部
    RKnee = 9#右膝盖
    RAnkle = 10#右踝
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14#右眼
    LEye = 15
    REar = 16#右耳
    LEar = 17
    Background = 18#背景

CocoPairs = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8), (8, 9), (9, 10), (1, 11),
    (11, 12), (12, 13), (1, 0), (0, 14), (14, 16), (0, 15), (15, 17), (2, 16), (5, 17)
]   # = 19
CocoPairsRender = CocoPairs[:-2]
# CocoPairsNetwork = [
#     (12, 13), (20, 21), (14, 15), (16, 17), (22, 23), (24, 25), (0, 1), (2, 3), (4, 5),
#     (6, 7), (8, 9), (10, 11), (28, 29), (30, 31), (34, 35), (32, 33), (36, 37), (18, 19), (26, 27)
#  ]  # = 19

CocoColors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
              [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
              [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

def read_imgfile(path,width=None,height=None):
    val_image = cv2.imread(path,cv2.IMREAD_COLOR)
    if width is not None and height is not None:
        val_image = cv2.resize(val_image,(width,height))
    return val_image
