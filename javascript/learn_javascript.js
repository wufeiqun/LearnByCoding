//给定一个字符串,求出这个字符串中出现频率最高的那个字符以及次数;
function word_max_count(word) {
    var obj = {};
    var arr = [];

    for (let i=0; i<word.length; i++) {
        if (word[i] in obj) {
            obj[word[i]] += 1;
        } else {
            obj[word[i]] = 1;
        }
    }
    
    for (let key in obj) {
        arr.push([key, obj[key]]) ;   
    }

    arr.sort(function(x, y) {return y[1] - x[1]})
    console.log(arr[0]);
    return arr[0];

}

var word = "abcdfdfddddhghhjfddddddd";
word_max_count(word)

//数组的复制和引用
var arr = ["a", "b", "c"];
var a = arr;
var b = arr.slice();
arr.push("d")
console.log(arr);
console.log(a);
console.log(b);

//使用Array的内置方法遍历数组
var arr = ["a", "b", "c"];
arr.forEach(function (item, index, array) {
    console.log(item, index)
})
