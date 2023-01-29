from logger import Logger
import wcu_utils as utils
from threading import Event, Thread
from json import dumps as data2Json
from sockets import ClientSocket, SocketError
from socket import (
    gethostbyname,
    timeout as SocketTimeoutError,
    gaierror as GetAddressInfoError)


class ConnectionCallback:

    def on_init(self):
        pass

    def on_ready(self):
        pass

    def on_connecting(self):
        pass

    def on_fail(self, reason: str | None):
        pass

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_error(self, reason: str | None):
        pass


class ConnectionService:

    def __init__(self, callback: ConnectionCallback) -> None:
        # Attach callback to this service
        self.callback = callback
        self.callback.on_init()
        # Runtime prepare
        self.conn_switcher = Event()
        self.logger = Logger("ConnectionService")
        self.logger.info("Initializing service...")
        # Connection service is ready
        self.callback.on_ready()
        self.logger.success("Initialized successfully.")

    @property
    def connected(self) -> bool:
        return self.conn_switcher.is_set()

    def connect(self) -> None:
        # Check if already connected
        if self.connected:
            self.logger.warning("Service is already connected !!")
            return
        # Connection socket
        self.socket = ClientSocket()
        self.socket.settimeout(1)
        # Start a connection handler
        ConnectionHandler().handle_connection(self)

    def disconnect(self) -> None:
        if self.connected:
            try:
                self.socket.close()
                self.conn_switcher.clear()
                self.callback.on_disconnect()
                self.logger.info("Closed connection successfully.")
            except:
                self.logger.error("Can't close connection.")
        else:
            self.logger.warning("Service hasn't connected to be disconnected.")

    def send(self, json_data: str) -> int:
        if not self.connected:
            self.logger.warning("Service hasn't connected yet.")
            return 0
        try:
            bytes_sent = self.socket.send(json_data)
            if not bytes_sent:
                raise SocketError()
            self.logger.info(f"Sent: '{json_data}' of length: {bytes_sent} byte.")
            return bytes_sent
        except (TimeoutError, SocketTimeoutError):
            self.logger.error("Timeout while trying to send data.")
            self.callback.on_error("Timeout while trying to send data.")
            return 0
        except (ConnectionAbortedError, ConnectionResetError, SocketError):
            self.logger.error("Connection was closed unexpectedly.")
            self.callback.on_error("Connection was closed unexpectedly.")
            return 0

    def receive(self, buffer_size=1024, deserialize_json: bool = False) -> str | None:
        if not self.connected:
            self.logger.warning("Service hasn't connected yet.")
            return None
        try:
            rcvd_data = self.socket.receive(buffer_size).decode('utf-8')
            self.logger.info(f"Received payload: {rcvd_data}")
            return rcvd_data
        except (TimeoutError, SocketTimeoutError):
            return None

    def request_start_stream(self) -> bool:
        if self.send(data2Json({"signal": utils.Signals.SIGNAL_START_STREAM})) > 0:
            # Wait for ACK signal
            return True if self.receive() == utils.Signals.SIGNAL_ACK else False
        # Can't request stream
        return False

    def request_close_stream(self) -> bool:
        if self.send(data2Json({"signal": utils.Signals.SIGNAL_CLOSE_STREAM})) > 0:
            # Wait for ACK signal
            return True if self.receive() == utils.Signals.SIGNAL_ACK else False
        # Can't request stream
        return False

    def request_SCM(self) -> bool:
        if self.send(data2Json({"signal": utils.Signals.SIGNAL_SWITCH_CONTROL_MODE})) > 0:
            # Wait for ACK signal
            return True if self.receive() == utils.Signals.SIGNAL_ACK else False
        # Can't request stream
        return False

class ConnectionHandler:

    def handle_connection(self, service: ConnectionService):
        Thread(name="Con-Handler", target=self.handler_job, args=[service]).start()

    def handler_job(self, service: ConnectionService):
        try:
            service.callback.on_connecting()
            service.logger.info("Connecting to robot...")
            # Resolve the address of robot will be connected on
            robot_host = gethostbyname(utils.ROBOT_HOSTNAME)
            address = (robot_host, utils.PORT_DATA_SOCKET)
            service.logger.success(f"Found 'rloader' at '{robot_host}'")
            # Connect to robot on resolved address
            service.socket.connect(address)
            service.conn_switcher.set()
            service.callback.on_connect()
            service.logger.success("Established a connection to robot successfully.")
        except GetAddressInfoError:
            service.logger.error("Can't find 'rloader' host on network.")
            service.callback.on_fail("Can't find 'rloader' host on network.")
        except (TimeoutError, SocketTimeoutError):
            service.conn_switcher.clear()
            service.logger.error("Timeout while trying to connect.")
            service.callback.on_fail("Timeout while trying to connect.")
        except ConnectionRefusedError:
            service.logger.error("Connection was refused by the target machine.")
            service.callback.on_fail("Connection was refused by the target machine.")
        finally:
            service.logger.info("ConnectionHandler finished his job.")
