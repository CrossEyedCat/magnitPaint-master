import math


class Magnetic_Vector:

    def __init__(self, x, y, length=1, angle=0, color='#000000'):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.color = color

    def draw(self, drawing_area):
        end_x = self.x + self.length * math.cos(self.angle)
        end_y = self.y + self.length * math.sin(self.angle)
        drawing_area.create_line(self.x, self.y, end_x,
                                 end_y, fill=self.color)
        ug = self.angle + math.pi * 1.25
        ug2 = ug - math.pi / 2
        drawing_area.create_line(end_x,
                                 end_y,
                                 end_x + self.length / 3 * math.cos(ug),
                                 end_y + self.length * math.sin(ug),
                                 fill=self.color)
        drawing_area.create_line(end_x,
                                 end_y,
                                 end_x + self.length / 3 * math.cos(ug2),
                                 end_y + self.length * math.sin(ug2),
                                 fill=self.color)

    def get_X(self):
        return self.x

    def get_Y(self):
        return self.y

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length

    def get_angle(self):
        return self.angle

    def set_angle(self, ang):
        self.angle = ang

    def set_color(self, color):
        self.color = color