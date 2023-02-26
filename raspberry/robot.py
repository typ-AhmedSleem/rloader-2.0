from sockets import ServerSocket, ConnectionClosedUnexpectedlyError, get_my_host
import robot_utils as utils
from components import Car
from logger import Logger
from streamer import Streamer
from threading import Thread, Event
from time import sleep
from socket import gethostbyname, timeout as SocketTimeoutError
from json import dumps as data2json

class Robot:

    def __init__(self) -> None:
        self.logger = Logger("Robot")
        # Constants
        self.host = get_my_host(True)
        # Robot components
        self.car = Car()
        self.streamer = Streamer(address=(self.host, utils.PORT_RTV_SOCKET), resolution = (400,300))  # type: ignore
        # Server sockets
        self.communicationServer = ServerSocket()
        self.communicationServer.settimeout(20)
        # Switchers
        self.stream_switcher = Event()
        self.power_on_switcher = Event()

    def power_on(self):
        self.__enter__()
        # Init switchers
        connection_switcher = Event()
        self.power_on_switcher.set()
        # Setup the car
        self.car.setup()
        # Setup connection server
        try:
            self.communicationServer.bind((self.host, utils.PORT_DATA_SOCKET))
            self.communicationServer.listen(0)
        except OSError as e:
            self.logger.warning(f"{e}")
        # Serve as long as robot is running
        while self.power_on_switcher.is_set():
            try:
                # Wait for WCU to connect
                self.logger.info(f"Waiting for WCU to connect on address {(self.host, utils.PORT_DATA_SOCKET)} ...")
                wcu_connected = False
                connection = self.communicationServer.accept()[0]
                connection.settimeout(5)
                connection_switcher.set()
                self.logger.success("Successfully established a connection with WCU.")
                # Serve as long as connection is established
                while connection_switcher.is_set():
                    # Handle connection traffic
                    try:
                        rcvd_bytes = connection.receive(utils.DEFAULT_BUFFER_SIZE)
                        if rcvd_bytes is None or len(rcvd_bytes) == 0:
                            self.logger.error("Received empty packet which means connection was lost.")
                            raise ConnectionResetError()
                        # Handle received packets here
                        dataModel = utils.convertJsonToModel(rcvd_bytes.decode("utf-8"))
                        self.logger.info(f"Received from WCU: {dataModel}")
                        # Handle incoming signal
                        if dataModel.signal:
                            # Start stream signal
                            if dataModel.signal == utils.Signals.SIGNAL_START_STREAM:
                                # Send ACK signal back to WCU
                                if not connection.send(utils.Signals.SIGNAL_ACK):
                                    connection.close()
                                    self.logger.error("Can't send 'ACK' signal to WCU. Seems like connection was lost.")
                                    break
                                self.streamer.start_stream()
                            # Close stream signal
                            elif dataModel.signal == utils.Signals.SIGNAL_CLOSE_STREAM:
                                # Send ACK signal back to WCU
                                if not connection.send(utils.Signals.SIGNAL_ACK):
                                    connection.close()
                                    self.logger.error("Can't send 'ACK' signal to WCU. Seems like connection was lost.")
                                    break
                                self.streamer.stop_stream()
                            # Switch control mode signal
                            elif dataModel.signal == utils.Signals.SIGNAL_SWITCH_CONTROL_MODE:
                                # Send ACK signal back to WCU
                                if not connection.send(utils.Signals.SIGNAL_ACK):
                                    connection.close()
                                    self.logger.error("Can't send ACK signal to WCU. Seems like connection was lost.")
                                    break
                                # Switch control mode
                                if not self.car.is_auto_driving:
                                    # Start automatic driver
                                    self.car.start_automatic_driving()
                                    # Log
                                    self.logger.success("Started Automatic Driver.")
                                else:
                                    # Stop automatic driver
                                    self.car.stop_automatic_driving()
                                    # Log
                                    self.logger.success("Stopped Automatic Driver.")
                            elif dataModel.signal == utils.Signals.SIGNAL_DISCONNECT:
                                self.power_off()
                        # Handle manual driver commands
                        if dataModel.cmd and not self.car.is_auto_driving:
                            self.car.decide_direction(dataModel.cmd)
                    except (ConnectionResetError, ConnectionAbortedError, ConnectionRefusedError):
                        connection_switcher.clear()
                        connection.close()
                        self.logger.error("Connection was closed unexpectedly.")
                        break
                    except (TimeoutError, SocketTimeoutError):
                        continue
                    except KeyboardInterrupt:
                        connection_switcher.clear()
                        connection.close()
                        break
            except KeyboardInterrupt:
                self.communicationServer.close()
                self.logger.error("Process terminated by user.")
                self.power_off()
                exit(1)
            except (TimeoutError, SocketTimeoutError):
                continue
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError) as e:
                self.logger.error(f"Faced an error while establishing connection. Reason: '{e}'")

    def power_off(self):
        self.car.cleanup()
        self.power_on_switcher.clear()

    def __enter__(self):
        self.logger.info("rLoader robot v1.1")
        self.logger.info("Coded by: Ahmed Sleem. Programmer & Mechatronics Engineer")
        self.logger.info("Twitter: @typ_ahmed_sleem")
        self.logger.info("Email: typahmedsleem@gmail.com")
        self.logger.info("Github: https://github.com/typ-AhmedSleem")
        print("=" * 50)
        self.logger.info("Starting rLoader robot...")
        return self

    def __exit__(self, *args):
        self.communicationServer.close()
        exit("Robot worked well till termination.")
        
if __name__ == '__main__':
    Robot().power_on()