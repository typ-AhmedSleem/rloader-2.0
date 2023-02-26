import socket as sockets
import uuid

def get_my_addr():
    return sockets.gethostbyaddr(sockets.gethostname())

def get_my_host(static: bool = False):
    return sockets.gethostname() if not static else '192.168.188.141'

class SocketError(Exception):
    """ Socket Error """

    def __init__(self, *args: object) -> None:
        """ Socket Error """
        super().__init__(*args)

class ConnectionClosedUnexpectedlyError(SocketError):
    pass

class NetAddress:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def to_tuple(self):
        return (self.host, self.port)

    def __repr__(self) -> str:
        return 'NetAddress(host=\'{}\', port={})'.format(self.host, self.port)


class ServerSocket:

    def __init__(self) -> None:
        # Runtime
        self.__source_address = None
        self.connected_clients: dict[str, ClientSocket] = {}
        self._server = sockets.socket()

    def __getitem(self, client_id: str):
        return self.get_client(client_id)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.closed():
            self.close()

    def bind(self, address):
        if address is None:
            raise ArgumentError("Address can't be None.")
        self.__source_address = address
        self._server.bind(self.__source_address)

    def listen(self, back_log: int = 1):
        self._server.listen(back_log)

    def accept(self):
        client_socket, addr = self._server.accept()
        # Append client to connected clients
        client = ClientSocket(client_socket)
        self.connected_clients[client.get_uid()] = client
        # Return client and its address
        return (client, NetAddress(addr[0], addr[1]))

    def close(self):
        if not self.closed():
            self._server.close()

    def closed(self, *args) -> bool:
        return self._server._closed  # type: ignore

    def settimeout(self, timeout: float):
        self._server.settimeout(timeout)

    def get_client(self, client_id: str):
        return self.connected_clients.get(client_id, None)

    def get_clients_number(self) -> int:
        return len(self.connected_clients)

    def get_source_addr(self):
        return self.__source_address


class ClientSocket:

    def __init__(self, socket: sockets.socket = None) -> None:
        # Socket
        if socket:
            self._socket = socket
        else:
            self._socket = sockets.socket(sockets.AF_INET, sockets.SOCK_STREAM)
        # Generate UUID for this client
        self._uid = uuid.uuid1().hex

    def __getitem__(self, buffer_size: int = 1024):
        return self.receive(buffer_size)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.opened:
            self.close()

    def connect(self, address):
        self._socket.connect(address.to_tuple() if type(address) is NetAddress else address)

    def connect_ex(self, address: NetAddress) -> int:
        return self._socket.connect_ex(address.to_tuple())

    def send(self, data, handle_error: bool = False) -> int:
        if self.closed:
            raise SocketError('Socket is closed.')
        else:
            if handle_error:
                try:
                    return self._socket.send(data.encode('utf-8') if type(data) is str else data)
                except:
                    return -1
            else:
                return self._socket.send(data.encode('utf-8') if type(data) is str else data)

    def receive(self, buffer_size: int = 1024) -> bytes:
        return self._socket.recv(buffer_size)

    def close(self):
        if not self.closed:
            self._socket.close()

    @property
    def closed(self) -> bool:
        return self._socket._closed  # type: ignore

    @property
    def opened(self) -> bool:
        return not self.closed

    def settimeout(self, timeout: float):
        self._socket.settimeout(timeout)

    def shutdown(self, how: int):
        self._socket.shutdown(how)

    def get_uid(self):
        return self._uid
