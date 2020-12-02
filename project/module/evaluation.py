import numpy as np
import math


def cal_line(point1, point2):
    """计算两点之间的距离"""
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    rebase = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return rebase


def cal_alpha(long, point1, point2):
    b = point2[0] - point1[0]
    alpha = b / long
    return alpha


class same_vector:
    def __init__(self, rshouder, point2):
        self.a = rshouder
        self.b = point2
        self.l = cal_line(self.a, self.b)
        self.alpha = cal_alpha(self.l, self.a, self.b)
        self.point = 0

    def __mul__(self, other):
        return self.l * other

    def like_equal(self, other_vector, angle, long):
        answer = False
        angle = math.cos(angle)
        dif_angle = other_vector.alpha - self.alpha
        dif_long = other_vector.l - self.l
        if -angle <= dif_angle <= angle:
            answer = True
            if -long <= dif_long <= long:
                answer = True
            else:
                answer = False
        return answer


def add_vector(back_points):
    vector_sets = []
    for x in back_points:
        h = []
        rs = x[0][2]
        for i in [x for x in range(19) if x != 2]:
            vector = same_vector(rs, x[0][i])
            vector.point = i
            h.append(vector)
        vector_sets.append(h)
    return vector_sets


class human_vector:
    def __init__(self, back_points):
        self.vector_sets = add_vector(back_points)
        self.human1 = self.vector_sets[0]
        self.human2 = self.vector_sets[1]

    def compare_forward(self):
        for i, j in zip(self.human1, self.human2):
            if i.like_equal(j, 30, 10):
                continue
            else:
                if i.b[0] != 0 and i.b[1] != 0:
                    print(i.point)
                    print(i.b)
        return