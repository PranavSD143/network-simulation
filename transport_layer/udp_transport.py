import socket
from transport_layer.base import TransportLayer

class SimpleUDPTransport(TransportLayer):
    def send(self, data: bytes, timeout: float = 2.0) -> bytes:
        with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(data,(self.dest_ip,self.dest_port))
            try:
                resp, _ = s.recvfrom(65535)
                return resp
            except socket.timeout:
                return b''
