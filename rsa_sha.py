import sympy
import math

public_key, private_key, n = 0, 0, 0

def set_keys():
    global public_key, private_key, n
    p = sympy.randprime(1000, 2000)
    q = sympy.randprime(1000, 2000)
    print('Prime Numbers  - ', p, q)
    n = p * q
    fi = (p - 1) * (q - 1)
    e = 2
    while True:
        if math.gcd(e, fi) == 1:
            break
        e += 1
    public_key = e
    d = 2
    while True:
        if (d * e) % fi == 1:
            break
        d += 1
    private_key = d

def encoder(message):
    encrypted = []
    for x in message:
        enc = 1
        e = public_key
        while e > 0:
            enc *= ord(x)
            enc %= n
            e -= 1
        encrypted.append(enc)
    return encrypted

def decoder(message):
    decrypted = []
    for x in message:
        dec = 1
        d = private_key
        while d > 0:
            dec *= x
            dec %= n
            d -= 1
        decrypted.append(dec)
    return decrypted

if __name__ == '__main__':
    set_keys()
    print('Keys - ', public_key, private_key)
    message = 'Encrypt this'
    print('Original Message - ', [ord(x) for x in message])
    encrypt_text = encoder(message)
    print('Encrypted Message - ', encrypt_text)
    decrypt_text = decoder(encrypt_text)
    print('Decrypted Message - ', decrypt_text)

# SHA-512    
from hashlib import sha512
text = 'Hello There!'
hash = sha512(text.encode('utf-8'))
print(text)
print(hash.hexdigest())

#RSA in-built
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

keypair = RSA.generate(2048)
public = keypair.publickey().exportKey()
private = keypair.exportKey()

pt = 'hello there'
cipher = PKCS1_OAEP.new(RSA.import_key(public))
ct = cipher.encrypt(pt.encode())
print(ct)
ciph = PKCS1_OAEP.new(RSA.import_key(private))
et = ciph.decrypt(ct)
print(et.decode())
