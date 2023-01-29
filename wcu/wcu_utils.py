PORT_RTV_SOCKET = 2005
PORT_DATA_SOCKET = 2001
ROBOT_HOSTNAME = 'rloader'
DEFAULT_BUFFER_SIZE = 1024  # 1 KB per buffer
FRAME_BUFFER_SIZE = 128 * 1024  # 128 KB per buffer


class RobotError(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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


class Status:

    CONNECTED = 1
    NOT_CONNECTED = 0

class GuiColors:
    RED = "#F0391B"
    BLUE = "#2C73D9"
    GREEN = "#0B9600"
    BLACK = "#000000"

class GuiTexts:
    """ Commands text to be displayed in the GUI """
    IDLE = 'Waiting for commands...'
    DRIVING_FORWARD = 'Driving Forward...'
    DRIVING_BACKWARD = 'Driving Backward...'
    TURNING_RIGHT = 'Turning Right...'
    TURNING_LEFT = 'Turning Left...'
    ACTIVATING_BRAKES = 'Activating Brakes...'
    NOT_CONNECTED = "Not Connected to Robot.\nPress 'Connect to Robot' button below to connect"
    CONNECTING = 'Connecting...'
    CONNECTED = 'Connected'
    CONNECT = "Connect to Robot"
    DISCONNECT = "Disconnect from Robot"
    RECONNECT = "Reconnect to Robot"
    REQUESTING_STREAM = 'Realtime Video Stream requested'
    CONTROL_MODE_AUTO = 'Changed to Automatic Control'
    CONTROL_MODE_MANUAL = 'Changed to Manual Control'
    REACHED_MAX_SPEED = 'Reached Maximum Speed'
    REACHED_MIN_SPEED = 'Reached Minimum Speed'
    REACHED_HARD_RIGHT = 'Reached Hard Right'
    REACHED_HARD_LEFT = 'Reached Hard Left'
    LFA_MODE_ENABLED = 'Automatic LF Control Is Enabled'
    SWITCH_TO_LFA_MODE = 'Switch to LFA control mode'
    SWITCH_TO_MANUAL_MODE = 'Switch to Manual control mode'
    START_STREAM = 'Start Robot Stream'
    STOP_STREAM = 'Stop Robot Stream'
    START_RECORDING_STREAM = 'Record Stream'
    STOP_RECORDING_STREAM = 'Stop Recording'
    REQUESTING_STREAM = 'Requesting Robot Stream...'
    FAILED_TO_CONNECT = 'Failed to connect to Robot'
