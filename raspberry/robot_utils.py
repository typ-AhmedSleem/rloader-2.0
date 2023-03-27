import json as JSON

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

    def __init__(self, data) -> None:
        self.data = data

    @property
    def signal(self) -> str:
        return self.data.get('signal', None)

    @property
    def cmd(self) -> str:
        return self.data.get('cmd', None)

    @property
    def is_arm_cmd(self) -> bool:
        return ('arm' in self.data) and ('jid' in self.data) and ('ag' in self.data)

    @property
    def arm_mv_spec(self):
        return self.data.get('jid', None), self.data.get('ag', None)

    def __repr__(self):
        return f"DataModel({self.data})"


def cvt_json2model(raw_json):
    try:
        if raw_json is None or len(raw_json) == 0:
            raw_json = ""
        return DataModel(JSON.loads(raw_json))
    except JSON.JSONDecodeError:
        return DataModel({})
