import socket
import struct

class SimpleIPNetwork:
    def __init__(self,src_ip:str,dest_ip:str):
        self.src_ip = src_ip
        self.dest_ip = dest_ip

    def checksum(self,data:bytes)->int:

        if(len(data)%2!=0):
            data += b'\x00'
        s = sum(struct.unpack("!%dH" % (len(data)//2),data))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        return ~s & 0xffff
    
    def build_ipv4_header(self,payload_len:int,protocol:int = socket.IPPROTO_UDP)->bytes:
        version_ihl = (4<<4)+5
        tos = 0
        total_length = 20 + payload_len
        identification = 54321
        flags_fragment_offset = 0
        ttl = 64
        header_checksum = 0

        src_ip_packed = socket.inet_aton(self.src_ip)
        dest_ip_packed = socket.inet_aton(self.dest_ip)

        header = struct.pack(
            "!BBHHHBBH4s4s",
            version_ihl, tos, total_length, identification,
            flags_fragment_offset, ttl, protocol, header_checksum,
            src_ip_packed, dest_ip_packed
        )
        header_checksum = self.checksum(header)
        header = struct.pack(
            "!BBHHHBBH4s4s",
            version_ihl, tos, total_length, identification,
            flags_fragment_offset, ttl, protocol, header_checksum,
            src_ip_packed, dest_ip_packed
        )

        return header
    
    def send(self,payload:bytes,protocol:int = socket.IPPROTO_TCP):
        ip_header = self.build_ipv4_header(payload_len = len(payload),protocol = protocol)
        packet = ip_header+payload

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as s:
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            s.sendto(packet, (self.dest_ip, 0))  # Port ignored at IP layer

    def receive(self):

        with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP) as s:
            # s.bind((self.src_ip, 0))
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            packet, addr = s.recvfrom(65535)  # Receive full packet (max size ~65KB)

            return packet
        


