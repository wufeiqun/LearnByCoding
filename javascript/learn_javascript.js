//给定一个字符串,求出这个字符串中出现频率最高的那个字符以及次数;
function word_max_count(word) {
    var obj = {};
    var arr = [];

    for (let key in word) {
        if (word[key] in obj) {
            obj[word[key]] += 1;
        } else {
            obj[word[key]] = 1;
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
