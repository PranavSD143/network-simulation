from abc import ABC, abstractmethod

class TransportLayer(ABC):
    def __init__(self, dest_ip, dest_port):
        self.dest_ip = dest_ip
        self.dest_port = dest_port

    @abstractmethod
    def send(self, data: bytes):
        pass