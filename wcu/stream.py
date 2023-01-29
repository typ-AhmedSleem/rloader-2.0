import os
import struct
import pickle
from PIL import Image
from io import BytesIO
import wcu_utils as utils
from logger import Logger
from threading import Thread, Event
from sockets import ClientSocket
from socket import (
    gethostbyname,
    gaierror as GetAddressInfoError,
    timeout as SocketTimeoutError
)


class StreamViewerCallback:

    def on_stream_connecting(self):
        pass

    def on_stream_start(self):
        pass

    def on_stream_first_frame(self, frame):
        pass

    def on_stream_receive_frame(self, frame):
        pass

    def on_stream_stop(self):
        pass

    def on_stream_fail(self, reason: str):
        pass


class StreamViewer:

    def __init__(self, callback: StreamViewerCallback) -> None:
        # StreamViewer runtime
        self.switcher = Event()
        self.logger = Logger("StreamViewer")
        self.callback = callback
        self.logger.success("Initialized successfully.")

    @property
    def viewing_stream(self):
        return self.switcher.is_set()

    def start_stream_view(self):
        if self.viewing_stream:
            self.logger.warning("StreamView is already running.")
            return
        # Start a new StreamHandler instance
        StreamHandler().handle_stream(self)

    def stop_stream_view(self):
        if self.viewing_stream:
            try:
                self.switcher.clear()
                self.callback.on_stream_stop()
                self.logger.info("Stopped viewing robot stream.")
            except:
                self.logger.error("Can't stop StreamView.")
        else:
            self.logger.warning("StreamView is already stopped.")


class StreamHandler:

    def handle_stream(self, viewer: StreamViewer):
        Thread(name='StreamHandler-Thread', target=self._stream_handler_job, args=[viewer]).start()

    def _stream_handler_job(self, viewer: StreamViewer):
        # Connection socket
        streamSocket = ClientSocket()
        streamSocket.settimeout(10)
        try:
            viewer.switcher.clear()
            received_first_frame = False
            # Resolve the address of robot will be connected on
            viewer.callback.on_stream_connecting()
            viewer.logger.info("Connecting to stream...")
            # Connection runtime
            robot_host = gethostbyname(utils.ROBOT_HOSTNAME)
            address = (robot_host, utils.PORT_RTV_SOCKET)
            viewer.logger.success(f"Found 'rloader' at '{robot_host}'")
            # Connect to stream
            streamSocket.connect(address)
            # Notify callback
            viewer.switcher.set()
            viewer.callback.on_stream_start()
            # Create byte-like connection for reading stream
            connection = streamSocket.makefile('rb')
            viewer.logger.success("Established a connection to stream successfully.")
            # Start StreamReceiver job
            while viewer.switcher.is_set():
                # Receive frame size from connection
                frameSize = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not frameSize:
                        # Received an empty packet
                        streamSocket.close()
                        viewer.switcher.clear()
                        viewer.logger.info("Received empty packet from stream connection.")
                # Receive frame data
                frame_data = BytesIO()
                frame_data.write(connection.read(frameSize))
                frame_data.seek(0)
                # Handle the frame
                image = Image.open(frame_data)
                image.save(os.path.relpath('wcu\\stream\\lastFrame.jpeg'))
                # Pass frame to GUI through callback
                if not received_first_frame:
                    received_first_frame = True
                    viewer.callback.on_stream_first_frame(image)
                else:
                    viewer.callback.on_stream_receive_frame(image)
        except struct.error:
            viewer.switcher.clear()
        except GetAddressInfoError:
            viewer.logger.error("Can't find 'rloader' host on network.")
            viewer.callback.on_stream_fail("Can't find 'rloader' host on network.")
        except (TimeoutError, SocketTimeoutError):
            viewer.logger.error("Timeout while trying to connect.")
            viewer.callback.on_stream_fail("Timeout while trying to connect.")
        except ConnectionRefusedError:
            viewer.logger.error("Stream was refused by the target machine.")
            viewer.callback.on_stream_fail("Stream was refused by the target machine.")
        finally:
            streamSocket.close()
            viewer.logger.info("StreamHandler finished his job.")
