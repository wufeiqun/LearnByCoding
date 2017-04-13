"use strict"

var xlsx = require('node-xlsx'); //处理Excel的模块
var request = require('sync-request'); //处理HTTP请求的模块, 类似AJAX, 可以发送POST/GET请求
var fs = require('fs'); //读写文件模块, 为了保存新生成的Excel文件

//获取指定电影的百科地址
var get_baike_url = function (name) {
    var url = encodeURI('http://baike.baidu.com/search/word?word=' + name);
    var options = {
        followRedirects: false,
        timeout: 5000,
        retry: true
    }
    resp = request('GET', url, options);
    return resp.headers.location;
}


var excel_file = xlsx.parse('yuhuan.xlsx'); //读取同级目录下的Excel文件

//遍历影视名称, 执行搜索并填写到Excel文件中
for (let i = 0, len = excel_file[0]['data'].length; i < len; i++) {
    
    console.log("正在搜索电影: " + excel_file[0]['data'][i][1]);
    //获取百科地址
    var baike_url = get_baike_url(excel_file[0]['data'][i][1]);
    //把获取的百科地址追加到指定的数组中
    excel_file[0]['data'][i][6] = baike_url;
}

//构建新的Excel文件
var buffer = xlsx.build(excel_file);
//保存新的Excel文件到本地磁盘的当前目录
fs.writeFileSync('yuhuan.xlsx', buffer, {'flag':'w'}); // 如果文件存在，覆盖

