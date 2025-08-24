import socket
import struct
from transport_layer.base import TransportLayer

class TCPTransport(TransportLayer):
    def __init__(self, src_ip, dest_ip, src_port, dest_port, network_layer):
        self.src_ip = src_ip
        self.dest_ip = dest_ip
        self.src_port = src_port
        self.dest_port = dest_port
        self.seq = 0
        self.ack_seq = 0
        self.network_layer = network_layer  # <-- pass your NetworkLayer object here

    def checksum(self, msg):
        if len(msg) % 2 != 0:
            msg += b"\x00"
        s = sum(struct.unpack("!%dH" % (len(msg)//2), msg))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff

    def build_tcp_header(self, payload=b"", flags=0x18):  # 0x18 = PSH + ACK
        data_offset = 5
        window = 5840
        urg_ptr = 0

        # Temp checksum 0 for now
        tcp_header = struct.pack(
            "!HHLLBBHHH",
            self.src_port, self.dest_port, self.seq, self.ack_seq,
            data_offset << 4, flags, window, 0, urg_ptr
        )

        # Pseudo header for checksum
        pseudo_header = struct.pack(
            "!4s4sBBH",
            socket.inet_aton(self.src_ip),
            socket.inet_aton(self.dest_ip),
            0,
            6,  # TCP protocol
            len(tcp_header) + len(payload)
        )

        chksum = self.checksum(pseudo_header + tcp_header + payload)

        # Repack with correct checksum
        tcp_header = struct.pack(
            "!HHLLBBH",
            self.src_port, self.dest_port, self.seq, self.ack_seq,
            data_offset << 4, flags, window
        ) + struct.pack("H", chksum) + struct.pack("!H", urg_ptr)

        return tcp_header

    def send(self, data: bytes):
        tcp_header = self.build_tcp_header(data)
        packet = tcp_header + data
        self.network_layer.send(packet)

    def receive(self):
        packet = self.network_layer.receive()  
        tcp_segment = packet[20:]
        data_offset = (tcp_segment[12] >> 4) * 4
        payload = packet[data_offset:]
        return payload
    