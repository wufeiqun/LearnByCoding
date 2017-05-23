"use strict"

var fs = require("fs");
var request = require("request");
var sync_request = require("sync-request");
var cheerio = require("cheerio");
var iconv = require('iconv-lite');


var VHao = {
	initURL: "http://www.6vhao.com/s/xiju/",
	fileName: "6vhao.txt",
	getAllPages: function() {
		var linksArray = [];
		var res = sync_request("GET", this.initURL);
		var html = iconv.decode(res.getBody(), "gb2312");
		var $ = cheerio.load(html);
		var select = $("#main > div.col4 > div > div:nth-child(2) > select")[0].children;
		for(let i = 0, len = select.length; i < len; i++) {
			linksArray.push(select[i].attribs.value);
		}
		return linksArray;
	},
	getDetailPage: function(url){
		//If null, the body is returned as a Buffer. 
		request({"encoding": null, "url": url}, function(error, response, body) {
			//Buffer to JS string
			var html = iconv.decode(body, "gb2312");
			var $ = cheerio.load(html);
			$(".list > li").each(function(index, element) {
				var item = element.children[1];
				var movieName = VHao.getMovieName(item); //这里不能使用this,因为this指向element
				var movieURL = item.attribs.href;
				VHao.getDownloadLink(movieURL, movieName);
			})
			
		})
	},
	getDownloadLink: function(url, name) {
		request({"encoding": null, "url": url}, function(error, response, body) {
			var html = iconv.decode(body, "gb2312");
			var $ = cheerio.load(html);
            console.log(url);
			$("#endText table tbody").each(function(index, element){
				//只获取第一个下载链接,一般为迅雷下载链接
				//var downLink = element.children[1].children[1].children[0].attribs.href;
				console.log(element.children[1].children[1].children)
				// fs.appendFile(this.fileName, name + " ---------> " + downLink + "\r\n", function(error) {
				// 	if (error) {
				// 		console.log(error);
				// 	}
				// })
			})
		})
	},
	getMovieName: function(item) {
		if (item.children[0].hasOwnProperty("data")) {
			return item.children[0].data;
		} else {
			return VHao.getMovieName(item.children[0]);
		}
	},
	start: function() {
		var links = this.getAllPages();
		for(let i = 0; i < links.length; i++) {
			this.getDetailPage(links[i]);
		}
	}
};

//VHao.start();
// VHao.getDetailPage("http://www.6vhao.com/s/xiju/index_16.html");
VHao.getDownloadLink("http://www.6vhao.com/dy/2017-05-21/ManHaoZhenTan.html", "xx");
VHao.getDownloadLink("http://www.6vhao.com/gq/2017-02-28/WoQuNaEr.html", "xx");
