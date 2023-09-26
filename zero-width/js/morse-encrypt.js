// import { incode, decode } from './encrypt';
// import { unicodeSsplit } from "./morse";

/*
    @param {String} str 待加密文本
    @param {String} textBefore 前段明文
    @param {String} textAfter 后段明文
*/

const morseWords = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..']
const morseNumber = ['-----', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.']

let wordsToMorse = {};
let morseToWords = {};

let morseToNum = {};

//a-z数组
let words = [];
for (let i = 10; i < 36; i++) {
  let j = i.toString(36);
  words.push(j);
}

//数字加密字典
let numToMorse = morseNumber;


//字母加密字典
for (let i in words) {
  wordsToMorse[words[i]] = morseWords[i];
}
//字母解密字典
for (let i in wordsToMorse) {
  morseToWords[wordsToMorse[i]] = i;
}
//数字解密字典
for (let i in morseNumber) {
  morseToNum[morseNumber[i]] = i;
}
//合并字典
let decodeWords = Object.assign(morseToWords, morseToNum);
/* 附件字符 */
const unicodeSsplit = "|/|"; //unicode 分割符
decodeWords['-...-'] = ' ';
decodeWords[".--.-"] = "\\";
decodeWords[".--.."] = unicodeSsplit;
wordsToMorse["\\"] = ".--.-";
wordsToMorse[unicodeSsplit] = ".--..";

function incode(str = '', textBefore = '', textAfter = '') {
  if (typeof str !== 'string' || str.length === 0) {
    return
  }
  let res = [];
  let l = "&#8205;";
  let s = "&#8204;";
  let q = "&#8203;";
  for (let i in str) {
    let val = str[i];
    if (val === ' ') {
      res.push('-...-')
    } else if (val === '|') {
      res.push('.--..')
    } else if (!!parseInt(val) || parseInt(val) == 0) {
      res.push(numToMorse[str[i]]);
    } else {
      res.push(wordsToMorse[str[i]]);
    }
  }
  let encrypt = res.join("/");
  encrypt = encrypt.replace(/\//g, q)
  encrypt = encrypt.replace(/\./g, s)
  encrypt = encrypt.replace(/\-/g, l)
  return textBefore + encrypt + textAfter;
}
/* 
  @param {String} text 待解密字符串
*/
function decode(text) {
  if (typeof text !== 'string' || text.length === 0) {
    return
  }
  let decode = [];
  text.match(/(\&\#8203\;|\&\#8204\;|\&\#8205\;|\u200B|\u200C|\u200D|\&zwnj\;|\&zwj\;)+/g).map(temp => {
    temp = temp.replace(/\&\#8203\;|\u200B/g, "|");
    temp = temp.replace(/\&\#8204\;|\u200C|\&zwnj\;/g, ".");
    temp = temp.replace(/\&\#8205\;|\u200D|\&zwj\;/g, "-");
    let arr = temp.split("|");
    for (let i in arr) {
      decode.push(decodeWords[arr[i]]);
    }
  })
  return decode;
}

// from http://www.atoolbox.net/Tool.php?Id=829
function handleDecode(ciphertext) {
  let code = decode(ciphertext);
  let outcodes = code.join('');
  // console.log(code, outcodes);

  outcodes = outcodes.replace(/\\u[0-9a-z]{4}/g, (t) => {

      return String.fromCharCode(parseInt(t.replace('\\u', ''), 16))
  })
  return outcodes
}

function incodeByUnicode(str = '', textBefore = '', textAfter = '') {
  const unicodeArr = [];
  let unicodeStr = '';
  // unicode 转码
  for (let i = 0; i < str.length; i++) {
    unicodeArr.push(str.charCodeAt(i).toString(36));
  }
  unicodeStr = unicodeArr.join(unicodeSsplit) + unicodeSsplit;
  // 零宽转码
  const ciphertext = incode(unicodeStr);
  return textBefore + ciphertext + textAfter;
}
/*
  @param {String} str 待解密字符串
*/
function decodeByUnicode(str) {
  const plaintextArr = decode(str);
  let plaintext = '';
  let unicodeText = '';
  // 零宽逆转码
  plaintextArr.map(val => {
    if (val) {
      unicodeText += val;
    } else {
      unicodeText += unicodeSsplit;
    }
  });
  // unicode 逆转码
  unicodeText.split(unicodeSsplit).forEach(val => {
    if (!val || val.length === 0) {
      return;
    }
    let textNum = parseInt(val, 36);
    plaintext += String.fromCharCode(textNum);
  });
  return plaintext;
}

// let ciphertext = "flag‌‌‍‍‍​‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌‍‍​‍‍‍‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‍‍‌​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌‍‍​‍‍‍‌‌​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‍‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌‍‍​‍‍‌‌‌​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‍‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌‍‍​‍‍‌‌‌​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌‍‍​‍‍‍‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‍‍‌​‌‍‍‌‌​​‌‍‍‌‌​‌‌‍‍‍​‌‌‌‍​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍‍​‍‍‌‌​‌‍‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‍‍‍​‍‌‍​‌‍‍‍‍​‌‍‍‌‌​​‌‍‍‌‌​‍‍‌​‌‌‍‍‍​‌‍‍​‌‍‍‌‌​​‌‍‍‌‌​‌‌‌​‍‍​‍‍‌​‌‍‍‌‌​​‌‍‍‌‌​‌‌​‌‍‍‍‍​‌‍‍‍​‌‍‍‌‌​​‌‍‍‌‌​‍‍‍​‍‌‌‌​‍‍‌‍​‌‍‍‌‌​​‌‍‍‌‌is not here!";
// console.log(handleDecode(ciphertext));
// console.log(decodeByUnicode(ciphertext));
