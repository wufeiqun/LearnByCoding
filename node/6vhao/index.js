"use strict"

var fs = require("fs");
var request = require("request");
var sync_request = require("sync-request");
var cheerio = require("cheerio");
var iconv = require('iconv-lite');


var VHao = {
	initURL: "http://www.6vhao.com/s/xiju/",
	fileName: "/tmp/6vhao.txt",
    errorFileName: "/tmp/error.txt",
    timeout: 100 * 1000,
	getAllPages: function() {
		var linksArray = [];
		var res = sync_request("GET", this.initURL, {"timeout": VHao.timeout});
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
		request({"encoding": null, "url": url, "timeout": VHao.timeout}, function(error, response, body) {
            if (!error && response.statusCode == 200) {
			    //Buffer to JS string
			    var html = iconv.decode(body, "gb2312");
			    var $ = cheerio.load(html);
			    $(".list > li").each(function(index, element) {
			    	var item = element.children[1];
			    	var movieName = VHao.getMovieName(item); //这里不能使用this,因为this指向element
			    	var movieURL = item.attribs.href;
			    	VHao.getDownloadLink(movieURL, movieName);
			    })
            } else {
                console.log(error);
            }
		})
	},
	getDownloadLink: function(url, name) {
		request({"encoding": null, "url": url, "timeout": VHao.timeout}, function(error, response, body) {
            if (!error && response.statusCode == 200) {
			    var html = iconv.decode(body, "gb2312");
			    var $ = cheerio.load(html);
                //console.log($("#endText  table  tbody tr")[0].children[1].children);
                try {
                    var downDomTree = $("#endText  table  tbody tr")[0].children[1].children;
		            for(let index = 0; index < downDomTree.length; index++) {
                        if(downDomTree[index].name === "a") {
                            console.log(downDomTree[index].attribs.href);
                            //fs.appendFile(this.errorFileName, name + "\r\n", function(error) {
                            //    if (error) {
                            //        console.log(error);
                            //    }
                            //})
                            break;
                        }
                    }
                
                } catch(e) {
                    fs.appendFile(VHao.errorFileName, name + " ---> " + url + "\r\n", function(error) {
                        if (error) {
                            console.log(error);
                        }
                    })
                }
            } else {
                console.log(error);
            }
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
