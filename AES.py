from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad

string = "hello there"

def AES_encrypt(string,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k,AES.MODE_ECB)
    enc_text = cipher.encrypt(pad(bytes(string, 'utf-8'), 16))
    return enc_text

def AES_decrypt(enc_text,key):
    k = bytes(key, 'utf-8')
    cipher = AES.new(k, AES.MODE_ECB)
    dec_text = cipher.decrypt(enc_text)
    return unpad(dec_text, 16)

print("\n\nAES ENCRYPTION\n")
aes_encrypt = AES_encrypt(string,key2)
print(aes_encrypt)
print(AES_decrypt(aes_encrypt, key2))
