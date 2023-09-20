import sys
import os
from lz4 import block # 自行通过pip安装

file = sys.argv[1]
if os.path.exists(file):
    with open(file, "rb") as f:
        data = f.read()[8:]
        out = block.decompress(data)
        with open(file + ".json", "wb") as f:
            f.write(out)
else:
    print("File not found")
