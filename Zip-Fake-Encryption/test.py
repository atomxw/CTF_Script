from rich.console import Console
from rich.table import Table

console = Console()

table = Table(show_header=True, header_style="bold")
table.add_column("节选HEX")
table.add_column("文件名")
table.add_column("可能使用的压缩工具")
table.add_column("是否存在伪加密")

data = [
    ["50 4B 01 02 1F 00 14 00 00 00", 'hint.txt', "WinRAR", "不存在伪加密!"],
    ["50 4B 01 02 1F 00 14 00 00 00", 'secret~.txt', "WinRAR", "不存在伪加密!"],
    ["50 4B 01 02 1F 00 14 00 00 00", 'f1ag.png', "WinRAR", "不存在伪加密!"],
    ["50 4B 01 02 1F 00 0A 00 00 00", 'attachment.7z', "WinRAR", "不存在伪加密!"],
    ["50 4B 01 02 1F 00 0A 00 09 00", 'flag.zip', "WinRAR", "可能存在伪加密!"],
]

for row in data:
    hex_value = row[0]
    filename = row[1]
    tool = row[2]
    encryption = row[3]

    table.add_row(hex_value, filename, tool, encryption)

console.print(table)