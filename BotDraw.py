import math
import StepperMotor
import time


class BotDraw:
    def __init__(self, motor_pins, pen_pin, best_callback):
        self.__PEN_PIN = pen_pin
        self.__pi = pigpio.pi()
        self.__pi.set_mode(self.__PEN_PIN, pigpio.OUTPUT)
        self.__x = 0
        self.__y = 0
        self.__one_step_x = 1
        self.__one_step_y = 1
        self.__cam_width = 640
        self.__cam_height = 480
        self.__paper_width = 210
        self.__paper_height = 297
        self.__width_scale = self.__paper_height / self.__cam_height
        self.__height_scale = self.__paper_width / self.__cam_width
        self.__scale = min(self.__paper_height / self.__cam_height, self.__paper_width / self.__cam_width)
        self.__motors = StepperMotor.StepperMotor(motor_pins, best_callback)

    def cleanup(self):
        self.__motors.cleanup()
        self.__pi.set_servo_pulsewidth(self.__PEN_PIN, 0)

    def put_pen_up(self, up):
        print("up" if up else "down")
        self.__pi.set_servo_pulsewidth(self.__PEN_PIN, 2000) if up else self.__pi.set_servo_pulsewidth(self.__PEN_PIN, 500)
        # put pen up if 'up' equals to True
        # put pen down if 'up' equals to False

    def goto(self, x_, y_):
        print("moving to ", (x_, y_), "...", sep="")
        x = x_*self.__scale * (1215 / 640)
        y = y_*self.__scale * (1600 / 480)
        old_x = self.__x
        old_y = self.__y
        self.__x = x
        self.__y = y
        self.__motors.rotate(((old_x - x / self.__one_step_x), (-1) * (old_y - y) / self.__one_step_y))

    def draw_line(self,array_of_points):
        for point in array_of_points:
            self.goto(point[0], point[1])

    def draw(self, points):
        for array_of_points in points:
            self.put_pen_up(True)
            time.sleep(0.5)
            self.goto(array_of_points[0][0], array_of_points[0][1])
            time.sleep(1)
            self.put_pen_up(False)
            time.sleep(0.5)
            self.draw_line(array_of_points)


def best_callback():
    print("Done!")


# TEST CODE
if __name__ == "__main__":
    bot = None
    control_pins1 = (6, 13, 19, 26)
    control_pins2 = (12, 16, 20, 21)
    bot = BotDraw((control_pins1, control_pins2), 26, best_callback)
    bot.draw(([(320, 240),(0, 0),(320, 240),(0, 0),],
                  [(320, 240), (0, 0), (320, 240)],
                  [(320, 240), (0, 0), (320, 240)]))
