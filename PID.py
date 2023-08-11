import cv2 as cv
import numpy as np
import math
from decimal import Decimal


class PID:

    lefti = 0
    righti = 0

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
        self.d = 0

        self.lefti = 0
        self.righti = 0

        self.rsense = 1.1
        self.lsense = 1

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

        return self.get_new_rpms

    @property
    def get_new_rpms(self):

        left_y_dist = self.targets[1] - self.left[1]
        right_y_dist = self.targets[2] - self.right[1]

        if left_y_dist < 0:  # buggy is below
            rsense = max(self.rsense, self.lsense)
            lsense = min(self.rsense, self.lsense)
            self.rsense = rsense
            self.lsense = lsense
        elif left_y_dist > 0:  # buggy is above
            lsense = max(self.rsense, self.lsense)
            rsense = min(self.rsense, self.lsense)
            self.lsense = lsense
            self.rsense = rsense

        leftp = self.p * abs(left_y_dist) * self.lsense
        lefti = self.i * (PID.lefti * 0)
        leftd = self.d * (self.lrpm - self.last_lrpm)
        leftsum = 0 if abs(left_y_dist) < 0.5 else float(leftp) + float(lefti) + float(leftd)
        # leftsum = float(leftp) + float(lefti) + float(leftd)
        self.last_lrpm = self.lrpm

        rightp = self.p * abs(right_y_dist) * self.rsense
        righti = self.i * (PID.righti * 0)
        rightd = self.d * (self.rrpm - self.last_rrpm)
        rightsum = 0 if abs(right_y_dist) < 0.5 else float(rightp) + float(righti) + float(rightd)
        # rightsum = float(rightp) + float(righti) + float(rightd)
        self.last_rrpm = self.rrpm

        print([self.lsense, self.rsense])
        new_left = round(leftsum, 6)
        new_right = round(rightsum, 6)

        return new_left, new_right

    def reset(self):
        self.lefti = 0
        self.righti = 0
