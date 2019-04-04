from turtle import Turtle
import cv2
import numpy as np
import random

IMG_EDGE_LENGTH = 512
TIME_DELAY = 100
TURTLE_SCALE = 0.03


class HilbertCurve:

    def __init__(self, n):
        self.n = n
        self.num_grid_points_edge = 2 ** n
        self.turtle = Turtle(0, self.num_grid_points_edge - 1)
        self.last_corner = self._get_pixel_position_from_turtle()
        self.img = np.zeros((IMG_EDGE_LENGTH, IMG_EDGE_LENGTH, 3), np.uint8)
        self.rand = random.Random()
        turtle_img_0 = cv2.imread('turtle_0.png', cv2.IMREAD_COLOR)
        turtle_img_0 = cv2.resize(turtle_img_0, (0, 0), fx=TURTLE_SCALE, fy=TURTLE_SCALE)
        turtle_img_90 = cv2.imread('turtle_90.png', cv2.IMREAD_COLOR)
        turtle_img_90 = cv2.resize(turtle_img_90, (0, 0), fx=TURTLE_SCALE, fy=TURTLE_SCALE)
        turtle_img_180 = cv2.imread('turtle_180.png', cv2.IMREAD_COLOR)
        turtle_img_180 = cv2.resize(turtle_img_180, (0, 0), fx=TURTLE_SCALE, fy=TURTLE_SCALE)
        turtle_img_270 = cv2.imread('turtle_270.png', cv2.IMREAD_COLOR)
        turtle_img_270 = cv2.resize(turtle_img_270, (0, 0), fx=TURTLE_SCALE, fy=TURTLE_SCALE)
        self.turtle_imgs = {0: turtle_img_0, 90: turtle_img_90, 180: turtle_img_180, 270: turtle_img_270}
        self.turtle_img = turtle_img_0
        self.turtle_img_start = None
        self.before_turtle_img = None
        self.img_num = 0

    def _get_pixel_position_from_turtle(self):
        pixel_per_grid = IMG_EDGE_LENGTH / self.num_grid_points_edge
        return int(pixel_per_grid * self.turtle.x + pixel_per_grid / 2), int(pixel_per_grid * self.turtle.y + pixel_per_grid / 2)

    def _set_before_turtle_image(self):
        height, width, _ = self.turtle_img.shape
        centre_x, centre_y = self._get_pixel_position_from_turtle()
        start_x = centre_x - int(width / 2)
        start_y = centre_y - int(height / 2)
        self.before_turtle_img = self.img[start_y: (start_y + height), start_x: (start_x + width)].copy()
        self.turtle_img_start = [start_x, start_y]

    def remove_turtle_image(self):
        height, width, _ = self.turtle_img.shape
        if self.before_turtle_img is not None:
            # Reset the old image before overlaying the turtle
            self.img[self.turtle_img_start[1]: (self.turtle_img_start[1] + height), self.turtle_img_start[0]: (self.turtle_img_start[0] + width)] = self.before_turtle_img

    def _draw_turtle_image(self):
        self._set_before_turtle_image()
        height, width, _ = self.turtle_img.shape
        centre_x, centre_y = self._get_pixel_position_from_turtle()
        start_x = centre_x - int(width / 2)
        start_y = centre_y - int(height / 2)
        self.img[start_y: (start_y + height), start_x: (start_x + width)] = self.turtle_img

    def _turn(self, direction):
        self.remove_turtle_image()
        self.turtle.turn(direction)
        self.turtle_img = self.turtle_imgs[self.turtle.direction]
        self._draw_turtle_image()
        cv2.imshow('image', self.img)
        self.save_image()
        cv2.waitKey(TIME_DELAY)

    def _move_forward(self, step):
        self.remove_turtle_image()
        self.turtle.move_forward(step)
        new_corner = self._get_pixel_position_from_turtle()
        cv2.line(self.img, self.last_corner, new_corner, (255, 255, 255), 2)
        self.last_corner = new_corner
        self._draw_turtle_image()
        cv2.imshow('image', self.img)
        self.save_image()
        cv2.waitKey(TIME_DELAY)

    def _finish(self):
        # (0, 4) -> 20% chance of finishing
        return self.rand.randint(0, 4) == 0
        #return False

    def _step_size(self, n):
        return 2 ** n - 1

    def start_curve(self):
        self._draw_turtle_image()
        cv2.imshow('image', self.img)
        cv2.waitKey(TIME_DELAY)
        self.hilbert(self.n)

    def hilbert(self, n):
        if n == 0:
            return
        if self._finish():
            step_size = self._step_size(n)
            self._turn(90)
            self._move_forward(step_size)
            self._turn(-90)
            self._move_forward(step_size)
            self._turn(-90)
            self._move_forward(step_size)
            self._turn(90)
        else:
            self._turn(90)
            self.treblih(n - 1)
            self._move_forward(1)
            self._turn(-90)
            self.hilbert(n - 1)
            self._move_forward(1)
            self.hilbert(n - 1)
            self._turn(-90)
            self._move_forward(1)
            self.treblih(n - 1)
            self._turn(90)

    def treblih(self, n):
        if n == 0:
            return
        if self._finish():
            step_size = self._step_size(n)
            self._turn(-90)
            self._move_forward(step_size)
            self._turn(90)
            self._move_forward(step_size)
            self._turn(90)
            self._move_forward(step_size)
            self._turn(-90)
        else:
            self._turn(-90)
            self.hilbert(n - 1)
            self._move_forward(1)
            self._turn(90)
            self.treblih(n - 1)
            self._move_forward(1)
            self.treblih(n - 1)
            self._turn(90)
            self._move_forward(1)
            self.hilbert(n - 1)
            self._turn(-90)

    def close(self):
        cv2.waitKey()
        cv2.imwrite('result_' + str(self.n) + '.png', self.img)
        cv2.destroyAllWindows()

    def save_image(self):
        cv2.imwrite('gif/image' + str(self.img_num) + '.png', self.img)
        self.img_num += 1


if __name__ == "__main__":
    hilbert = HilbertCurve(5)
    hilbert.start_curve()
    hilbert.close()
