from main import UnicodeSteganography


if __name__ == '__main__':
    with open("./js/unicode_steganography.js", "rb") as f:
        unicodeSteganography = UnicodeSteganography(f.read())
        
    with open('./demo/Binary/Binary.txt', "r", encoding="utf-8") as f:
        cipher_text1 = f.read()
        print(unicodeSteganography.decodeBinary(cipher_text1))
    
    with open("./demo/Text/text2.txt", "r", encoding="utf-8") as f:
        cipher_text2 = f.read()
        print(unicodeSteganography.decodeText(cipher_text2))
    