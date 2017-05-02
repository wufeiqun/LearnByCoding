"use strict"
// [123, 456, 789, 123, 456, 789, 123], 3 --> [[123, 456, 789], [123, 456, 789], [123]]
//
//
function separation(arr, len) {
	if (arr.length <= len) {
		return arr;
	} else {
		var newArr = [];
		var quotient = parseInt(arr.length / len); //商
		var remainder = arr.length % len; //余数
		for (let i = 0; i < quotient; i++) {
			newArr.push(arr.slice(len*i, len*i + len));
		}

		if (remainder !== 0) {
			newArr.push(arr.slice(-remainder));
		}

		return newArr;
	}

}

var arr = [123, 456, 789, 123, 456, 789];
var len = 1;
console.log(separation(arr, len));


