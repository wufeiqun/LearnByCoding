//工作中经常遇到求两个相同长度的array的和,比如x = [1,2,3,4], y = [5,6,7,8] ,结果为[6,8,10,12],如果只要一个地方使用的话,用for loop就可以了
//但是多个地方都是用的话,代码看上去就会很冗余,所以就为所有的array添加一个方法.

Array.prototype.SumArray = function(arr) {
    var sum = [];
    if (arr != null && this.length == arr.length) {
        for (let i = 0; i < this.length; i++) {
            sum.push(this[i] + arr[i]);
        }
    }
    return sum;
}

//test
var x = [1,2,3,4];
var y = [5,6,7,8];
var z = x.SumArray(y);
console.log(z);

