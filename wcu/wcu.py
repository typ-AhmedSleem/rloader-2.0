# from sockets import ServerSocket, get_my_addr
# import wcu_utils as utils
# from json import loads as toJSON
# from time import sleep
# from random import choice as pickOneFrom
# from threading import Thread, Event

# server = ServerSocket()
# server.bind((get_my_addr(), utils.PORT_DATA_SOCKET))
# server.listen(0)
# server.settimeout(None)
# client = server.accept()[0]
# client.settimeout(60)
# print("WCU has connected")
# while True:
#     try:
#         rcvd = client.receive(1024)
#         if not rcvd:
#             raise ConnectionAbortedError
#         model = toJSON(rcvd.decode('utf-8'))
#         print(f"Received '{model}' from wcu.")
#         if model['signal'] == utils.Signals.SIGNAL_START_STREAM:
#             print("Received 'StartStream' signal")
#             client.send(utils.Signals.SIGNAL_ACK)
#             print("Sent 'ACK' signal to wcu.")
#             # Start stream
            
#         elif model['signal'] == utils.Signals.SIGNAL_CLOSE_STREAM:
#             print("Received 'CloseStream' signal")
#             client.send(utils.Signals.SIGNAL_ACK)
#             print("Sent 'ACK' signal to wcu.")
#         elif model['signal'] == utils.Signals.SIGNAL_SWITCH_CONTROL_MODE:
#             print("Received 'SwitchControlMode' signal from wcu.")
#             client.send(utils.Signals.SIGNAL_ACK)
#             print("Sent 'ACK' signal to wcu.")
#     except (ConnectionAbortedError, ConnectionResetError):
#         print("Lost connection with Robot.")
#         break
#     except (KeyboardInterrupt, TimeoutError):
#         server.close()
#         print("Finished")
#         break
import flet as ft
import socket

def main(page: ft.Page):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()
    d = socket.getfqdn()
    h = socket.gethostbyname(d)
    print(f"D: {d} | H: {h}")

ft.app(target=main)