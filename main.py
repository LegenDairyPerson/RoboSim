import cv2 as cv
import numpy as np
from buggy import Buggy
from decimal import Decimal
from PID import PID

blank = np.zeros([700, 700, 3], dtype="uint8")

_RED = (0, 0, 255)
_WHITE = (255, 255, 255)
_BLUE = (255, 0, 0)
_GREEN = (0, 255, 0)

last_mouse_y = 100
l_target = 100
r_target = 100

targets = [last_mouse_y, l_target, r_target]


def check_for_key(key):
    global lrpm, rrpm
    if key == ord("q"):
        return -1
    elif key == ord("r"):
        lrpm = 0
        rrpm = 0
        Car.reset(blank)
        PID.reset()
    elif key == ord("w"):
        lrpm += Decimal("0.01")
        rrpm += Decimal("0.01")
    elif key == ord("a"):
        rrpm += Decimal("0.01")
    elif key == ord("s"):
        lrpm -= Decimal("0.01")
        rrpm -= Decimal("0.01")
    elif key == ord("d"):
        lrpm += Decimal("0.01")


def check_for_key2(key):
    if key == ord("q"):
        return -1
    if key == ord("w"):
        Car.move_straight(1, 1)
    elif key == ord("a"):
        Car.move_right_wheel(1)
    elif key == ord("s"):
        Car.move_straight(-1)
    elif key == ord("d"):
        Car.move_left_wheel(1)


def updateScreen():
    global blank, last_mouse_y, l_target, r_target
    blank = np.zeros([700, 700, 3], dtype="uint8")
    blank = cv.line(blank, (0, last_mouse_y), (700, last_mouse_y), _RED)
    blank = cv.line(blank, (0, l_target), (700, l_target), _WHITE)
    blank = cv.line(blank, (0, r_target), (700, r_target), _GREEN)

    Car.draw_buggy(blank)
    blank = cv.putText(blank, f"LRPM = {lrpm}, RRPM = {rrpm}", (25, 25), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255))
    print("ATTEMPT COMPLETE\n\n\n")


def draw_mouse_line(event, x, y, flags, params):
    global blank, last_mouse_y, l_target, r_target, targets

    if event == cv.EVENT_MOUSEMOVE:
        # print("lkajsdlkas")
        # print(y)
        last_mouse_y = y
        l_target = int(last_mouse_y - 20) #Car.dist//2)
        r_target = int(last_mouse_y + 20) #Car.dist//2)
        targets = [last_mouse_y, l_target, r_target]
        print(targets)

cv.namedWindow(winname="named_window")
cv.setMouseCallback("named_window", draw_mouse_line)

lrpm = 0
rrpm = 0

Car = Buggy(blank)
PID = PID(lrpm, rrpm, targets, Car)


while True:
    cv.imshow("named_window", blank)

    Car.move_straight(float(lrpm), float(rrpm))
    lrpm, rrpm = PID.update(lrpm, rrpm, targets, Car)
    updateScreen()
    if check_for_key(cv.waitKey(1) & 0xff) == -1:
        break

cv.destroyAllWindows()
