import os
import mmap
import chardet
import argparse
import threading
import multiprocessing as mp
from AESTool import AesCipher


def read_large_file(file_path):
    # 使用mmap映射文件
    with open(file_path, "r+b") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            while True:
                yield mm.readline().rstrip(b"\r\n")
                if mm.tell() == len(mm):
                    break
    
def producer(dic_path, queue, thread_num):
    for password in read_large_file(dic_path):
        queue.put(password)
    
    for _ in range(thread_num):
        queue.put(None)    

def consumer(enc, queue_password, f, version):
    while True:
        pwd = queue_password.get()
        if pwd is None:
            return

        aes = AesCipher(key=pwd, version=version)
        if (dec := aes.decrypt(enc)):
            if (result := chardet.detect(dec)) and result["encoding"] in ["GB2312", "UTF-16", "utf-8", "UTF-8-SIG", "ascii"] and result["confidence"] > 0.8:
                message = f"Find Password: {pwd.decode()}, AES key: {aes.key.decode()}, Message: {str(dec)}" + "\n"
                f.write(message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, default=None, required=True,
                        help='输入字典的文件名称')
    parser.add_argument('-v', type=int, default=3,
                        help='输入冰蝎子流量版本')
    parser.add_argument('-p', type=int, default=mp.cpu_count(),
                        help='输入多线程数')
    args = parser.parse_args()

    dic_path = os.path.abspath(args.d)
    thread_num = args.p
    version = args.v
    
    manager = mp.Manager()
    queue_password = mp.Queue()
    t = threading.Thread(target=producer, args=(dic_path, queue_password, thread_num))
    t.start()

    # enc = AesCipher.decodeBase64("TyXq0tb3mQYD6Ch0FMHJpgsBLOdQsSiFwdEtJEKUEwl4MMV404ZdswnxNWB966ma")
    enc = AesCipher.decodeBase64("qPm3sf5ED5vjWYAJhpDBu9LXU7LgIuNSXa1TLo+aWXjp9SpHbDQJqTuJXlaW2NWG")
    
    with open("output.txt", "w", encoding='utf-8') as f:
        threads = []
        for _ in range(thread_num):
            t = threading.Thread(target=consumer, args=(enc, queue_password, f, version))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()