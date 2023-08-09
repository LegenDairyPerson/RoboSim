import cv2 as cv
import numpy as np
import math
from decimal import Decimal


class PID:

    def __init__(self, lrpm, rrpm, targets, car):
        self.left = car.roundedLeft
        self.right = car.roundedRight
        self.vector_angle = car.vector_angle
        self.lrpm = lrpm
        self.rrpm = rrpm
        self.targets = targets

        self.last_lrpm = self.lrpm
        self.last_rrpm = self.rrpm

        self.p = 0.01
        self.i = 0
        self.d = 0.5

        self.lefti = 0
        self.righti = 0

    def update(self, lrpm, rrpm, targets, car=None):
        if car is None:
            return
        else:
            self.left = car.wl
            self.right = car.wr
            self.vector_angle = car.vector_angle

        self.lrpm = lrpm
        self.rrpm = rrpm
        self.targets = targets

        return self.get_new_rpms()

    def get_new_rpms(self):

        left_y_dist = abs(self.targets[1] - self.left[1])
        right_y_dist = abs(self.targets[2] - self.right[1])

        leftp = self.p * left_y_dist
        lefti = self.i * 0
        leftd = self.d * (self.lrpm - self.last_lrpm)
        leftsum = float(leftp) + float(lefti) + float(leftd)
        self.last_lrpm = self.lrpm

        rightp = self.p * right_y_dist * 2
        righti = self.i * 0
        rightd = self.d * (self.rrpm - self.last_rrpm)
        rightsum = float(rightp) + float(righti) + float(rightd)
        self.last_rrpm = self.rrpm

        new_left = round(leftsum, 6)
        new_right = round(rightsum, 6)

        return new_left, new_right

    def reset(self):
        self.lefti = 0
        self.righti = 0
