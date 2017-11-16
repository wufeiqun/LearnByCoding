//TCPServer
package main

import (
	"flag"
	"fmt"
	//"io"
	"net"
	"os"
)

func main() {
	host := "0.0.0.0"
	port := flag.String("port", "8888", "监听端口") //指针类型, 通过*port来获取真实的值

	flag.Parse()

	listener, err := net.Listen("tcp4", host+":"+*port)
	if err != nil {
		fmt.Println("Error listening:", err)
		os.Exit(1)
	}
	defer listener.Close()
	fmt.Println("Server start at: " + host + ":" + *port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("Error accepting: ", err)
			continue
		}

		go handle(conn)

	}

}

func handle(conn net.Conn) {
	defer conn.Close()
	fmt.Printf("Received new connection: %s -> %s \n", conn.RemoteAddr(), conn.LocalAddr())
	data := make([]byte, 1024*1024)
	for {
		length, _ := conn.Read(data)
		fmt.Println(data[:length])
	}
}
