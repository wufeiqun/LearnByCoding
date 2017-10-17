#!/usr/bin/env python
#优点: 1. 相比较于select, 监控的fd没有数量限制
#缺点: 1. 只支持Linux, MacOS和Windows不支持(Mac上测试有bug)
import sys
import queue
import select
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.setblocking(False)

server_address = ("0.0.0.0", 8888)
server.bind(server_address)
print("Starting server at: {0}:{1}".format(*server_address))

server.listen(5)

message_queues = {}

TIMEOUT = 5000 #5s

READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = READ_ONLY | select.POLLOUT

# 创建一个poll实例
poller = select.poll()
# 将server注册到poll实例中
poller.register(server, READ_ONLY)

# 由于poll返回的是一个数组, 数组中的元素为元组, 元组格式为(fd, flag), 所以有必要定义一个fd_to_socket
fd_to_socket = {server.fileno(): server}
# 由于客户端socket关闭以后要删除fd_to_socket中保存的socket, 但是socket是value, 为了更加快速删除该条记录
# 又定义了一个socket_to_fd字典
socket_to_fd = {server: server.fileno()}

while True:
    print("事件监听中...")
    events = poller.poll(TIMEOUT)
    for fd, flag in events:
        sock = fd_to_socket[fd]
        if flag in (select.POLLIN, select.POLLPRI):
            if sock is server: # 说明是有新的客户端请求进来
                connection, client_address = sock.accept()
                print("收到{0}:{1}的连接!".format(*client_address))
                connection.setblocking(False)
                fd_to_socket[connection.fileno()] = connection
                socket_to_fd[connection] = connection.fileno()
                # 将新来的客户端socket注册到监听列表中
                poller.register(connection, READ_ONLY)
                # 这里使用了队列, 保存要返回的数据, 如果只是学习poll使用的话可以去掉, 让每个socket返回相同数据即可
                message_queues[connection] = queue.Queue()
            else: # 说明已经建立连接的socket有数传送过来据等待接收
                while True:
                    data = sock.recv(1024)
                    if data:
                        print("接收到来自客户端: {1}:{2}的数据: {0}".format(data.decode(encoding="utf-8", errors="ignore"),
                            *sock.getpeername()))
                        message_queues[sock].put("谢谢你".encode())
                        # 修改该socket监控状态为读写
                        poller.modify(sock, READ_WRITE)
                    else: # 客户端断开连接
                        print("客户端: {0}:{1} 断开连接!".format(*sock.getpeername()))
                        # 取消该socket的注册信息
                        poller.unregister(sock)
                        # 删除该socket的消息队列
                        del message_queues[sock]
                        # 从fd字段中删除该socket
                        del fd_to_socket[socket_to_fd[sock]]
                        del socket_to_fd[sock]
                        # 关闭该socket
                        sock.close()
        elif flag == select.POLLOUT: # 说明该socket是可写状态, 一般只要没有在可读状态的时候一个socket都是出于可写状态的
            try:
                next_msg = message_queues[sock].get_nowait() # 从消息队列里获取数据(前面填充到该队列里的数据)
            except queue.Empty: # 该socket的消息队列为空的时候表示已经读取并回复了, 这时候应该只监听该socket是否可读即可
                poller.modify(sock, READ_ONLY)
            else:
                sock.send(next_msg)
        elif flag in (select.POLLERR, select.POLLHUP):
            print("Socket: {0}:{1} 发生异常!".format(*sock.getpeername()))
            # 取消该socket的注册信息
            poller.unregister(sock)
            # 删除该socket的消息队列
            del message_queues[sock]
            # 从fd字段中删除该socket
            del fd_to_socket[socket_to_fd[sock]]
            del socket_to_fd[sock]
            sock.close()




