import struct
from io import BytesIO
from logger import Logger
from picamera import PiCamera
from sockets import ServerSocket
from threading import Event, Thread
from socket import timeout as SocketTimeoutError


class Streamer:

    def __init__(self, address, resolution=(900, 600)) -> None:
        self.logger = Logger("Streamer")
        self.stream_switcher = Event()
        # Init picamera runtime
        self.camera = PiCamera()
        self.camera.framerate = 30
        self.camera.vflip = True
        self.camera.resolution = resolution
        # Init socket runtime
        self.address = address
        self.streamSocket = ServerSocket()
        self.streamSocket.settimeout(20)
        self.logger.success("Streamer is initialized successfully")

    @property
    def streaming(self) -> bool:
        """ Tells whether Streamer is streaming or not

        Returns:
            bool: True if switcher is set, False otherwise
        """
        return self.stream_switcher.is_set()

    def start_stream(self):
        """  Starts streaming from picamera to WCU

        Raises:
            RuntimeWarning: If Streamer is already active streaming
        """
        if self.streaming:
            self.logger.warning("Already streaming !!!")
            return
        # Create StreamerHandler instance and start it
        StreamerHandler().handle_streamer(self)

    def stop_stream(self):
        """ Stops current active streaming """
        if self.streaming:
            self.stream_switcher.clear()


class StreamerHandler:

    def handle_streamer(self, streamer: Streamer):
        Thread(name="StreamerHandler", target=self._handler_job, args=[streamer]).start()

    def _handler_job(self, streamer: Streamer):
        # Prepare stream runtime
        try:
            streamer.logger.info("Starting stream...")
            # Turn on stream switcher
            streamer.stream_switcher.set()
            # Wait for WCU to connect
            self.streamSocket = ServerSocket()
            self.streamSocket.bind(streamer.address)
            self.streamSocket.listen(0)
            streamer.logger.info("Waiting for WCU to connect...")
            client = self.streamSocket.accept()[0]
            client.settimeout(5)
            connection = client._socket.makefile('wb')
            frame_stream = BytesIO()
            for fn in streamer.camera.capture_continuous(output=frame_stream, format="jpeg"):
                # Write frame size to connection
                frame_size = frame_stream.tell()
                connection.write(struct.pack("<L", frame_size))
                connection.flush()
                # Write frame data to connection
                frame_stream.seek(0)
                connection.write(frame_stream.read())
                # Reset the frame stream to receive the next frame
                frame_stream.seek(0)
                frame_stream.truncate()
                streamer.logger.info(f"Sent frame of size {round(frame_size / 1024, 1)} KBs.")
                # Check if stream switcher is switched off or not
                if not streamer.stream_switcher.is_set():
                    # Close stream
                    streamer.streamSocket.close()
                    streamer.logger.info("Stopping stream...")
                    break
            streamer.logger.info("Finished streaming.")
        except (TimeoutError, SocketTimeoutError):
            streamer.logger.info("Timeout while waiting for WCU to connect .")
        except KeyboardInterrupt:
            streamer.streamSocket.close()
            streamer.stream_switcher.clear()
            streamer.logger.warning("Streamer was forced to stop. Stopping...")
        except (
                ConnectionResetError,
                ConnectionAbortedError,
                ConnectionRefusedError,
                BrokenPipeError):
            # Connection was closed unexpectedly
            streamer.streamSocket.close()
            streamer.stream_switcher.clear()
            streamer.logger.error("Connection was closed unexpectedly.")
        finally:
            if streamer.streaming:
                streamer.streamSocket.close()
                streamer.stream_switcher.clear()
                streamer.logger.info("Streamer has finished.")


if __name__ == "__main__":
    streamer = Streamer(("rloader", 2002), (500, 480))
    streamer.start_stream()
