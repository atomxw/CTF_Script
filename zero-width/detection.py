import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
args  = parser.parse_args()

if __name__ == '__main__':
    file_path = os.path.abspath(args.f)

    with open(file_path, "r", encoding='utf-8') as f:
        data = f.read()

    AllChars = {'\u200a', '\u200b', '\u200c', '\u200d', '\u200e', '\u200f', '\u202a', '\u202c', '\u202d', '\u2062', '\u2063', '\ufeff'}
    Chars = sorted(set(data) & AllChars)
    print(Chars)
    os.system('pause')