# coding=utf-8
import socket
import select
import SocketServer
import struct
import signal
import sys

class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    SocketServer.ThreadingMixIn:利用多线程实现异步。
    """
    pass


class Socks5Server(SocketServer.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                data_ = sock.recv(4096)
                if remote.send(data_) <= 0:
                    break
            if remote in r:
                data_ = remote.recv(4096)
                if sock.send(data_) <= 0:
                    break

    def handle(self):
        try:
            print 'socks connection from ', self.client_address
            sock = self.connection
            # 1. Version
            sock.recv(262)
            sock.send(b"\x05\x00")
            # 2. Request
            data = self.rfile.read(4)

            #ord 将字符转换成ascii码
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:  # IPv4
                addr = socket.inet_ntoa(self.rfile.read(4))
            elif addrtype == 3:  # Domain name
                addr = self.rfile.read(ord(sock.recv(1)[0]))
            port = struct.unpack('>H', self.rfile.read(2))
            reply = b"\x05\x00\x00\x01"
            try:
                if mode == 1:  # 1. Tcp connect
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    print 'Tcp connect to', addr, port[0]
                else:
                    reply = b"\x05\x07\x00\x01"  # Command not supported
                local = remote.getsockname()

                #inet_aton: Convert an IPv4 address from dotted-quad string format (for example, ‘123.45.67.89’)
                # to 32-bit packed binary format, as a string four characters in length.
                reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
            except socket.error:
                # Connection refused
                reply = '\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00'
            sock.send(reply)
            # 3. Transfering
            if reply[1] == '\x00':  # Success
                if mode == 1:  # 1. Tcp connect
                    self.handle_tcp(sock, remote)
        except socket.error:
            print 'socket error'


def main():
    server = ThreadingTCPServer(('127.0.0.1', 9086), Socks5Server)

    def handler(signum, _):
        server.server_close()

    signal.signal(getattr(signal, 'SIGQUIT', signal.SIGTERM), handler)

    def int_handler(signum, _):
            sys.exit(1)
    signal.signal(signal.SIGINT, int_handler)

    server.serve_forever()
    server.server_close()


if __name__ == '__main__':
    main()
