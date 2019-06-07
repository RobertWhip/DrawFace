import time
import math
import threading


class StepperMotor:
    def __init__(self, motor_pins, on_motor_stop_callback):
        self.init_motors(motor_pins)

        self.__threads = []
        self.__motor_pins = motor_pins
        self.on_motor_stop_callback = on_motor_stop_callback
        self.__MIN_TIME = 0.002
        self.__STEP_SEQUENCE = (
            (1, 0, 0, 0),
            (1, 1, 0, 0),
            (0, 1, 0, 0),
            (0, 1, 1, 0),

            (0, 0, 1, 0),
            (0, 0, 1, 1),
            (0, 0, 0, 1),
            (1, 0, 0, 1)
        )

    def rotate(self, angles):
        self.__threads = []
        max_angle = max(map(math.fabs, angles))
        for i in range(len(angles)):
            angle = angles[i]
            if angle == 0:
                continue
            if angle > 0:
                direction = self.__step_forward
            else:
                direction = self.__step_backward
            steps = int(math.fabs(512 * (angle / 360)))
            delay = math.fabs(max_angle * self.__MIN_TIME / angle)
            self.__threads.append(threading.Thread(target=self.__start_rotation, args=(steps, direction, delay, i,)))

        for thread in self.__threads:
            thread.start()
        for thread in self.__threads:
            thread.join()
        self.on_motor_stop_callback()

    def init_motors(self, motor_pins):
        # GPIO.setmode(GPIO.BCM)
        for pins in motor_pins:
            a = 5
            # GPIO.setup(pins, GPIO.OUT)

    def cleanup(self):
        pass
        # GPIO.cleanup()

    def __del__(self):
        pass
        # GPIO.cleanup()

    def __start_rotation(self, steps, direction, delay, index):
        print(self.__motor_pins[index])
        for i in range(steps):
            direction(self.__motor_pins[index], delay)

    def __step_forward(self, stepper_pins, delay_time):
        for row in self.__STEP_SEQUENCE:
            #GPIO.output(stepper_pins, row)
            time.sleep(delay_time)

    def __step_backward(self, stepper_pins, delay_time):
        for row in reversed(self.__STEP_SEQUENCE):
            #GPIO.output(stepper_pins, row)
            time.sleep(delay_time)


# TEST CODE
if __name__ == "__main__":
    control_pins1 = (12, 16, 20, 21)
    control_pins2 = (6, 13, 19, 26)
    motors = StepperMotor((control_pins1, control_pins2))
    try:
        motors.rotate((720, -720))
    except KeyboardInterrupt:
        b=2
        #GPIO.cleanup()
