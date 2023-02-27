from PyQt5 import QtCore
from logger import Logger


class CarDriverCallback:

    def on_drive_forward(self):
        pass

    def on_drive_backward(self):
        pass

    def on_steer_right(self):
        pass

    def on_steer_left(self):
        pass

    def on_stop(self):
        pass


class CarManualDriver:

    def __init__(self, callback: CarDriverCallback) -> None:
        self.logger = Logger("CarManualDriver")
        self.callback = callback

    def decide(self, key_pressed):
        if key_pressed in (QtCore.Qt.Key.Key_W, QtCore.Qt.Key.Key_Up):
            self.callback.on_drive_forward()
        elif key_pressed in (QtCore.Qt.Key.Key_S, QtCore.Qt.Key.Key_Down):
            self.callback.on_drive_backward()
        elif key_pressed in (QtCore.Qt.Key.Key_D, QtCore.Qt.Key.Key_Right):
            self.callback.on_steer_right()
        elif key_pressed in (QtCore.Qt.Key.Key_A, QtCore.Qt.Key.Key_Left):
            self.callback.on_steer_left()
        elif key_pressed == QtCore.Qt.Key.Key_Space:
            self.callback.on_stop()
