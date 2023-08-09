import cv2 as cv
import numpy as np
import math

_RPM_SENSE = 10


class Buggy:

    def __init__(self, window, ix=100, iy=600):

        self.wl = [ix, iy - 20]  # left wheel
        self.wr = [ix, iy + 20]  # right wheel
        self.midpoint = None  # initialize midpoint, calc later
        self.wm = self.find_middle_wheel()  # middle wheel
        self.t1, self.t2 = self.wr  # debug vars for right vector
        self.dist = math.dist(self.wl, self.wr)

        self.roundedLeft = (round(self.wl[0]), round(self.wl[1]))
        self.roundedRight = (round(self.wr[0]), round(self.wr[1]))
        self.roundedMiddle = (round(self.wm[0]), round(self.wm[1]))
        self.roundedMidpoint = None
        self.roundedT1 = round(self.t1)
        self.roundedT2 = round(self.t2)
        self.roundedDist = round(self.dist)

        self.right_vector_angle = None  # initialize right vector, calc later
        self.vector_angle = None  # initialize main vector, calc later
        self.draw_buggy(window)  # draw with initial vals

    def find_middle_wheel(self, update=False):
        pwl = self.wl
        pwr = self.wr
        self.dist = math.dist(self.wl, self.wr)
        self.roundedDist = round(self.dist)
        _MAGNITUDE = self.dist / 2 * math.tan(math.radians(60))

        dx = pwl[0] - pwr[0]
        dy = pwl[1] - pwr[1]
        # print(f"Dx: {dx}, Dy: {dy}")

        self.midpoint = ((pwl[0] + pwr[0]) / 2, (pwl[1] + pwr[1]) / 2)
        # print(f"Midpoint: {midpoint}")

        # cv.circle(window, midpoint, 5, (0, 0, 255), thickness=-1)
        # cv.line(window, midpoint, (400, midpoint[1]), (0, 0, 255))

        try:
            if (dx > 0 and dy > 0) or (dx > 0 > dy):
                # print("NEW CASE")
                self.vector_angle = math.radians(360 - (math.degrees(math.atan(dy / dx)) + 90))
            else:
                self.vector_angle = math.radians(180 - (math.degrees(math.atan(dy / dx)) + 90))
            # print(f"Vector Angle 2: {180 - (math.degrees(math.atan(dy / dx)) + 90)}")
            # print(f"(math.degrees(math.atan(dy/dx)): {(math.degrees(math.atan(dy / dx)) + 90)}")

        except ZeroDivisionError:
            if self.wl[1] < self.wr[1]:
                self.vector_angle = math.radians(180 - 90 - 90)
            else:
                self.vector_angle = math.radians(360 - 90 - 90)

        deltx = _MAGNITUDE * math.cos(self.vector_angle)
        delty = _MAGNITUDE * math.sin(self.vector_angle)

        if not update:
            pass
            # print(f"math.cos(vector_angle): {math.cos(self.vector_angle)}")
            # print(f"Delta X: {deltx}, Delta Y: {delty}")
            # print("Vector Angle: " + f"{math.degrees(self.vector_angle)}")

        return [self.midpoint[0] + deltx, self.midpoint[1] - delty]

    def draw_buggy(self, window, update=False):

        if self.dist < 40:
            pass
            # print(f"Alert! Dist = {math.dist(self.wl, self.wr)}")

        self.wm = self.find_middle_wheel(update=update)

        self.roundedLeft = (round(self.wl[0]), round(self.wl[1]))
        self.roundedRight = (round(self.wr[0]), round(self.wr[1]))
        self.roundedMiddle = (round(self.wm[0]), round(self.wm[1]))
        self.roundedMidpoint = (round(self.midpoint[0]), round(self.midpoint[1]))
        self.roundedT1 = round(self.t1)
        self.roundedT2 = round(self.t2)

        triangle_contours = np.array([self.roundedLeft, self.roundedRight, self.roundedMiddle])
        cv.drawContours(window, [triangle_contours], 0, (0, 0, 255), -1)
        cv.line(window, self.roundedMidpoint, self.roundedMiddle, (255, 255, 255))

        cv.circle(window, self.roundedLeft, 5, (255, 255, 255), thickness=-1)
        cv.circle(window, self.roundedMiddle, 5, (255, 255, 255), thickness=-1)
        cv.circle(window, self.roundedRight, 5, (255, 0, 0), thickness=-1)

        cv.line(window, self.roundedLeft, (self.roundedRight[0], self.roundedLeft[1]), (255, 255, 255))
        cv.line(window, self.roundedRight, (self.roundedRight[0], self.roundedLeft[1]), (255, 255, 255))
        cv.line(window, (self.roundedLeft[0], self.roundedMidpoint[1]), (self.roundedRight[0], self.roundedMidpoint[1]),
                (255, 255, 255))
        cv.line(window, (self.roundedT1, self.roundedT2), self.roundedRight, (255, 255, 255))

        if not update:
            pass
            # print(f"Left x, Left y: ({roundedLeft[0]}, {roundedLeft[1]})")
            # print(f"Right x, Right y: ({roundedRight[0]}, {roundedRight[1]})")

    def move_right_wheel(self, right_rpm=1):

        a = math.dist(self.wl, self.wr)  # leg distance
        b = _RPM_SENSE * right_rpm  # vector magnitude// px per function call

        c = math.degrees(math.acos((a ** 2 + a ** 2 - b ** 2) / (2 * a * a)))  # side c angle; Isosceles triangle math

        # Since it's an isosceles triangle, angles A and B are equal
        ins_angle = (180 - c) / 2

        # nex vector angle: 75.52248781407008 mag = 10 <-- debug constants
        dx = self.wl[0] - self.wr[0]
        dy = self.wl[1] - self.wr[1]
        try:
            if (dx > 0 and dy > 0) or (dx > 0 > dy):  # catches quad 3 and 4 ? I think
                self.right_vector_angle = math.radians(360 - (math.degrees(math.atan(dy / dx)) + ins_angle))
            else:  # quad 1 and 2 angles
                self.right_vector_angle = math.radians(180 - (math.degrees(math.atan(dy / dx)) + ins_angle))
            # print("RightVector: " + f"{math.degrees(self.right_vector_angle)}")
        except ZeroDivisionError:  # catches error when dx = 0
            if self.wl[1] < self.wr[1]:  # if the left wheel is above the right
                self.right_vector_angle = math.radians(180 - 90 - ins_angle)
            else:  # if the right wheel is above the left
                self.right_vector_angle = math.radians(360 - 90 - ins_angle)
            # print("RightVector: " + f"{math.degrees(self.right_vector_angle)}")

        # trig functions using vector angle and magnitude b to identify offset
        right_deltx = b * math.cos(self.right_vector_angle)
        right_delty = b * math.sin(self.right_vector_angle)

        # print(f"Right Delta X: {right_deltx}, Right Delta Y: {right_delty}")
        # creates temp last positions to draw white debug line
        self.t1 = self.wr[0]
        self.t2 = self.wr[1]

        # updates wheel position
        self.wr[0] += right_deltx
        self.wr[1] -= right_delty

        # check to prevent size loss
        # a = math.dist(self.wl, self.wr)
        # if a < 40:
        #     while a < 40:
        #         a = math.dist(self.wl, self.wr)
        #         if right_deltx < 0:
        #             self.wr[0] -= 1
        #         else:
        #             self.wr[0] += 1
        #         if right_delty < 0:
        #             self.wr[1] += 1
        #         else:
        #             self.wr[1] -= 1

    def move_left_wheel(self, left_rpm=1):

        a = math.dist(self.wl, self.wr)
        b = _RPM_SENSE * left_rpm

        c = math.degrees(math.acos((a ** 2 + a ** 2 - b ** 2) / (2 * a * a)))

        # Since it's an isosceles triangle, angles A and B are equal
        ins_angle = (180 - c) / 2

        # angle math
        left_deltx = b * math.cos(self.vector_angle - math.radians(90 - ins_angle))
        left_delty = b * math.sin(self.vector_angle - math.radians(90 - ins_angle))
        # print(f"Left_deltx, Left_delty: ({left_deltx}, {left_delty})")
        # print(f"Vector Angle: First Checkpoint: {math.degrees(self.vector_angle)}")

        # print([self.wl, self.wr, self.wm])
        self.wl[0] += left_deltx
        self.wl[1] -= left_delty

        # maintain size
        # a = math.dist(self.wl, self.wr)
        # if a < 40:
        #     while a < 40:
        #         a = math.dist(self.wl, self.wr)
        #         print("Correction Made")
        #         print(f"{a}")
        #         if left_deltx < 0:
        #             self.wl[0] -= 1
        #         else:
        #             self.wl[0] += 1
        #         if left_delty < 0:
        #             self.wl[1] += 1
        #         else:
        #             self.wl[1] -= 1

    def move_straight(self, left_rpm=1, right_rpm=1):

        if self.vector_angle == math.radians(90):
            if left_rpm > right_rpm:
                self.move_left_wheel(left_rpm)
            else:
                # print("!!!!!!!!!!!!!!!!!!!!\n")
                # print("!!!!!!!!!!!!!!!!!!!!\n")
                # print("!!!!!!!!!!!!!!!!!!!!\n")
                # print("!!!!!!!!!!!!!!!!!!!!\n")
                self.move_right_wheel(right_rpm)
            return

        right_deltx = _RPM_SENSE * right_rpm * math.cos(self.vector_angle)
        right_delty = _RPM_SENSE * right_rpm * math.sin(self.vector_angle)
        # print(f"Right Delta X: {right_deltx}, Right Delta Y: {right_delty}")

        # print([self.wl, self.wr, self.wm])
        self.wr[0] += right_deltx
        self.wr[1] -= right_delty

        left_deltx = _RPM_SENSE * left_rpm * math.cos(self.vector_angle)
        left_delty = _RPM_SENSE * left_rpm * math.sin(self.vector_angle)
        # print(f"Left Delta X: {left_deltx}, Left Delta Y: {left_delty}")

        # print([self.wl, self.wr, self.wm])
        self.wl[0] += left_deltx
        self.wl[1] -= left_delty

    def reset(self, window, ix=100, iy=600):

        self.wl = [ix, iy - 20]  # left wheel
        self.wr = [ix, iy + 20]  # right wheel
        self.midpoint = None  # initialize midpoint, calc later
        self.wm = self.find_middle_wheel()  # middle wheel
        self.t1, self.t2 = self.wr  # debug vars for right vector
        self.dist = math.dist(self.wl, self.wr)

        self.roundedLeft = (round(self.wl[0]), round(self.wl[1]))
        self.roundedRight = (round(self.wr[0]), round(self.wr[1]))
        self.roundedMiddle = (round(self.wm[0]), round(self.wm[1]))
        self.roundedMidpoint = None
        self.roundedT1 = round(self.t1)
        self.roundedT2 = round(self.t2)
        self.roundedDist = round(self.dist)

        self.right_vector_angle = None  # initialize right vector, calc later
        self.vector_angle = None  # initialize main vector, calc later
        self.draw_buggy(window)  # draw with initial vals

    # def move_both_wheels(self, left_rpm, right_rpm):
    #     self.move_left_wheel(left_rpm)
    #     self.move_right_wheel(right_rpm)
