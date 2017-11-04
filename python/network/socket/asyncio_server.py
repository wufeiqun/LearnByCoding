import os
import asyncio
import argparse
# 参考https://docs.python.org/3/library/asyncio-protocol.html#asyncio.Protocol.eof_received


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.client_address = transport.get_extra_info("peername")
        print("收到{0}:{1}的连接!".format(*self.client_address))
        self.transport = transport

    def data_received(self, data):
        message = data.decode(encoding="utf-8", errors="ignore")
        print("接收到来自客户端: {1}:{2}的数据: {0}".format(message, *self.client_address))
        self.transport.write("谢谢你!\n".encode())

    def eof_received(self):
        print("eof received!")

    def connection_lost(self, exc):
        print("客户端 {0}:{1}断开连接!".format(*self.client_address))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简单的TCP回显服务器!")
    parser.add_argument("--hostname", dest="hostname", default="0.0.0.0", metavar="IP", help="请输入监听的IP地址")
    parser.add_argument("--port", dest="port", type=int, default=8888, metavar="端口", help="请输入监听的端口")
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    # 每一个新的请求实例化一个类
    coro = loop.create_server(EchoServerClientProtocol, args.hostname, args.port)
    server = loop.run_until_complete(coro)

    print("Server start at: {1}:{2} PID:{0}".format(os.getpid(), *server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
