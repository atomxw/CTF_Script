function encode(text, wm) {
    let wm_bin = str2bin(wm);
    wm_bin += " ";
    console.log(wm_bin);
    return embed(text, wm_bin);
}

function str2bin(str) {
    let result = [];
    let list = str.split("");
    for (let i = 0; i < list.length; i++) {
        if (i != 0) {
            result.push(" ");
        }
        let item = list[i];
        let binaryStr = item.charCodeAt().toString(2);
        result.push(binaryStr);
    }
    return result.join("");
}

function bin2str(str) {
    let result = [];
    let list = str.split(" ");
    for (let i = 0; i < list.length; i++) {
        let item = list[i];
        let asciiCode = parseInt(item, 2);
        let charValue = String.fromCharCode(asciiCode);
        result.push(charValue);
    }
    return result.join("");
}

function embed(text, wm_bin) {
    let len_bin_wm = wm_bin.length;
    let len_text = text.length;
    if (len_bin_wm > len_text) {
        return "密文需要明文长度为" + len_bin_wm + "，不符合要求。";
    }


    let text_embed = "";
    for (let idx = 0; idx < len_text; idx++) {
        text_embed += text[idx];
        if (wm_bin[idx] === "1") {
            text_embed += String.fromCharCode(127);
        } else if (wm_bin[idx] === " ") {
            text_embed += String.fromCharCode(127);
            text_embed += String.fromCharCode(127);
        }
    }
    return text_embed;
}

function extract(text_embed) {
    let bin_wm_extract = "";
    let idx = 0;
    let previous_is_char = false;
    while (idx < text_embed.length) {
        if (previous_is_char) {
            if (text_embed[idx] === String.fromCharCode(127)) {
                if (text_embed[idx + 1] === String.fromCharCode(127)) {
                    bin_wm_extract += " ";
                    previous_is_char = false;

                    idx++;
                } else {
                    bin_wm_extract += "1";
                    previous_is_char = false;

                }
            } else {
                bin_wm_extract += "0";
                previous_is_char = true;

            }
        } else {
            previous_is_char = true;
        }

        idx++;

    }

    return bin_wm_extract
}


function decode(text_embed) {
    return bin2str(extract(text_embed));
}

// console.log(decode("awjddddddddddddddddddddddddddddd0paojrrrrrrr"))