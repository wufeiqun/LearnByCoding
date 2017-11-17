package main

import (
	"bytes"
	"fmt"
	"net"
	"os"
	"strconv"
	"time"
)

func main() {

	var (
		host            = "39.106.97.235"
		port            = "8888"
		server_addr     = host + ":" + port
		file_name       string
		merge_file_name string
		coroutine       int
		bufsize         int
		total_size      int64
		allocated_size  int64
	)

	if len(os.Args) <= 1 {
		fmt.Println("使用方法: up [文件名]")
		return
	} else {
		file_name = os.Args[1]       //待发送文件名称
		merge_file_name = os.Args[1] //待合并文件名称(在服务器上的文件名称)
	}

	//根据文件大小的范围确定比较合适的协程数和buffer size
	fileobj, err := os.OpenFile(file_name, os.O_RDONLY, 0666)
	if err != nil {
		fmt.Println("打开文件出错: ", err)
		return
	}
	defer fileobj.Close()

	filestat, err := fileobj.Stat() //获取文件状态

	total_size = filestat.Size() //获取文件总大小
	//当文件小于1M的时候
	if total_size < 1048576 {
		coroutine = 1     //协程数量或拆分文件的数量
		bufsize = 1048576 //单次发送数据的大小
	} else if total_size > 1048576 && total_size < 10485760 {
		coroutine = 4      //协程数量或拆分文件的数量
		bufsize = 1024 * 4 //单次发送数据的大小
	} else {
		coroutine = 8       //协程数量或拆分文件的数量
		bufsize = 1024 * 10 //单次发送数据的大小
	}

	allocated_size = total_size / int64(coroutine) //每个协程要传输的文件大小

	fmt.Printf("文件总大小: %d, 每个协程分配的文件大小: %d\n", total_size, allocated_size)

	starttime := time.Now().Unix() //时间戳格式
	//对待发送文件进行拆分计算并调用发送方法
	ch := make(chan string)
	var start_pos int64 = 0
	for coroutine_num := 0; coroutine_num < coroutine; coroutine_num++ {
		//server_addr: 远端地址
		//ch: 管道, 用于同步协程
		//coroutine_num: 协程序号
		//bufsize: socket单次发送数据块的大小
		//file_name: 客户端上传文件的名字
		//merge_file_name: 服务端重命名文件名称
		//start_pos: 当前协程开始的位置, 每次启动一个新的协程后, start的指针会向后移动
		//start+littleSize当前协程的结束位置, 如果是最后一个协程的话就把结束位置置为文件的最后, 也就是size
		if coroutine_num == coroutine-1 {
			go sendFile(server_addr, ch, coroutine_num, bufsize, file_name, merge_file_name, start_pos, total_size)
			fmt.Println(start_pos, total_size, bufsize)
		} else {
			go sendFile(server_addr, ch, coroutine_num, bufsize, file_name, merge_file_name, start_pos, start_pos+allocated_size)
			fmt.Println(start_pos, start_pos+allocated_size)
		}

		start_pos += allocated_size
	}

	//同步等待发送文件的协程
	for j := 0; j < coroutine; j++ {
		fmt.Println(<-ch)
	}

	midtime := time.Now().Unix()
	sendtime := midtime - starttime
	fmt.Printf("发送耗时: %d 秒\n", sendtime)

	sendMergeCommand(server_addr, merge_file_name, coroutine) //发送文件合并指令及文件名

	endtime := time.Now().Unix()
	mergetime := endtime - midtime
	fmt.Printf("合并耗时: %d 秒\n", mergetime)

	tot := endtime - starttime
	fmt.Printf("总计耗时：%d 分 %d 秒 \n", tot/60, tot%60)

}

