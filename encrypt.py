from Crypto.Random import get_random_bytes # used to generate a random salt
from Crypto.Protocol.KDF import PBKDF2 # used for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import string

def generateRandomString() -> str:
    characterSet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characterSet) for i in range(64))


def generateKey() -> None:
    keyPass = generateRandomString()
    # generate a  key for encryption and decryption
    salt = get_random_bytes(32)
    key = PBKDF2(keyPass, salt, dkLen=32)

    with open('key.bin', 'wb') as f:
        f.write(key)

def generateEncryptedPassword(password: str) -> None:
    passwordBytes = str.encode(password)

    with open('key.bin', 'rb') as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    encryptedPassword = cipher.encrypt(pad(passwordBytes, AES.block_size))
    with open('password.bin', 'wb') as f:
        f.write(cipher.iv)
        f.write(encryptedPassword)

def decryptEncryptedPassword() -> str:
    with open("password.bin", 'rb') as f:
        iv = f.read(16)
        encryptedPassword = f.read()

    with open("key.bin", 'rb') as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    passwordBytes = unpad(cipher.decrypt(encryptedPassword), AES.block_size)
    password = passwordBytes.decode('ascii')
    return password