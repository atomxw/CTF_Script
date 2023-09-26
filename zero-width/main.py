import os
import argparse
from rich.console import Console
from py_mini_racer import MiniRacer


console = Console()

def icon():
    console.print(r"""
   ___                 ___  ___ _        ____                  _      ___    ____  __      ______          __  
  / _ )__ ____ __ ___ |_  |/ _ ( )___   /_  / ___ _______  ___| | /| / (_)__/ / /_/ /  ___/_  __/__  ___  / /__
 / _  / // /\ \ /(_-</ __// // //(_-<    / /_/ -_) __/ _ \/___/ |/ |/ / / _  / __/ _ \/___// / / _ \/ _ \/ (_-<
/____/\_, //_\_\/___/____/\___/ /___/   /___/\__/_/  \___/    |__/|__/_/\_,_/\__/_//_/    /_/  \___/\___/_/___/
     /___/                                                                                                               
""")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", type=str, default=None, required=True,
                        help="输入零宽文件")
    return parser.parse_args()

class JSRuntime:
    
    def __init__(self, jsCode) -> None:
        self.crx = MiniRacer() # _get_lib_path 我修改了这个的dll的路径 py_mini_racer.py
        self.crx.eval(jsCode)

class UnicodeSteganography(JSRuntime):
    
    AllChars = {'\u200a', '\u200b', '\u200c', '\u200d', '\u200e', '\u200f', '\u202a', '\u202c', '\u202d', '\u2062', '\u2063', '\ufeff'}
    
    def __init__(self, jsCode) -> None:
        super().__init__(jsCode)

    def getUseChars(self, cipher_text) -> str:
        return ''.join(sorted(set(cipher_text) & self.AllChars))

    def __setChars(self, cipher_text):
        cipher_text = cipher_text
        self.crx.call("unicodeSteganographer.setUseChars", self.getUseChars(cipher_text))

    def decodeText(self, cipher_text) -> dict:
        self.__setChars(cipher_text)
        res = self.crx.call("unicodeSteganographer.decodeText", cipher_text)
        res['hiddenText'] = res['hiddenText'].replace('\x9d', '')
        return res
    
    def decodeBinary(self, cipher_text) -> dict:
        self.__setChars(cipher_text)
        decodeDic = self.crx.call("unicodeSteganographer.decodeBinary", cipher_text)
        decodeDic['hiddenData'] = bytes(decodeDic['hiddenData'].values())
        return decodeDic

class ZeroWidthLib(JSRuntime):

    def __init__(self, jsCode) -> None:
        super().__init__(jsCode)

    def decode(self, cipher_text) -> str:
        return self.crx.call("zero_width_lib.decode", cipher_text)

class ZwspStegJs(JSRuntime):

    def __init__(self, jsCode) -> None:
        super().__init__(jsCode)

    def decode_MODE_ZWSP(self, cipher_text) -> str:
        return self.crx.call("zwsp_steg_js.decode", cipher_text, 0)
    
    def decode_MODE_FULL(self, cipher_text) -> str:
        return self.crx.call("zwsp_steg_js.decode", cipher_text, 1)

class TextBlindWatermark(JSRuntime):
    
    def __init__(self, jsCode) -> None:
        super().__init__(jsCode)

    def decode(self, cipher_text) -> str:
        return self.crx.call("decode", cipher_text)
    
class MorseEncrypt(JSRuntime):
    
    def __init__(self, jsCode) -> None:
        super().__init__(jsCode)
        
    def decodeByMorse(self, cipher_text) -> str:
        return self.crx.call("handleDecode", cipher_text)

    def decodeByUnicode(self, cipher_text) -> str:
        return self.crx.call("decodeByUnicode", cipher_text)
    
def createJsObj():
    with open(os.path.join(jsDir, "unicode_steganography.js"), "rb") as f:
        unicodeSteganography = UnicodeSteganography(f.read())

    with open(os.path.join(jsDir, "zero-width-lib.js"), "rb") as f:
        zeroWidthLib = ZeroWidthLib(f.read())
        
    with open(os.path.join(jsDir, "zwsp-steg-js.js"), "rb") as f:
        zxwspStegJs = ZwspStegJs(f.read())
        
    with open(os.path.join(jsDir, "text_blind_watermark.js"), "rb") as f:
        text_blind_watermark = TextBlindWatermark(f.read())
    
    with open(os.path.join(jsDir, "morse-encrypt.js"), "rb") as f:
        morseEncrypt = MorseEncrypt(f.read())
    return unicodeSteganography, zeroWidthLib, zxwspStegJs, text_blind_watermark, morseEncrypt

def try_decode(decode_func, cipher):
  try:
    return decode_func(cipher)
  except Exception as _:
    return "不存在该零宽!"

if __name__ == '__main__':
    args = parse_arguments()
    baseDir = os.path.dirname(os.path.abspath(__file__))
    jsDir = os.path.join(baseDir, "js")
    filePath = os.path.abspath(args.f)
    with open(filePath, "r", encoding="utf-8") as f:
        cipher_text = f.read()
    
    unicodeSteganography, zeroWidthLib, zxwspStegJs, text_blind_watermark, morseEncrypt = createJsObj()
    
    libs = {
        "UnicodeSteg": unicodeSteganography.decodeText,
        "UnicodeStegBinary": unicodeSteganography.decodeBinary,
        "ZeroWidthLib": zeroWidthLib.decode,
        "ZxwspStegJs_ZWSP": zxwspStegJs.decode_MODE_ZWSP,
        "ZxwspStegJs_FULL": zxwspStegJs.decode_MODE_FULL,
        "Decode_TextBlindWatermark": text_blind_watermark.decode,
        "MorseEncrypt_decodeByMorse": morseEncrypt.decodeByMorse,
        "MorseEncrypt_decodeByUnicode": morseEncrypt.decodeByUnicode
    }
    
    icon()
    console.print("[1] UnicodeSteganography:")
    console.print(f"\tText: {try_decode(libs['UnicodeSteg'], cipher_text)['hiddenText']}")
    console.print(f"\tBinary: {try_decode(libs['UnicodeStegBinary'], cipher_text)['hiddenData']}")
    
    console.print("\n[2] Zero-Width-Lib:")
    console.print(f"\tText: {try_decode(libs['ZeroWidthLib'], cipher_text)}")

    console.print("\n[3] Zwsp-Steg-Js:")
    console.print(f"\tText1: {try_decode(libs['ZxwspStegJs_ZWSP'], cipher_text)}")
    console.print(f"\tText2: {try_decode(libs['ZxwspStegJs_FULL'], cipher_text)}")
    
    console.print("\n[4] text_blind_watermark:")
    console.print(f"\tText: {try_decode(libs['Decode_TextBlindWatermark'], cipher_text)}")
    
    console.print("\n[5] morse-encrypt:")
    console.print(f"\tMorse: {try_decode(libs['MorseEncrypt_decodeByMorse'], cipher_text)}")
    console.print(f"\tUnicode: {try_decode(libs['MorseEncrypt_decodeByUnicode'], cipher_text)}")
    os.system("pause")