func sendFile(server_addr string, c chan string, coroutineNum int, size int, fileName, mergeFileName string, start int64, end int64) {

	con, err := net.Dial("tcp", server_addr)
	if err != nil {
		fmt.Println("服务器连接失败!")
		os.Exit(-1)
	}
	defer con.Close()
	fmt.Println(coroutineNum, "连接已建立.文件发送中...")

	var by [1]byte
	by[0] = byte(coroutineNum)
	var bys []byte
	databuf := bytes.NewBuffer(bys) //数据缓冲变量
	databuf.Write(by[:])
	databuf.WriteString(mergeFileName)
	bb := databuf.Bytes()
	// bb := by[:]
	// fmt.Println(bb)
	in, err := con.Write(bb) //向服务器发送当前协程的顺序，代表拆分文件的顺序, 以及待合并的文件名称
	if err != nil {
		fmt.Printf("向服务器发送数据错误: %d\n", in)
		os.Exit(-1)
	}

	var msg = make([]byte, 1024)  //创建读取服务端信息的切片
	lengthh, err := con.Read(msg) //确认服务器已收到顺序数据
	if err != nil {
		fmt.Printf("读取服务器数据错误.\n", lengthh)
		os.Exit(-1)
	}
	str := string(msg[0:lengthh])
	fmt.Println("服务端收到顺序号回应: ", str)

	//打开待发送文件，准备发送文件数据
	file, err := os.OpenFile(fileName, os.O_RDWR, 0666)
	if err != nil {
		fmt.Println(fileName, "-文件打开错误.")
		os.Exit(-1)
	}
	defer file.Close()

	file.Seek(start, 0) //设定读取文件的位置, 第二个参数0表示start是相对于文件开头的位置

	buf := make([]byte, size) //创建用于保存读取文件数据的切片, size就是buffsize

	var sendDtaTolNum int = 0 //记录发送成功的数据量（Byte）
	//读取并发送数据
	for i := start; int64(i) < end; i += int64(size) {
		length, err := file.Read(buf) //读取数据到切片中
		if err != nil {
			fmt.Println("读文件错误", i, coroutineNum, end)
			os.Exit(-1)
		}

		//判断读取的数据长度与切片的长度是否相等，如果不相等，表明文件读取已到末尾
		if length == size {
			//判断此次读取的数据是否在当前协程读取的数据范围内，如果超出，则去除多余数据，否则全部发送
			if int64(i)+int64(size) >= end {
				sendDataNum, err := con.Write(buf[:size-int((int64(i)+int64(size)-end))])
				if err != nil {
					fmt.Printf("向服务器发送数据错误: %d\n", sendDataNum)
					os.Exit(0)
				}
				sendDtaTolNum += sendDataNum
			} else {
				sendDataNum, err := con.Write(buf)
				if err != nil {
					fmt.Printf("向服务器发送数据错误: %d\n", sendDataNum)
					os.Exit(0)
				}
				sendDtaTolNum += sendDataNum
			}

		} else {
			//这种情况发生在最后一个协程读取最后一个数据块的时候, 因为没有buffersize大, 所以会出现读取的长度小于buffersize
			//这时候把这个数据块的所有内容发给服务端即可
			sendDataNum, err := con.Write(buf[:length])
			if err != nil {
				fmt.Printf("向服务器发送数据错误: %d\n", sendDataNum)
				os.Exit(-1)
			}
			sendDtaTolNum += sendDataNum
		}

		//读取服务器端信息，确认服务端已接收数据
		lengths, err := con.Read(msg)
		if err != nil {
			fmt.Printf("读取服务器数据错误.\n", lengths)
			os.Exit(-1)
		}
		//str := string(msg[0:lengths])
		//fmt.Println("服务端收到数据块后回信息: ", str)

	}

	fmt.Println(coroutineNum, "发送数据(Byte): ", sendDtaTolNum)

	c <- strconv.Itoa(coroutineNum) + " 协程退出"
}

func sendMergeCommand(server_addr, mergeFileName string, coroutine int) {

	con, err := net.Dial("tcp", server_addr)
	if err != nil {
		fmt.Println("服务器连接失败!")
		os.Exit(-1)
		return
	}
	defer con.Close()
	fmt.Println("连接已建立. 发送合并指令.\n文件合并中...")

	var by [1]byte
	by[0] = byte(coroutine)
	var bys []byte
	databuf := bytes.NewBuffer(bys) //数据缓冲变量
	databuf.WriteString("fileover")
	databuf.Write(by[:])
	databuf.WriteString(mergeFileName)
	cmm := databuf.Bytes()

	in, err := con.Write(cmm)
	if err != nil {
		fmt.Printf("向服务器发送数据错误: %d\n", in)
	}

	var msg = make([]byte, 1024)
	lengthh, err := con.Read(msg)
	if err != nil {
		fmt.Printf("读取服务器数据错误.\n", lengthh)
		os.Exit(0)
	}
	str := string(msg[0:lengthh])
	fmt.Println("传输完成（服务端信息）： ", str)
}
