import os
import time
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-f', type=str, default=None, required=True,
                    help='输入RAR文件路径')
args  = parser.parse_args()

RarBlockType = {
    114: "MARKER",
    115: "ARCHIVE",
    116: "FILE_OR_DIR",
    117: "COMMENT_OLD",
    118: "AV_OLD_1",
    119: "SUBBLOCK_OLD",
    120: "RR_OLD",
    121: "AV_OLD_2",
    122: "SUBBLOCK",
    123: "_END_"
}

RarHead = bytes.fromhex("52 61 72 21 1A 07 00".replace(" ", ""))
RarTail = bytes.fromhex("C4 3D 7B 00 40 07 00".replace(" ", ""))

def repair(pos, answer, FileName=None):
    output = f"[+] 字节地址: {pos}, "
    rarBlockType = data[pos]

    if not FileName:
        if rarBlockType == answer:
            output += f"{RarBlockType[answer]} 结构正确!"
        else:
            data[pos] = answer
            output += f"修复前: {RarBlockType[rarBlockType]}, 修复后: {RarBlockType[answer]}"
    else:
        if rarBlockType == answer:
            output += f"文件名: {bytes(FileName)}, {RarBlockType[answer]} 结构正确, "
        else:
            data[pos] = answer
            output += f"文件名: {bytes(FileName)}, 修复前: {RarBlockType[rarBlockType]}, 修复后: {RarBlockType[answer]}, "
        
        # 判断是否为伪加密
        if data[FileHeadFlags_Pos] >> 2 & 1:
            data[FileHeadFlags_Pos] = data[FileHeadFlags_Pos] & 0b11111011
            output = f"{output}可能存在伪加密已经修复!"
        else:
            output = f"{output}不存在伪加密!"
    print(output)
if __name__ == '__main__':
    filePath = os.path.abspath(args.f)
    baseDir = os.path.dirname(filePath)
    fileSuffix, ext = os.path.splitext(filePath)
    fileName = fileSuffix.split("\\")[-1]

    with open(filePath, "rb") as f:
        data = bytearray(f.read())

    if data[:7] == RarHead:
        print("[+] Rar文件头正确!")
    else:
        data[:7] = RarHead
        print("[-] Rar文件头修复完毕!")

    repair(0x9, 115)

    count = 1
    crc_Pos = 0x14
    while crc_Pos < len(data):
        RarBlockType_Pos = crc_Pos + 2
        FileHeadFlags_Pos = RarBlockType_Pos + 1

        if data[crc_Pos:crc_Pos+7] == RarTail:
            repair(RarBlockType_Pos, 123)
            break

        # 处理reverse字段的存在
        if not RarBlockType.get(data[RarBlockType_Pos]):
            RarBlockType_Pos = RarBlockType_Pos - 5
        
        # 获取文件大小
        RawDataSize_Pos = RarBlockType_Pos + 5
        File_RawDataSize = int.from_bytes(data[RawDataSize_Pos:RawDataSize_Pos+4], byteorder="little", signed=False)

        # 获取文件名长度
        NameSize_Pos = RawDataSize_Pos + 0x13
        File_NameSize = int.from_bytes(data[NameSize_Pos:NameSize_Pos+2], byteorder="little", signed=False)

        # 获取文件名
        FileName_Pos = NameSize_Pos + 6
        FileName = data[FileName_Pos:FileName_Pos+File_NameSize]
        repair(RarBlockType_Pos, 116, FileName)

        crc_Pos = FileName_Pos + File_NameSize + 5 + File_RawDataSize
        count += 1

    saveFileName = os.path.join(baseDir, f"fix_{fileName}{ext}") 
    with open(saveFileName, "wb") as f:
        f.write(data)
        print("[+] 修复完毕, 已经为您保存至同级目录中, 切记使用WinRar打开!(该软件对Rar格式支持性较好)")
    
    time.sleep(0.5)