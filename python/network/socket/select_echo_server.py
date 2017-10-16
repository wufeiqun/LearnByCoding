#!/usr/bin/env python
import sys
import queue
import socket
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server_addr = ("0.0.0.0", 8888)
server.bind(server_addr)
server.listen(5)

rlist = [server]
wlist = []
message_queues = {}

while rlist:
    try:
        readable, writable, exceptional = select.select(rlist, wlist, rlist, 10)
        if not (readable or writable or exceptional):
            print('在指定时间内未发现活跃的socket,这里可以做一些其它的事情!')
            continue
    except select.error:
        print("select error")

    for s in readable:
        if s is server:
            conn, client_addr = s.accept()
            print("{0}:{1} connected!".format(*client_addr))
            conn.setblocking(False)
            rlist.append(conn)
            message_queues[conn] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                print("Received data: {0} from {1}:{2}".format(data.decode(encoding="utf-8", errors="ignore"), *s.getpeername()))
                message_queues[s].put("谢谢你")
                print("Put received data to queue: {0}:{1}!".format(*s.getpeername()))
                if s not in wlist:
                    wlist.append(s)
                    print("Put {0}:{1} to wlist!".format(*s.getpeername()))
            else:
                print("Client: {0}:{1} closed!".format(*s.getpeername()))
                if s in wlist:
                    wlist.remove(s)
                rlist.remove(s)
                s.close()
                del message_queues[s]
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            #print("{0}:{1} queue empty!".format(*s.getpeername()))
            wlist.remove(s)
            #print("Put {0}:{1} out wlist!".format(*s.getpeername()))
        else: # 当try语句执行的时候才执行else
            print("sending {0} to {1}:{2}".format("谢谢你", *s.getpeername()))
            s.send("谢谢你".encode())
    for s in exceptional:
        print("exceptional occur on {0}:{1}".format(*s.getpeername()))
        rlist.remove(s)
        if s in wlist:
            wlist.remove(s)
        s.close()
        del message_queues[s]



