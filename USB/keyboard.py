'''
BYTE1 --
       |--bit0:   Left Control是否按下，按下为1 
       |--bit1:   Left Shift  是否按下，按下为1 
       |--bit2:   Left Alt    是否按下，按下为1 
       |--bit3:   Left GUI    是否按下，按下为1 
       |--bit4:   Right Control是否按下，按下为1  
       |--bit5:   Right Shift 是否按下，按下为1 
       |--bit6:   Right Alt   是否按下，按下为1 
       |--bit7:   Right GUI   是否按下，按下为1 
BYTE2 -- 暂不清楚，有的地方说是保留位
BYTE3--BYTE8 -- 这六个为普通按键
from: https://blog.csdn.net/fjh1997/article/details/105841367
'''
import os
import tools
import string
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下的名称")
args = parser.parse_args()

normalKeys = {
    "04": "a", "05": "b", "06": "c", "07": "d", "08": "e",
    "09": "f", "0a": "g", "0b": "h", "0c": "i", "0d": "j",
    "0e": "k", "0f": "l", "10": "m", "11": "n", "12": "o",
    "13": "p", "14": "q", "15": "r", "16": "s", "17": "t",
    "18": "u", "19": "v", "1a": "w", "1b": "x", "1c": "y",
    "1d": "z", "1e": "1", "1f": "2", "20": "3", "21": "4",
    "22": "5", "23": "6", "24": "7", "25": "8", "26": "9",
    "27": "0", "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "<ALT>",
    "2c": "<SPACE>", "2d": "-", "2e": "=", "2f": "[", "30": "]", "31": "\\",
    "32": "<NON>", "33": ";", "34": "'", "35": "<GA>", "36": ",", "37": ".",
    "38": "/", "39": "<CAP>", "3a": "<F1>", "3b": "<F2>", "3c": "<F3>", "3d": "<F4>",
    "3e": "<F5>", "3f": "<F6>", "40": "<F7>", "41": "<F8>", "42": "<F9>", "43": "<F10>",
    "44": "<F11>", "45": "<F12>", "4a": "<HOME>", "4c": "<DELETE>", "4d": "<END>", "4f": "<RightArrow>",
    "50": "<LeftArrow>", "51": "<DownArrow>", "52": "<UpArrow>", "53": "<NumLock>", "54": "/",
    "55": "*", "56": "-", "57": "+", "58": "<RET>", "59": "1", "5a": "2", "5b": "3", "5c": "4", "5d": "5",
    "5e": "6", "5f": "7", "60": "8", "61": "9", "62": "0"}
shiftKeys = {
    "04": "A", "05": "B", "06": "C", "07": "D", "08": "E",
    "09": "F", "0a": "G", "0b": "H", "0c": "I", "0d": "J",
    "0e": "K", "0f": "L", "10": "M", "11": "N", "12": "O",
    "13": "P", "14": "Q", "15": "R", "16": "S", "17": "T",
    "18": "U", "19": "V", "1a": "W", "1b": "X", "1c": "Y",
    "1d": "Z", "1e": "!", "1f": "@", "20": "#", "21": "$",
    "22": "%", "23": "^", "24": "&", "25": "*", "26": "(", "27": ")",
    "28": "<RET>", "29": "<ESC>", "2a": "<DEL>", "2b": "<ALT>","2c": "<SPACE>",
    "2d": "_", "2e": "+", "2f": "{", "30": "}", "31": "|", "32": "<NON>", "33": ":",
    "34": ":", "35": "<GA>", "36": "<", "37": ">", "38": "?", "39": "<CAP>", "3a": "<F1>",
    "3b": "<F2>", "3c": "<F3>", "3d": "<F4>", "3e": "<F5>", "3f": "<F6>", "40": "<F7>",
    "41": "<F8>", "42": "<F9>", "43": "<F10>", "44": "<F11>", "45": "<F12>",
    "4a": "<HOME>", "4c": "<DELETE>", "4d": "<END>", "4f": "<RightArrow>",
    "50": "<LeftArrow>", "51": "<DownArrow>", "52": "<UpArrow>", "53": "<NumLock>", "54": "/",
    "55": "*", "56": "-", "57": "+", "58": "<RET>", "59": "1", "5a": "2", "5b": "3", "5c": "4", "5d": "5",
    "5e": "6", "5f": "7", "60": "8", "61": "9", "62": "0"}


def isShift(shiftNum):
    return shiftNum >> 1 & 1 == 1 or shiftNum >> 5 & 1

def get_info(mode):  # sourcery skip: low-code-quality
    output = []
    capState = False
    for line in data:
        if mode in [1, 2] and len(line) != 16:
            continue
        elif mode in [3] and len(line) != 74:
            continue
        elif mode in [4] and len(line) != 4:
            continue
        
        if mode == 1 and line[4:6] != "00":
            continue
        elif mode == 2 and (line[4:6] == "00" or line[6:8] == "0a" or line[6:8] != "00"):
            # from https://github.com/FzWjScJ/knm
            # if line[0] != '0' or line[1] not in ['0', '2'] or line[2] != '0' or line[3] != '0' or line[6] != '0' or line[7] != '0' or line[8] != '0' or line[9] != '0' or line[10] != '0' or line[11] != '0' or line[12] != '0' or line[13] != '0' or line[14] != '0' or line[15] != '0' or line[4:6] == "00":
            continue
        elif mode == 3 and (line[6:8] == "00" or line[8:10] == "0a"):
            continue
        elif mode == 4 and line[2:3] == "00":
            continue
        
        shiftNum = int(line[:2], 16) if mode in [1, 2, 4] else int(line[2:4], 16)
        if mode in [1, 3]:
            button = line[6:8]
        elif mode == 2:
            button = line[4:6]
        elif mode == 4:
            button = line[2:4]

        # if button == "27":
        #     print(line)
        
        if not normalKeys.get(button):
            continue

        if button == "39":
            capState = not capState

        # capslock这个按键好像只对a-z开启大写
        if capState and shiftKeys[button] in string.ascii_letters:
            output.append(shiftKeys[button])
        elif isShift(shiftNum): 
            output.append(shiftKeys[button])
        else:
            output.append(normalKeys[button])

    return output

def convertSpecialChars(data):
    flag = []
    for i in data:
        if i == "<SPACE>":
            flag.append(" ")
        elif i == "<ALT>":
            flag.append("\t")
        elif i == "<RET>":
            flag.append("\n")
        elif i in ["<DEL>", "<DELETE>"]:
            if flag != []:
                flag.pop(-1)
        elif i != "<CAP>":
            flag.append(i)
    return flag

if __name__ == '__main__':
    filePath = os.path.abspath(args.f)

    if filePath.endswith(".txt"):
        with open(filePath, "r") as f:
            data = f.read().splitlines()
        print("[+] 读取文本成功, 执行USB流量分析...")
    else:
        data = tools.get_data(filePath)

    print("\n模式1:")
    info = get_info(1)
    print(f"\t原始数据: {''.join(info)}")
    print(f"\t正常数据: {''.join(convertSpecialChars(info))}")
    
    print("\n模式2:")
    info = get_info(2)
    print(f"\t原始数据: {''.join(info)}")
    print(f"\t正常数据: {''.join(convertSpecialChars(info))}")
    
    print("\n模式3:")
    info = get_info(3)
    print(f"\t原始数据: {''.join(info)}")
    print(f"\t正常数据: {''.join(convertSpecialChars(info))}")

    print("\n模式4:")
    info = get_info(4)
    print(f"\t原始数据: {''.join(info)}")
    print(f"\t正常数据: {''.join(convertSpecialChars(info))}")

    os.system("pause")