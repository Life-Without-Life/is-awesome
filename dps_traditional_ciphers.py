import string
from sympy import mod_inverse
import math

def additive_cipher(text, mode, key):
    pop = string.ascii_letters
    additiveKey = {}
    cipher_message = ""
    for i in range(26):
        j = (i + key) % 26
        additiveKey[pop[i]] = pop[j]
        additiveKey[pop[i + 26]] = pop[j + 26]
    additiveKey[' '] = ' '
    if mode == 'encrypt':
        for char in text:
            cipher_message += additiveKey[char]
    elif mode == 'decrypt':
        for x in text:
            y = list(additiveKey.keys())[list(additiveKey.values()).index(x)]
            cipher_message += y
    return cipher_message
# additive cipher output
strz = "hElLo tHeRe"
print(strz)
zrts = additive_cipher(strz, "encrypt", 20)
print(zrts)
strz1 = additive_cipher(zrts, "decrypt", 20)
print(strz1)

def multiplicative_cypher(text,mode,key):
    char_dict={}
    cipher_message = ''
    for i in range(26):
         char_dict[chr(ord('a') + i)]=i
    key_list=list(char_dict.keys())
    inv_char_dict = dict(zip(char_dict.values(),char_dict.keys()))

    if mode == 'encrypt':
        if math.gcd( 26,key) == 1:
            for char in text:
                if char in key_list:
                    new_index=(char_dict[char]*key)%26
                    cipher_message=cipher_message+inv_char_dict[new_index]
                else:
                    cipher_message=cipher_message+char
        else:
            print('invalid key selected')

        return cipher_message

    if mode == 'decrypt':
        mult_inv=mod_inverse(key, 26)
        for char in text:
            if char in key_list:
                new_index=(char_dict[char]*mult_inv)%26
                cipher_message=cipher_message+inv_char_dict[new_index]
            else:
                cipher_message=cipher_message+char

    return cipher_message
#multiplicative cipher output
strz = "hElLo tHeRe"
print(strz)
zrts = multiplicative_cypher(strz, "encrypt", 19)
print(zrts)
strz1 = multiplicative_cypher(zrts, "decrypt", 19)
print(strz1)

def affine_cipher(text, mode, key):
    pop = string.ascii_letters
    n = len(pop)
    cipher_message = ''
    if mode == 'encrypt':
        for x in text:
            if x in pop:
                i = pop.index(x)
                j = (key[0] * i + key[1]) % n
                cipher_message += pop[j]
            else:
                cipher_message += x
    elif mode == 'decrypt':
        mult_inv=mod_inverse(key[0], n)
        for char in text:
            if char in pop:
                i = pop.index(char)
                j = mult_inv * (i - key[1]) % n
                cipher_message=cipher_message + pop[j]
            else:
                cipher_message=cipher_message+char
    return cipher_message
#affine cipher output
op1 = affine_cipher(strz, "encrypt", [17, 20])
op2 = affine_cipher(op1, "decrypt", [17, 20])
print(strz)
print(op1)
print(op2)

def transposition_cipher(txt, mode, key):
    K = len(key)
    P = len(txt)
    row = int(math.ceil(P / K))
    matrix = [ ['X'] * K for i in range(row)]
    t = 0
    if mode == 'encrypt':
        for r in range(row):
            for c,ch in enumerate(txt[t:t+K]):
                matrix[r][c] = ch
            t += K
        sort_order = sorted([(ch, i) for i,ch in enumerate(key)])
        cipher_txt = ''
        for ch,c in sort_order:
            for r in range(row):
                cipher_txt += matrix[r][c]
        return cipher_txt
    elif mode == 'decrypt':
        cipher_txt = txt
        key_order = [key.index(ch) for ch in sorted(list(key))]
        for c in key_order:
            for r,ch in enumerate(cipher_txt[t:t+row]):
                matrix[r][c] = ch
            t += row
        p_txt = ''
        for r in range(row):
            for c in range(K):
                p_txt += matrix[r][c] if matrix[r][c] != 'X' else ''
        return p_txt
    else:
        return "ERROR"
# transposition cipher
p_txt = 'enemyattackstonight '
key = 'head'
print(p_txt)
c_txt = transposition_cipher(p_txt, "encrypt", key)
print(c_txt)
print(transposition_cipher(c_txt, "decrypt", key))

# double transfposition cipher - just do transposition cipher twice obviously
p_txt = 'enemyattackstonight '
key = 'head'
key1 = 'fade'
print(p_txt)
c1_txt = transposition_cipher(p_txt, "encrypt", key)
c2_txt = transposition_cipher(c1_txt, "encrypt", key1)
p1_txt = transposition_cipher(c2_txt, "decrypt", key1)
p2_txt = transposition_cipher(p1_txt, "decrypt", key)
print(c1_txt)
print(c2_txt)
print(p1_txt)
print(p2_txt)

len(p_txt)
