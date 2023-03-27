import os
import sys
from PIL import Image
from logger import Logger
from datetime import datetime
from json import dumps as data2json
from PyQt5 import QtGui, QtWidgets, QtCore
from stream import StreamViewer, StreamViewerCallback
from car_driver import CarManualDriver, CarDriverCallback
from connection import ConnectionService, ConnectionCallback
from arm_controller import ArmControllerWindow, Operation as Opts
from utils import Status, GuiColors, GuiTexts as Texts, Directions


class MainWindow(QtWidgets.QMainWindow, ConnectionCallback, CarDriverCallback, StreamViewerCallback):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # GUI necessaries
        self.MARGIN_SIZE = 15
        self.BUTTON_HEIGHT = 100
        self.SCREEN_W = self.screen().size().width()
        self.SCREEN_H = self.screen().size().height()
        self.WINDOW_SIZE = QtCore.QSize(self.SCREEN_W, self.SCREEN_H)
        # Setup root and container
        root = QtWidgets.QWidget(self)
        root.setFixedSize(self.WINDOW_SIZE)
        # INFO: Setup (RTV & Status) container
        self.rtvStatusContainer = QtWidgets.QWidget(root)
        self.rtvStatusContainer.setGeometry(0, 0, self.WINDOW_SIZE.width() // 2,
                                            self.WINDOW_SIZE.height() - self.MARGIN_SIZE)
        # Realtime Video stream ImageView
        self.imgRTV = QtWidgets.QLabel(self.rtvStatusContainer)
        self.imgRTV.setScaledContents(True)
        self.imgRTV.setMinimumSize(900, 600)
        self.imgRTV.setMaximumSize(900, 600)
        self.imgRTV.setGeometry(self.MARGIN_SIZE, self.MARGIN_SIZE, 900, 600)
        # Robot current speed label
        self._lblLogList = QtWidgets.QLabel(self.rtvStatusContainer)
        self._lblLogList.setText("WCU Log")
        self._lblLogList.setFont(QtGui.QFont("monospace", 15))
        self._lblLogList.setGeometry(
            self.MARGIN_SIZE,
            self.imgRTV.height() + self.MARGIN_SIZE,
            self.imgRTV.width(), 50)
        # WCU log ListView
        self.listLog = QtWidgets.QListWidget(self.rtvStatusContainer)
        self.listLog.setSpacing(1)
        self.listLog.setFixedWidth(900)
        self.listLog.setStyleSheet("color: #052BF3;")
        self.listLog.setSelectionRectVisible(False)
        self.listLog.setSelectionMode(QtWidgets.QListView.SelectionMode.NoSelection)
        self.listLog.setGeometry(
            self.MARGIN_SIZE,
            self._lblLogList.geometry().bottom(),
            self.imgRTV.width(),
            self.WINDOW_SIZE.height() - self._lblLogList.geometry().bottom() + 1 - 2 * self.MARGIN_SIZE)
        # INFO: Speed container
        # Calculate X coordinate for speed container
        targetXCoord = self.rtvStatusContainer.width() - self.MARGIN_SIZE
        targetWidth = self.WINDOW_SIZE.width() - targetXCoord - 1 * self.MARGIN_SIZE
        self.speedContainer = QtWidgets.QWidget(root)
        self.speedContainer.setGeometry(targetXCoord, 0, targetWidth, self.WINDOW_SIZE.height() - self.MARGIN_SIZE)
        # Calculate X coordinate for its children
        targetXCoord = self.MARGIN_SIZE
        targetWidth = self.speedContainer.width() - 1 * self.MARGIN_SIZE
        # Control commands label
        self._lblTitle = QtWidgets.QLabel(self.speedContainer)
        self._lblTitle.setMaximumHeight(100)
        self._lblTitle.setMinimumHeight(50)
        self._lblTitle.setFixedSize(targetWidth, 100)
        self._lblTitle.setText("Robot Wireless Control Unit (WCU v2.0)")
        # self._lblCommands.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self._lblTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._lblTitle.setFont(QtGui.QFont("monospace", 20, weight=QtGui.QFont.Weight.Bold))
        self._lblTitle.setGeometry(0, self.MARGIN_SIZE, targetWidth, 100)
        # Exit button
        self.btnQuit = QtWidgets.QPushButton(self.speedContainer)
        self.btnQuit.setText("Exit WCU")
        self.btnQuit.setMaximumHeight(100)
        self.btnQuit.setMinimumHeight(100)
        self.btnQuit.clicked.connect(self.close)
        self.btnQuit.setFont(QtGui.QFont("monospace", 15))
        self.btnQuit.setGeometry(0, self.listLog.geometry().bottom() - self.BUTTON_HEIGHT, targetWidth,
                                 self.BUTTON_HEIGHT)
        # Arm Controller button
        self.btnArmController = QtWidgets.QPushButton(self.speedContainer)
        self.btnArmController.setMaximumHeight(100)
        self.btnArmController.setMinimumHeight(100)
        self.btnArmController.setText("Arm Controller")
        self.btnArmController.clicked.connect(self.show_arm_controller)
        self.btnArmController.setFont(QtGui.QFont("monospace", 15))
        self.btnArmController.setGeometry(0, self.btnQuit.geometry().top() - (self.BUTTON_HEIGHT + self.MARGIN_SIZE),
                                          targetWidth, self.BUTTON_HEIGHT)
        # Change control mode button
        self.btnSwitchControlMode = QtWidgets.QPushButton(self.speedContainer)
        self.btnSwitchControlMode.setMaximumHeight(100)
        self.btnSwitchControlMode.setMinimumHeight(100)
        self.btnSwitchControlMode.setText("Switch Control Mode")
        self.btnSwitchControlMode.setFont(QtGui.QFont("monospace", 15))
        self.btnSwitchControlMode.clicked.connect(self.switch_control_mode)
        self.btnSwitchControlMode.setGeometry(0, self.btnArmController.geometry().top() - (
            self.BUTTON_HEIGHT + self.MARGIN_SIZE), targetWidth, self.BUTTON_HEIGHT)
        # Start/Stop Recording button
        self.btnRecordStream = QtWidgets.QPushButton(self.speedContainer)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.btnRecordStream.setMaximumHeight(100)
        self.btnRecordStream.setMinimumHeight(100)
        self.btnRecordStream.setFont(QtGui.QFont("monospace", 15))
        self.btnRecordStream.setGeometry(0, self.btnSwitchControlMode.geometry().top() - (
            self.BUTTON_HEIGHT + self.MARGIN_SIZE), targetWidth, self.BUTTON_HEIGHT)
        # Start/Stop Stream button
        self.btnStartStopStream = QtWidgets.QPushButton(self.speedContainer)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.btnStartStopStream.setMaximumHeight(100)
        self.btnStartStopStream.setMinimumHeight(100)
        self.btnStartStopStream.setFont(QtGui.QFont("monospace", 15))
        self.btnStartStopStream.clicked.connect(self.start_stop_stream)
        self.btnStartStopStream.setGeometry(0, self.btnRecordStream.geometry().top() - (
            self.BUTTON_HEIGHT + self.MARGIN_SIZE), targetWidth, self.BUTTON_HEIGHT)
        # Connect/Disconnect button
        self.btnConnectDisconnect = QtWidgets.QPushButton(self.speedContainer)
        self.btnConnectDisconnect.setText("Connect")
        self.btnConnectDisconnect.setStyleSheet("color: #4222F3;")
        self.btnConnectDisconnect.setMaximumHeight(100)
        self.btnConnectDisconnect.setMinimumHeight(100)
        self.btnConnectDisconnect.setFont(QtGui.QFont("monospace", 17, QtGui.QFont.Weight.Bold))
        self.btnConnectDisconnect.clicked.connect(self.connect_disconnect)
        self.btnConnectDisconnect.setGeometry(0, self.btnStartStopStream.geometry().top() - (
            self.BUTTON_HEIGHT + self.MARGIN_SIZE), targetWidth, self.BUTTON_HEIGHT)
        # Robot control commands display
        labelHeight = self.btnConnectDisconnect.geometry().top() - self._lblTitle.geometry().bottom() - self.MARGIN_SIZE * 2
        self.lblStatus = QtWidgets.QLabel(self.speedContainer)
        self.lblStatus.setWordWrap(True)
        self.lblStatus.setMinimumHeight(100)
        self.lblStatus.setText(Texts.NOT_CONNECTED)
        self.lblStatus.setStyleSheet("color: #052BF3;")
        self.lblStatus.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.lblStatus.setFont(QtGui.QFont("monospace", 20, weight=QtGui.QFont.Weight.Medium))
        self.lblStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lblStatus.setGeometry(0, self._lblTitle.geometry().bottom() + self.MARGIN_SIZE, self._lblTitle.width(),
                                   labelHeight)
        # Set container and root to window
        self.grabKeyboard()
        self.setCentralWidget(root)
        self.setWindowTitle("Robot Wireless Control Unit")
        self.setMinimumSize(self.WINDOW_SIZE.width(), self.WINDOW_SIZE.height())
        self.setMaximumSize(self.WINDOW_SIZE.width(), self.WINDOW_SIZE.height())
        self.showFullScreen()
        # WCU features #
        self.logger = Logger("WCU-GUI")
        self.driver = CarManualDriver(self)
        self.streamViewer = StreamViewer(self)
        self.connection = ConnectionService(self)
        self.arm_controller = ArmControllerWindow(self.handle_arm_data)

    @property
    def status(self) -> int:
        return Status.CONNECTED if self.connection.connected else Status.NOT_CONNECTED

    def on_init(self):
        # Reset all gui controls
        self.btnQuit.setEnabled(False)
        self.btnRecordStream.setEnabled(False)
        self.btnArmController.setEnabled(False)
        self.btnStartStopStream.setEnabled(False)
        self.btnConnectDisconnect.setEnabled(False)
        self.btnSwitchControlMode.setEnabled(False)
        self.update_status_lbl_text("Initializing...")
        self.log_to_list("ConnectionService", "Initializing...")
        self.imgRTV.setPixmap(QtGui.QPixmap(QtGui.QImage(os.path.relpath('wcu\\assets\\disconnected.png'))))
        # Create necessary directories if needed
        try:
            os.mkdir(os.path.relpath('stream'))
            self.logger.success("Stream folder created.")
        except FileExistsError:
            self.logger.success("Stream folder exists.")

    def on_ready(self):
        self.btnQuit.setEnabled(True)
        self.btnArmController.setEnabled(False)
        self.btnRecordStream.setEnabled(False)
        self.btnStartStopStream.setEnabled(False)
        self.btnConnectDisconnect.setEnabled(True)
        self.btnSwitchControlMode.setEnabled(False)
        self.update_status_lbl_text("Ready to connect...")
        self.btnConnectDisconnect.setStyleSheet(f"color: {GuiColors.BLUE}")
        self.log_to_list("ConnectionService", "Ready to connect", GuiColors.GREEN)

    def on_connecting(self):
        self.btnRecordStream.setEnabled(False)
        self.btnArmController.setEnabled(False)
        self.lblStatus.setText(Texts.CONNECTING)
        self.btnStartStopStream.setEnabled(False)
        self.btnConnectDisconnect.setEnabled(False)
        self.btnSwitchControlMode.setEnabled(False)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.btnConnectDisconnect.setText(Texts.CONNECTING)
        self.update_status_lbl_text("Connecting to Robot...")
        self.btnConnectDisconnect.setStyleSheet(f"color: {GuiColors.BLUE}")
        self.log_to_list("ConnectionService", "Connecting to robot...", GuiColors.BLUE)

    def on_connect(self):
        self.btnArmController.setEnabled(True)
        self.btnStartStopStream.setEnabled(True)
        self.btnConnectDisconnect.setEnabled(True)
        self.btnSwitchControlMode.setEnabled(True)
        self.lblStatus.setText(Texts.FAILED_TO_CONNECT)
        self.btnConnectDisconnect.setText(Texts.DISCONNECT)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.btnConnectDisconnect.setStyleSheet(f"color: {GuiColors.RED}")
        self.update_status_lbl_text("Waiting for commands...", GuiColors.BLUE)
        self.log_to_list("ConnectionService", "Established a connection with robot successfully.", GuiColors.GREEN)

    def on_fail(self, reason: str | None):
        self.btnRecordStream.setEnabled(False)
        self.btnArmController.setEnabled(False)
        self.btnStartStopStream.setEnabled(False)
        self.btnConnectDisconnect.setEnabled(True)
        self.btnSwitchControlMode.setEnabled(False)
        self.btnConnectDisconnect.setText(Texts.RECONNECT)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.update_status_lbl_text(f"{reason}", GuiColors.RED)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.log_to_list("ConnectionService", f"{reason}", GuiColors.RED)
        self.btnConnectDisconnect.setStyleSheet(f"color: {GuiColors.BLUE}")

    def on_disconnect(self):
        self.btnRecordStream.setEnabled(False)
        self.btnArmController.setEnabled(False)
        self.btnStartStopStream.setEnabled(False)
        self.btnConnectDisconnect.setEnabled(True)
        self.btnSwitchControlMode.setEnabled(False)
        self.lblStatus.setText(Texts.NOT_CONNECTED)
        self.btnConnectDisconnect.setText(Texts.CONNECT)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.btnConnectDisconnect.setStyleSheet(f"color: {GuiColors.BLUE}")
        if self.arm_controller.isVisible():
            self.arm_controller.close()
        self.log_to_list("ConnectionService", "Lost connection with robot.", GuiColors.RED)

    def on_stream_connecting(self):
        self.btnStartStopStream.setEnabled(False)
        self.btnStartStopStream.setText(Texts.REQUESTING_STREAM)
        self.log_to_list("StreamViewer", "Connecting to robot stream service...", GuiColors.BLUE)
        self.imgRTV.setPixmap(QtGui.QPixmap(os.path.relpath('wcu\\assets\\loading.png')))

    def on_stream_start(self):
        self.btnStartStopStream.setEnabled(True)
        self.btnStartStopStream.setText(Texts.STOP_STREAM)
        self.log_to_list("StreamViewer", "Started viewing stream.", GuiColors.GREEN)
        self.imgRTV.setPixmap(QtGui.QPixmap(os.path.relpath('wcu\\assets\\connected.png')))

    def on_stream_first_frame(self, image: Image.Image):
        self.btnRecordStream.setEnabled(False)
        self.btnStartStopStream.setEnabled(True)
        self.btnStartStopStream.setText(Texts.STOP_STREAM)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.log_to_list("StreamViewer", "Received first frame from stream.", GuiColors.GREEN)

    def on_stream_receive_frame(self, image: Image.Image):
        try:
            self.imgRTV.setPixmap(QtGui.QPixmap(QtGui.QImage(os.path.relpath('wcu\\stream\\lastFrame.jpeg'))))
            self.log_to_list("StreamViewer", f"Received frame: {image.size} | {image.format}", GuiColors.BLUE)
        except Exception as e:
            self.logger.error(e)
            # self.logToList("StreamViewer", f"Error displaying frame: {e}", GuiColors.BLUE)

    def on_stream_fail(self, reason: str):
        self.btnStartStopStream.setEnabled(True)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.log_to_list("StreamViewer", f"Failed to request stream. Reason('{reason}').", GuiColors.RED)
        self.imgRTV.setPixmap(QtGui.QPixmap(os.path.join(os.path.relpath('wcu\\assets\\disconnected.png'))))

    def on_stream_stop(self):
        self.btnRecordStream.setEnabled(False)
        self.btnStartStopStream.setEnabled(False)
        self.btnStartStopStream.setText(Texts.START_STREAM)
        self.btnRecordStream.setText(Texts.START_RECORDING_STREAM)
        self.log_to_list("ConnectionService", "Lost connection with robot.")
        self.imgRTV.setPixmap(QtGui.QPixmap(os.path.join(os.path.relpath('wcu\\assets\\disconnected.png'))))

    def on_drive_forward(self):
        if self.connection.send(data2json({"cmd": Directions.CMD_DRIVE_FORWARD})) > 0:
            self.log_to_list("CarDriver", "Moved forward.", )
            self.lblStatus.setText("Moved forward")
        else:
            self.connection.disconnect()
            self.log_to_list("ConnectionService", "Lost connection with robot")

    def on_drive_backward(self):
        if self.connection.send(data2json({"cmd": Directions.CMD_DRIVE_BACKWARD})) > 0:
            self.log_to_list("CarDriver", "Moved backward.", )
            self.lblStatus.setText("Moved backward")
        else:
            self.connection.disconnect()
            self.log_to_list("ConnectionService", "Lost connection with robot")

    def on_steer_right(self):
        if self.connection.send(data2json({"cmd": Directions.CMD_ROTATE_RIGHT})) > 0:
            self.log_to_list("CarDriver", "Steered right.", )
            self.lblStatus.setText("Steered right.")
        else:
            self.connection.disconnect()
            self.log_to_list("ConnectionService", "Lost connection with robot")

    def on_steer_left(self):
        if self.connection.send(data2json({"cmd": Directions.CMD_ROTATE_LEFT})) > 0:
            self.log_to_list("CarDriver", "Steered left.", )
            self.lblStatus.setText("Steered left.")
        else:
            self.connection.disconnect()
            self.log_to_list("ConnectionService", "Lost connection with robot")

    def on_stop(self):
        if self.connection.send(data2json({"cmd": Directions.CMD_STOP})) > 0:
            self.log_to_list("CarDriver", "Activated Brakes.", )
            self.lblStatus.setText("Stopped moving.")
        else:
            self.connection.disconnect()
            self.log_to_list("ConnectionService", "Lost connection with robot")

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        self.log_to_list("WCU", "GUI Initialized Successfully.")
        self.log_to_list("ConnectionService", "Press (Connect) button to connect to Robot.")
        return super().showEvent(event)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.log_to_list("WCU", "Closing...")
        if self.arm_controller.isVisible():
            self.arm_controller.close()
        self.connection.disconnect()
        self.streamViewer.stop_stream_view()
        return super().closeEvent(a0)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        # Check if WCU is connected or not
        if self.status == Status.NOT_CONNECTED:
            return
        # Operate according to pressed key
        key_pressed = event.key()
        match key_pressed:
            case QtCore.Qt.Key.Key_Escape | QtCore.Qt.Key.Key_Q:
                # Exit the application
                self.close()
            case _:
                # Decide where to go according to key pressed
                self.driver.decide(key_pressed)
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        return super().keyReleaseEvent(event)

    def log_to_list(self, tag: str, msg: str, color: str = GuiColors.BLACK):
        # Append msg to log list and scroll to bottom
        item = QtWidgets.QListWidgetItem()
        item.setForeground(QtGui.QColor(color))
        item.setFont(QtGui.QFont("monospace", 13, weight=QtGui.QFont.Weight.Normal))
        item.setText(f"[{tag}-{datetime.strftime(datetime.now(), '%H:%M:%S')}] -> {msg}")
        self.listLog.addItem(item)
        self.listLog.scrollToBottom()

    def update_status_lbl_text(self, msg: str, color=GuiColors.BLACK):
        # Show text also on commands label
        self.lblStatus.setText(msg)
        self.lblStatus.setStyleSheet(f"color: {color};")

    def connect_disconnect(self):
        if self.connection.connected:
            self.connection.disconnect()
            self.streamViewer.stop_stream_view()
        else:
            self.connection.connect()

    def switch_control_mode(self):
        if self.connection.request_SCM():
            self.log_to_list("Robot", "Switched control mode.")
        else:
            self.log_to_list("Robot", "Can't switch control mode.")

    def start_stop_stream(self):
        if self.streamViewer.viewing_stream:
            # Close stream
            if self.connection.request_close_stream():
                self.streamViewer.stop_stream_view()
        else:
            # Start stream
            if self.connection.request_start_stream():
                self.streamViewer.start_stream_view()

    def handle_arm_data(self, joint, angle, opt):
        na = angle + 1 if opt == Opts.INC else angle - 1
        payload = data2json({'arm': 1, 'jid': joint[0], 'ag': na})  # super important model to be used in rpi
        self.logger.info(f'ArmController wants to send payload: {payload}')
        if self.connection.send(payload) > 0:
            self.log_to_list(self.arm_controller.tag, f"'{joint[0]}' by {na} degrees.", GuiColors.GREEN)
            self.arm_controller.ujr(joint[0], na)

    def show_arm_controller(self):
        if self.arm_controller is None:
            self.arm_controller = ArmControllerWindow(self.handle_arm_data)
        self.arm_controller.show()


def myExceptHook(type, value, tback):
    sys.__excepthook__(type, value, tback)


if __name__ == "__main__":
    # Hook my exception handler before anything
    sys.__excepthook__ = myExceptHook
    # Create and start execution of the WCU app
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    try:
        code = app.exec_()
        print(f"WCU finished with code: {code}")
        sys.exit(code)
    except Exception as e:
        print(f"Exiting after error occurred. Type[{type(e)}] MSG[{e}]")
