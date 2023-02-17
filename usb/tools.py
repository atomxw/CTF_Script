import os
import pyshark
import subprocess


maximum = 0.8 # 流量小于0.8MB才会自动读取流量大小
filters = ["usb.capdata", "usbhid.data"]

def get_input():
    while True:
        if (tmp := input("[+]: 请选择数据类型(1.usb.capdata 2.usbhid.data 3.回车默认): ")) in ["1", "2"]:
            return int(tmp)
        elif tmp == "":
            return None

def get_select(file_path):
    select = 1
    if (size:= round(os.path.getsize(file_path) / (1024 * 1024), 2)) < maximum:

        lengths = []
        for filter in filters:
            cap = pyshark.FileCapture(file_path, display_filter=filter)
            cap.load_packets()
            lengths.append(len(cap))

        if lengths[0] >= lengths[1]:
            print(f"[-]: usb.size: {size}(MB), usb.capdata: {lengths[0]}, usbhid.data: {lengths[1]}, 默认读取: {filters[0]}")
            select = 1
        else:
            print(f"[-]: usb.size: {size}, usb.capdata: {lengths[0]}, usbhid.data: {lengths[1]}, 默认读取: {filters[1]}")
            select = 2

    if (tmp := get_input()) is not None:
        select = tmp
    return select

def get_data(file_path):
    select = get_select(file_path)
    command = f'tshark -r {file_path} -Y {filters[select-1]} -T fields -e {filters[select-1]}'
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.stdout.read().decode("gbk").splitlines()

if __name__ == '__main__':
    get_data("usb.pcapng")