import os
import re
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
parser.add_argument("-n", type=int, default=2, required=False,
                    help="输入放大的倍数 (默认: 2倍)")
args  = parser.parse_args()


if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    shfflePath, ext = os.path.splitext(filePath)
    shffleName = shfflePath.split("\\")[-1]
    
    with open(filePath, "rb") as f:
        data = bytearray(f.read())
        
    sof_lis = [b"\xff\xc0\x00\x11\x08", b"\xFF\xC2\x00\x11\x08"]

    flag = False
    for sof in sof_lis:
        for iter in re.finditer(re.escape(sof), data):
            flag = True
            height = int.from_bytes(data[iter.end():iter.end()+2], byteorder="big", signed=False)
            data[iter.end():iter.end()+2] = int(height * args.n).to_bytes(2, byteorder="big", signed=False)
        
    if not flag:
        print("没有找到SOFx层!")
        time.sleep(0.5)
        exit(-1)
    else:
        print(f"原始图像高度: {height}, 已经修改为了{args.n}倍!")
        with open("fix_1.jpg", "wb") as f:
            f.write(data)
        time.sleep(0.5)
        exit()