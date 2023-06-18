from Crypto.Random import get_random_bytes # used to generate a random salt
from Crypto.Protocol.KDF import PBKDF2 # used for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generateKey(keyPass: str) -> bytes:
    # generate a  key for encryption and decryption
    salt = get_random_bytes(32)
    key = PBKDF2(keyPass, salt, dkLen=32)

    with open('key.bin', 'wb') as f:
        f.write(key)
    return key

def generateEncryptedPassword(password: str) -> bytes:
    passwordBytes = str.encode(password)

    with open('key.bin', 'rb') as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC)
    encryptedPassword = cipher.encrypt(pad(passwordBytes, AES.block_size))
    with open('password.bin', 'wb') as f:
        f.write(cipher.iv)
        f.write(encryptedPassword)
    return encryptedPassword

def decryptEncryptedPassword() -> bytes:
    with open("password.bin", 'rb') as f:
        iv = f.read(16)
        encryptedPassword = f.read()

    with open("key.bin", 'rb') as f:
        key = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    passwordBytes = unpad(cipher.decrypt(encryptedPassword), AES.block_size)
    password = passwordBytes.decode('ascii')
    return password

myKey = generateKey("twentyOrangesOnAMountain")
print(generateEncryptedPassword("MclarenP1"))
print(decryptEncryptedPassword())