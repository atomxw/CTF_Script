import os
import re
import argparse
from rich.table import Table
from rich.console import Console


console = Console()
table = Table(show_header=True, header_style="bold")
table.add_column("节选HEX")
table.add_column("文件名")
table.add_column("可能使用的压缩工具")
table.add_column("是否存在伪加密")

def icon():
    console.print(r"""
   ___                 ___  ___ _        ____     __         ____                       __  _         
  / _ )__ ____ __ ___ |_  |/ _ ( )___   / __/__ _/ /_____   / __/__  __________ _____  / /_(_)__  ___ 
 / _  / // /\ \ /(_-</ __// // //(_-<  / _// _ `/  '_/ -_) / _// _ \/ __/ __/ // / _ \/ __/ / _ \/ _ \
/____/\_, //_\_\/___/____/\___/ /___/ /_/  \_,_/_/\_\\__/ /___/_//_/\__/_/  \_, / .__/\__/_/\___/_//_/
     /___/                                                                 /___/_/                              
""")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, default=None, required=True,
                        help="输入Zip文件")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    filePath = os.path.abspath(args.f)
    fileName = filePath.split('\\')[-1]
    fileDir = os.path.dirname(filePath)

    ZIP_DIR_ENTRY_Signature = bytes.fromhex('504b0102')

    VersionMade = {
        20: "Bandizip/Windows自带压缩工具",
        31: "WinRAR",
        63: "7-Zip",
    }

    with open(filePath, "rb") as f:
        data = bytearray(f.read())

    num = 0
    flag = False
    for VersionMadeBy, value in VersionMade.items():
        findByte = b"\x50\x4b\x01\x02" + re.escape(VersionMadeBy.to_bytes(2, byteorder="little", signed=False))
        for iter in re.finditer(findByte, data):
            pos = iter.end() + 2
            print(pos)
            FileNameLengthPos = pos + 20
            FileNameLength = int.from_bytes(data[FileNameLengthPos:FileNameLengthPos+2], byteorder="little", signed=False)
            FileNamePos = FileNameLengthPos + 18
            FileName = data[FileNamePos:FileNamePos+FileNameLength]
            
            hexStr1 = ' '.join(re.findall(".{2}", data[iter.start():iter.start()+8].hex().upper()))
            hexStr2 = ' '.join(re.findall(".{2}", data[iter.start()+8:iter.start()+10].hex().upper()))
            
            if int.from_bytes(data[pos:pos+2], byteorder="little", signed=False)  % 2 != 0:
                data[pos:pos+2] = b"\x00\x00"
                table.add_row(
                    f"[green]{bytes(FileName)}[/green]",
                    f"[purple]{hexStr1}[/purple] [red]{hexStr2}[/red]",
                    f"[blue]{value}[/blue]",
                    "[red]可能存在伪加密![/red]"
                )
                flag = True
                num += 1
            else:
                table.add_row(
                    f"[green]{bytes(FileName)}[/green]",
                    f"[purple]{hexStr1}[/purple] [green]{hexStr2}[/green]",
                    f"[blue]{value}[/blue]",
                    "不存在伪加密!"
                )

    icon()
    console.print(table)
    if flag:
        console.print(f"[+] 已经帮您修改 {num} 个伪加密文件, 已经帮您保存到文件所在目录!")
        with open(os.path.join(fileDir, f"fix_{fileName}"), "wb") as f:
            f.write(data)
    else:
        print("[+] 不存在加密, 无需保存文件!")