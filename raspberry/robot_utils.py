import json as JSON
from typing import Any


DEFAULT_BUFFER_SIZE = 1024  # 1 KB per buffer
FRAME_BUFFER_SIZE = 128 * 1024  # 128 KB per buffer
PORT_DATA_SOCKET = 2001
PORT_RTV_SOCKET = 2005


class Signals:
    """ Signals that used by WCU and Robot to control everything in-between"""
    SIGNAL_START_STREAM = 'SS'
    SIGNAL_CLOSE_STREAM = 'CS'
    SIGNAL_SWITCH_CONTROL_MODE = 'SCM'
    SIGNAL_DISCONNECT = 'BYE'
    SIGNAL_ACK = 'ACK'


class Directions:
    """ Control commands used to drive the robot """
    CMD_DRIVE_FORWARD = 'df'
    CMD_DRIVE_BACKWARD = 'db'
    CMD_ROTATE_RIGHT = 'rr'
    CMD_ROTATE_LEFT = 'rl'
    CMD_STOP = 'pb'


class ControlModes:
    CONTROL_MODE_MANUAL = 'mcm'
    CONTROL_MODE_AUTOMATIC = 'acm'


class DataModel:

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @property
    def signal(self) -> str:
        return self.data.get('signal', None)

    @property
    def cmd(self) -> str:
        return self.data.get('cmd', None)

    def __repr__(self):
        return f"DataModel({self.data})"

def convertJsonToModel(raw_json):
    try:
        if raw_json is None or len(raw_json) ==0:
            raw_json = ""
        return DataModel(JSON.loads(raw_json))
    except JSON.JSONDecodeError:
        return DataModel({})
