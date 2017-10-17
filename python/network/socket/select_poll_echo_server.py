#!/usr/bin/env python
#coding: utf-8
import sys
import queue
import select
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server_address = ("0.0.0.0", 8888)
server.bind(server_address)
print("Starting server at: {0}:{1}".format(*server_address))

server.listen(5)

message_queues = {}

TIMEOUT = 5000 #5s

READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = READ_ONLY | select.POLLOUT

# Set up the poller
poller = select.poll()
poller.register(server, READ_ONLY)

# 由于poll返回的是一个数组, 数组中的元素为元组, 元组格式为(fd, flag), 所以有必要定义一个fd_to_socket
fd_to_socket = {server.fileno(): server}

while True:
    print("waiting for the next event...")
    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        s = fd_to_socket[fd]
        if flag in (select.POLLIN, select.POLLPRI):
            if s is server:
                connection, client_address = s.accept()
                print("Client: {0}:{1} connected!".format(*client_address))
                connection.setblocking(False)
                fd_to_socket[connection.fileno()] = connection
                poller.register(connection, READ_ONLY)

                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print("Received data: {0} from {1}:{2}".format(data.decode(encoding="utf-8", errors="ignore"), *s.getpeername()))
                    message_queues[s].put("谢谢你".encode())
                    poller.modify(s, READ_WRITE)
                else: #client disconnected
                    print("Client: {0}:{1} closed!".format(*s.getpeername()))
                    poller.unregister(s)
                    s.close()
                    del message_queues[s]
        elif flag == select.POLLHUP:
            # Client hung up
            print("Closing hung up client: {0}:{1}".format(*s.getpeername()))
            poller.unregister(s)
            s.close()
        elif flag == select.POLLOUT:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                # No messages waiting so stop checking
                print("{0}:{1} queue empty".format(*s.getpeername()))
                poller.modify(s, READ_ONLY)
            else:
                print("Send: {0} to {1}:{2}".format(next_msg, *s.getpeername()))
                s.send(next_msg)
        elif flag == select.POLLERR:
            print("Exception occur on {0}:{1}".format(*s.getpeername()))
            poller.unregister(s)
            s.close()

            # Remove message queue
            del message_queues[s]




