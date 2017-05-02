"use strict"

function divideBythree(intPart) { //typeof intPart string
	var times = intPart.length / 3;
	var arr = [];
	for (let i=0; i<times; i++) {
		arr.push(intPart.slice(3*i, 3*i+3));
	}
	return arr.join(",");
}

function formatNum(num) {
	var num2str = String(num).split(".");
	var intPart = num2str[0];
	var floatPart = num2str[1];
	var newIntPart = '';

	//整数部分和小数部分分开处理
	if (intPart.length <= 3) {
		newIntPart = intPart;
	} else {
		var remainder = intPart.length % 3; //整数部分长度除以3的余数;
		if (remainder === 0) {
			newIntPart = divideBythree(intPart);
		} else {
			var post = intPart.slice(0, remainder); //整数部分从开始取余数位,目的是让剩下的位数为3的倍数
			var rest = intPart.slice(remainder);
			rest = divideBythree(rest);
			newIntPart = post + "," + rest;
		}
	}

	//处理小数部分
	if (floatPart) {
		var result = newIntPart + "." + floatPart;
	} else {
		var result = newIntPart;
	}

	console.log(result);
	return result;
}