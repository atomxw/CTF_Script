package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"hash/crc32"
	"io"
	"os"
	"path/filepath"
	"time"
)

var dirPath string
var start time.Time

func calculation_crc32(data []byte, width int, height int) uint32 {
    crc32 := crc32.NewIEEE()
    crc32.Write(data[12:16])
    binary.Write(crc32, binary.BigEndian, int32(width))
    binary.Write(crc32, binary.BigEndian, int32(height))
    crc32.Write(data[24:29])
    return crc32.Sum32()
}

func save_png(data []byte, width int, height int, original_crc32 uint32, PNG_NAME string) {
    var buf bytes.Buffer
    buf.Write(data[:16])
    binary.Write(&buf, binary.BigEndian, int32(width))
    binary.Write(&buf, binary.BigEndian, int32(height))
    buf.Write(data[24:])
    err := os.WriteFile(filepath.Join(dirPath, fmt.Sprintf("fix_%s", PNG_NAME)), buf.Bytes(), 0644)
    if err != nil {
        fmt.Println("[-] 保存文件失败")
        fmt.Println(err) // 打印错误信息
        os.Exit(-1)
    }
    end := time.Now()
    duration := end.Sub(start)
    hours := int(duration.Hours())
    minutes := int(duration.Minutes()) % 60
    seconds := int(duration.Seconds()) % 60
    milliseconds := int(duration.Milliseconds()) % 1000
    fmt.Printf("[-] 宽度: %d, hex: %x\n", width, width)
    fmt.Printf("[-] 高度: %d, hex: %x\n", height, height)
    fmt.Printf("[-] 运行时间为：%d小时 %d分钟 %d秒 %d毫秒\n", hours, minutes, seconds, milliseconds)
    fmt.Printf("[-] CRC32: %x, 已经为您保存到运行目录中!", original_crc32)
    os.Exit(0)
}

func main() {
    args := os.Args
    if len(args) < 2 {
        fmt.Println("[-] 请输入图片路径")
        os.Exit(-1)
    }
	
	filePath, err := filepath.Abs(args[1])
    if err != nil {
        fmt.Printf("获取文件绝对路径失败：%v\n", err)
        return
    }

    fileName := filepath.Base(filePath)
    dirPath = filepath.Dir(filePath)

    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("[-] 读取文件失败")
        fmt.Println(err) // 打印错误信息
        os.Exit(-1)
    }
    defer file.Close()

    data, err := io.ReadAll(file)
    if err != nil {
        fmt.Println("[-] 读取文件失败")
        os.Exit(-1)
    }
    // crc32key := calculation_crc32(data, int(binary.BigEndian.Uint32(data[0x10:0x14])), int(binary.BigEndian.Uint32(data[0x14:0x18])))
    original_crc32 := binary.BigEndian.Uint32(data[29:33])

    if filepath.Ext(fileName) != ".png" {
        fmt.Println("[-] 您的文件后缀名不为PNG!")
        os.Exit(-1)
    }

    start = time.Now()
    fmt.Println("[-] 爆破高度中...")
    for height := 0; height < 0x1FFF; height++ {
        if calculation_crc32(data, int(binary.BigEndian.Uint32(data[0x10:0x14])), height) == original_crc32 {
            save_png(data, int(binary.BigEndian.Uint32(data[0x10:0x14])), height, original_crc32, fileName)
        }
    }

    fmt.Println("[-] 爆破宽度中...")
    for width := 0; width < 0x1FFF; width++ {
        if calculation_crc32(data, width, int(binary.BigEndian.Uint32(data[0x14:0x18]))) == original_crc32 {
            save_png(data, width, int(binary.BigEndian.Uint32(data[0x14:0x18])), original_crc32, fileName)
        }
    }
	
    fmt.Println("[-] 爆破宽度和高度中...")
    for width := 0; width < 0x1FFF; width++ {
        for height := 0; height < 0x1FFF; height++ {
            if calculation_crc32(data, width, height) == original_crc32 {
                save_png(data, width, height, original_crc32, fileName)
            }
        }
    }
}
