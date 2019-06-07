from FaceDetector import FaceDetector
from BotDraw import BotDraw


def best_callback():
    pass


# BCM
pen_pin = 15
control_pins1 = (6, 13, 19, 26)
control_pins2 = (12, 16, 20, 21)

bot = BotDraw((control_pins1, control_pins2), pen_pin, best_callback)
face_detector = FaceDetector()
bot.draw(face_detector.get_face_contour_lines())
