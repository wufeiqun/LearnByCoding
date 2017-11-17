package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
)

func main() {

	var (
		host = "0.0.0.0"
		port string
	)

	if len(os.Args) <= 1 {
		port = "8888"
	} else {
		port = os.Args[1]
	}

	server_addr := host + ":" + port

	listen, err := net.Listen("tcp", server_addr)

	if err != nil {
		fmt.Println("服务启动发生错误: ", err)
		os.Exit(-1)
	}

	defer listen.Close()

	fmt.Printf("Server started at: %s...\n", server_addr)

	for {
		conn, err := listen.Accept()

		if err != nil {
			fmt.Println("客户端连接错误: ", err.Error())
			continue
		}

		go receiveFile(conn)
	}
}

func receiveFile(conn net.Conn) {
	var (
		end_flag       string
		temp_file_name string                    //保存临时文件名称
		data           = make([]byte, 1024*1024) //用于保存接收的数据的切片
		file_num       int                       //当前协程接收的数据在原文件中的位置
	)
	defer conn.Close()

	fmt.Println("收到新的连接请求: ", conn.RemoteAddr())

	j := 0 //标记接收数据的次数
	size := 0
	for {
		length, err := conn.Read(data)

		if err != nil {
			fmt.Printf("客户端: %v已断开. 协程号: %2d\n", conn.RemoteAddr(), file_num)
			return
		}
		//每个新建立的连接的第一次接收的数据是一些该数据块的信息, 包括是否结束字段, 该数据块的协程号, 该文件的名称等
		if j == 0 {
			end_flag = string(data[0:8])
			if end_flag == "fileover" {
				xienum := int(data[8])
				merge_file_name := string(data[9:length])
				go mainMergeFile(xienum, merge_file_name) //合并临时文件，生成有效文件
				end_flag = "文件接收完成: " + merge_file_name
				conn.Write([]byte(end_flag))
				fmt.Println(merge_file_name, "文件接收完成")
				return

			} else { //创建临时文件
				file_num = int(data[0])
				temp_file_name = string(data[1:length]) + strconv.Itoa(file_num)
				fmt.Println("创建临时文件：", temp_file_name)
				fout, err := os.Create(temp_file_name)
				if err != nil {
					fmt.Println("创建临时文件错误: ", temp_file_name)
					return
				}
				fout.Close()
			}
		} else {
			writeTempFileEnd(temp_file_name, data[0:length])
			size += length
		}

		end_flag = strconv.Itoa(file_num) + " 接收完成"
		conn.Write([]byte(end_flag))
		j++
	}
	fmt.Println(file_num)
	fmt.Println(size)

}

func writeTempFileEnd(filename string, data []byte) {
	temp_file, err := os.OpenFile(filename, os.O_APPEND|os.O_RDWR, 0666)
	if err != nil {
		fmt.Println("打开临时文件错误", err)
		return
	}
	defer temp_file.Close()
	temp_file.Write(data)
}

func mainMergeFile(block_number int, filename string) {

	file, err := os.Create(filename)
	if err != nil {
		fmt.Println("创建有效文件错误: ", err)
		return
	}
	defer file.Close()

	//依次对临时文件进行合并, 这里没有使用协程, 因为文件是有顺序的
	for i := 0; i < block_number; i++ {
		mergeFile(filename+strconv.Itoa(i), file)
	}

	//删除生成的临时文件
	for i := 0; i < block_number; i++ {
		os.Remove(filename + strconv.Itoa(i))
	}

}

/*
*	将指定临时文件合并到有效文件中
*	2013-09-26
*	李林
*
*	rfilename	临时文件名称
*	wfile	 	有效文件
 */
func mergeFile(temp_file string, wfile *os.File) {

	rfile, err := os.OpenFile(temp_file, os.O_RDONLY, 0666)

	if err != nil {
		fmt.Println("合并时打开临时文件错误: ", temp_file)
		return
	}

	defer rfile.Close()

	stat, _ := rfile.Stat()

	num := stat.Size()

	buf := make([]byte, 1024*1024)

	for i := 0; int64(i) < num; {
		length, err := rfile.Read(buf)

		if err != nil {
			fmt.Println("读取文件错误")
		}
		i += length

		wfile.Write(buf[:length])
	}

}
