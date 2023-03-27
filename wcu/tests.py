from time import sleep
from random import choice
from logger import Logger
from sys import argv as args
from connection import ConnectionService, ConnectionCallback
from car_driver import CarManualDriver, CarDriverCallback
from stream import StreamViewer, StreamViewerCallback


class TestService(ConnectionCallback):

    def __new__(cls):
        test = super().__new__(TestService)
        test.__init__()
        return test

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger("TestService")
        self.service = ConnectionService(self)

    def on_init(self):
        self.logger.info("Service is initializing...")

    def on_ready(self):
        self.logger.success("Service is ready.")

    def on_connecting(self):
        self.logger.info("Service is connecting...")

    def on_fail(self, reason: str | None):
        self.logger.error(f"Service failed to connect with reason: {reason}")

    def on_connect(self) -> None:
        self.logger.success("Service has connected to robot.")

    def on_disconnect(self):
        self.logger.info("Service has disconnected from robot.")

    def on_error(self, reason: str | None):
        self.logger.error(f"Service faced an error: {reason}")

    def perform_test(self):
        # Test 1
        self.service.connect()
        self.service.send("Hello!")
        self.service.disconnect()
        # Test 2
        self.service.send("Hello!")
        self.service.disconnect()
        self.service.connect()


class TestDriver(CarDriverCallback):

    def __new__(cls):
        test = super().__new__(TestDriver)
        test.__init__()
        return test

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger("TestDriver")
        self.driver = CarManualDriver(self)

    def on_drive_forward(self):
        self.logger.info("Drive forward.")

    def on_drive_backward(self):
        self.logger.info("Drive Backward.")

    def on_steer_right(self):
        self.logger.info("Steer Right.")

    def on_steer_left(self):
        self.logger.info("Steer left.")

    def perform_test(self):
        while True:
            try:
                key_pressed = choice(['w', 'a', 's', 'd'])
                self.driver.decide(key_pressed)
                sleep(1)
            except KeyboardInterrupt:
                break


class TestStream(StreamViewerCallback):

    def __new__(cls):
        test = super().__new__(TestStream)
        test.__init__()
        return test

    def __init__(self) -> None:
        super().__init__()
        self.logger = Logger("TestStream")
        self.viewier = StreamViewer(self)

    def on_stream_connecting(self):
        return
        self.logger.info("Stream is connecting...")

    def on_stream_start(self):
        return
        self.logger.success("Stream started.")

    def on_stream_fail(self, reason: str):
        return
        self.logger.error(f"{reason}")

    def on_stream_stop(self):
        return
        self.logger.success("Stream stopped.")

    def on_stream_first_frame(self, frame):
        return
        self.logger.success(f"Stream received first frame. size= {frame.size()}")

    def on_stream_receive_frame(self, image):
        # image.show()
        self.logger.success("Received first frame.")

    def perform_test(self):
        self.viewier.start_stream_view()


if __name__ == '__main__':
    test_type = args[1].strip().lower() if len(args) > 1 else None
    tests = {
        '-c': TestService,
        '-d': TestDriver,
        '-s': TestStream
    }
    if not test_type or not (test_type in tests):
        print("""
Select a test to perform it.
Available tests:
\t -c: Test the ConnectionService
\t -d: Test the CarManualDriver
\t -s: Test the StreamViewer
""")
    else:
        test = tests[test_type]
        test = test.__new__(test)
        test.perform_test()
