class Turtle:

    def __init__(self, x_start, y_start):
        self.x = x_start
        self.y = y_start
        self.direction = 0
        self.line_segments = []

    def move_forward(self, step):
        if self.direction == 0:
            self.y -= step
        elif self.direction == 90:
            self.x += step
        elif self.direction == 180:
            self.y += step
        elif self.direction == 270:
            self.x -= step
        else:
            raise ValueError('Invalid direction argument')

    def turn(self, direction):
        if direction % 90 != 0:
            raise ValueError('Invalid direction argument')
        else:
            self.direction = (self.direction + direction) % 360