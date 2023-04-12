import io
import zipfile

with open("flag1", "rb") as f:
    data = f.read()[::-1]

all_files_processed = False  # 初始化标志变量


while True:
    with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
        for i in zf.filelist:
            if zipfile.is_zipfile(io.BytesIO(zf.read(i.filename)[::-1])):
                data = zf.read(i.filename)[::-1]
                print(i.filename)
            else:
                all_files_processed = True
                with open(i.filename, "wb") as f:
                    f.write(zf.read(i.filename))

        if all_files_processed:
            break