import os
import math
import argparse
import numpy as np
from PIL import Image


parser = argparse.ArgumentParser()
parser.add_argument("-f", type=str, default=None, required=True,
                    help="输入同级目录下图片的名称")
args  = parser.parse_args()

SAVE_DIR = os.getcwd()

def save_img(data, width=None, height=None, sqrt_num=None):
    with open(os.path.join(SAVE_DIR, "width.bmp"), "wb") as f:
        f.write(data[:0x12] + width.to_bytes(4, byteorder="little", signed=False) + data[0x16:])

    with open(os.path.join(SAVE_DIR, "height.bmp"), "wb") as f:
        f.write(data[:0x16] + height.to_bytes(4, byteorder="little", signed=False) + data[0x1a:])

    with open(os.path.join(SAVE_DIR, "sqrt.bmp"), "wb") as f:
        f.write(data[:0x12] + sqrt_num.to_bytes(4, byteorder="little", signed=False) * 2 + data[0x1a:])


if __name__ == '__main__':
    file_path = os.path.abspath(args.f) 

    img = Image.open(file_path).convert('RGB')
    img = np.array(img, dtype=np.uint8)
    assert img.shape[-1] == 3

    size = os.path.getsize(file_path)
    row, col = img.shape[:2]
    width = (size - 53) // 3 // row
    height = (size - 53) // 3 // col
    sqrt_num = int(math.sqrt((size - 53) // 3))

    print(f"1.宽度可能为: {width}")
    print(f"2.高度可能为: {height}")
    print(f"3.宽度和高度可能为: {sqrt_num}")

    with open(file_path, "rb") as f:
        data = f.read()
    save_img(data, width=width, height=height, sqrt_num=sqrt_num)