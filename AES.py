def hex2bin(s):
    mp = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100", '5': "0101", '6': "0110", '7': "0111",
		  '8': "1000", '9': "1001", 'A': "1010", 'B': "1011", 'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin

def bin2hex(s):
	mp = {"0000": '0', "0001": '1', "0010": '2', "0011": '3', "0100": '4', "0101": '5', "0110": '6', "0111": '7',
          "1000": '8', "1001": '9', "1010": 'A', "1011": 'B', "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'}
	hex = ""
	for i in range(0, len(s), 4):
		ch = "" + s[i] + s[i + 1] + s[i + 2] + s[i + 3]
		hex = hex + mp[ch]
	return hex

def bin2dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = int(len(res) / 4)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans

def printState(state):
    for x in state:
        print(end='\t')
        for j in x:
            print(j, end='\t')
        print()
    print()

def gen_t(w, i):
    RCon = ['01000000', '02000000', '04000000', '08000000', '10000000', '20000000', '40000000', '80000000', '1B000000', '36000000']
    g = w[2:] + w[:2]
    s = ''
    for j in range(0, len(g), 2):
        s += S_Box[g[j]][g[j+1]]
    A = bin2hex(xor(hex2bin(s), hex2bin(RCon[i])))
    return A

def aes_key_gen(key):
    n = 8
    word = [(key[i:i+n]) for i in range(0, len(key), n)]
    t = []
    rk = [[[word[0][2 * i: 2 * (i + 1)], word[1][2 * i: 2 * (i + 1)], word[2][2 * i: 2 * (i + 1)], word[3][2 * i: 2 * (i + 1)]] for i in range(4)]]
    for j in range(1, 11):
        t = gen_t(word[4 * j - 1], j - 1)
        w0 = bin2hex(xor(hex2bin(t), hex2bin(word[4 * j - 4])))
        word.append(w0)
        w1 = bin2hex(xor(hex2bin(word[4 * j - 3]), hex2bin(word[-1])))
        word.append(w1)
        w2 = bin2hex(xor(hex2bin(word[4 * j - 2]), hex2bin(word[-1])))
        word.append(w2)
        w3 = bin2hex(xor(hex2bin(word[4 * j - 1]), hex2bin(word[-1])))
        word.append(w3)
        mat = [[w0[2 * i: 2 * (i + 1)], w1[2 * i: 2 * (i + 1)], w2[2 * i: 2 * (i + 1)], w3[2 * i: 2 * (i + 1)]] for i in range(4)]
        rk.append(mat)
    return rk

def add_round_key(rk, state):
    mat = [['' for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            m1 = hex2bin(state[i][j])
            m2 = hex2bin(rk[i][j])
            mat[i][j] = bin2hex(xor(m1, m2))
    return mat

def hex_product(a, b):
    A = hex2bin(a)
    B = hex2bin(b)
    if B.count('1') > A.count('1'):
        A, B = B, A
    B = B[::-1]
    L = len(B)
    c = ["" for i in range(L)]
    for i in range(L):
        if B[i] == '1':
            if i == 0:
                c[i] = A
            else:
                c[i] = A[i:] + "0" * i
        else:
            c[i] = "0" * 8
    c = list(zip(*c))
    C = ""
    for col in c:
        if col.count('1') % 2 == 0:
            C = C + "0"
        else:
            C = C + '1'
    return bin2hex(C)

def xor_list(l):
    l = [hex2bin(x) for x in l]
    x = ''
    for i in range(len(l[0])):
        s = 0
        for j in range(len(l)):
            if l[j][i] == '1':
                s += 1
        if s % 2 == 0:
            x += '0'
        else:
            x += '1'
    return bin2hex(x)

def mixColumns(A):
    B = [['02', '03', '01', '01'], ['01', '02', '03', '01'], ['01', '01', '02', '03'], ['03', '01', '01', '02']]
    C = [["" for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            l = []
            for k in range(4):
                t = hex_product(A[i][k], B[k][j])
                l.append(t)
            C[i][j] = xor_list(l)
    return C

def subBytes(mat):
    sub_state = mat
    for i in range(4):
        for j in range(4):
            r, c = mat[i][j]
            sub_state[i][j] = S_Box[r][c]
    return sub_state

def shiftRows(mat):
    shift = mat
    for i in range(4):
        shift[i] = mat[i][i:] + mat[i][:i]
    return shift

def concatState(mat):
    s = ''
    for i in range(4):
        for j in range(4):
            s += mat[j][i]
    return s

def intToState(pt):
    lis = [pt[i:i+2] for i in range(0, len(pt), 2)]
    state = [["" for j in range(4)] for i in range(4)]
    k = 0
    for i in range(4):
        for j in range(4):
            if k < len(lis):
                state[i][j] = lis[k]
                k += 1
    for i in range(4):
        for j in range(4):
            if state[i][j] == '':
                state[i][j] = bin2hex(dec2bin(ord('Z')))
    return state

def aes_encrypt(pt, rkh, show=False):
    states = []
    state = intToState(pt)
    if show:
        print('Initial State: ')
        printState(state)
    round0_state = add_round_key(rkh[0], state)
    if show:
        print("State after Round 0: ")
        printState(round0_state)
    states.append(round0_state)
    for k in range(1, 11):
        prev = states[-1]
        sub_state = subBytes(prev)
        if show:
            print(' State after substitution:')
            printState(sub_state)
        shift = shiftRows(sub_state)
        if show:
            print(' State after shift:')
            printState(shift)
        mc = mixColumns(shift)
        if show:
            print(' State after mix columns:')
            printState(mc)
        state = add_round_key(rkh[k], mc)
        if show:
            print("State after Round {}:".format(k))
            printState(state)
        states.append(state)
    states = [concatState(x) for x in states]
    ct = states[-1]
    return ct, states

# S-Box
S_Box = {'0': {'0': '63', '1': '7C', '2': '77', '3': '7B', '4': 'F2', '5': '6B', '6': '6F', '7': 'C5', '8': '30', '9': '01', 'A': '67', 'B': '2B', 'C': 'FE', 'D': 'D7', 'E': 'AB', 'F': '76'},
         '1': {'0': 'CA', '1': '82', '2': 'C9', '3': '7D', '4': 'FA', '5': '59', '6': '47', '7': 'F0', '8': 'AD', '9': 'D4', 'A': 'A2', 'B': 'AF', 'C': '9C', 'D': 'A4', 'E': '72', 'F': 'C0'},
         '2': {'0': 'B7', '1': 'FD', '2': '93', '3': '26', '4': '36', '5': '3F', '6': 'F7', '7': 'CC', '8': '34', '9': 'A5', 'A': 'E5', 'B': 'F1', 'C': '71', 'D': 'D8', 'E': '31', 'F': '15'},
         '3': {'0': '04', '1': 'C7', '2': '23', '3': 'C3', '4': '18', '5': '96', '6': '05', '7': '9A', '8': '07', '9': '12', 'A': '80', 'B': 'E2', 'C': 'EB', 'D': '27', 'E': 'B2', 'F': '75'},
         '4': {'0': '09', '1': '83', '2': '2C', '3': '1A', '4': '1B', '5': '6E', '6': '5A', '7': 'A0', '8': '52', '9': '3B', 'A': 'D6', 'B': 'B3', 'C': '29', 'D': 'E3', 'E': '2F', 'F': '84'},
         '5': {'0': '53', '1': 'D1', '2': '00', '3': 'ED', '4': '20', '5': 'FC', '6': 'B1', '7': '5B', '8': '6A', '9': 'CB', 'A': 'BE', 'B': '39', 'C': '4A', 'D': '4C', 'E': '58', 'F': 'CF'},
         '6': {'0': 'D0', '1': 'EF', '2': 'AA', '3': 'FB', '4': '43', '5': '4D', '6': '33', '7': '85', '8': '45', '9': 'F9', 'A': '02', 'B': '7F', 'C': '50', 'D': '3C', 'E': '9F', 'F': 'A8'},
         '7': {'0': '51', '1': 'A3', '2': '40', '3': '8F', '4': '92', '5': '9D', '6': '38', '7': 'F5', '8': 'BC', '9': 'B6', 'A': 'DA', 'B': '21', 'C': '10', 'D': 'FF', 'E': 'F3', 'F': 'D2'},
         '8': {'0': 'CD', '1': '0C', '2': '13', '3': 'EC', '4': '5F', '5': '97', '6': '44', '7': '17', '8': 'C4', '9': 'A7', 'A': '7E', 'B': '3D', 'C': '64', 'D': '5D', 'E': '19', 'F': '73'},
         '9': {'0': '60', '1': '81', '2': '4F', '3': 'DC', '4': '22', '5': '2A', '6': '90', '7': '88', '8': '46', '9': 'EE', 'A': 'B8', 'B': '14', 'C': 'DE', 'D': '5E', 'E': '0B', 'F': 'DB'},
         'A': {'0': 'E0', '1': '32', '2': '3A', '3': '0A', '4': '49', '5': '06', '6': '24', '7': '5C', '8': 'C2', '9': 'D3', 'A': 'AC', 'B': '62', 'C': '91', 'D': '95', 'E': 'E4', 'F': '79'},
         'B': {'0': 'E7', '1': 'C8', '2': '37', '3': '6D', '4': '8D', '5': 'D5', '6': '4E', '7': 'A9', '8': '6C', '9': '56', 'A': 'F4', 'B': 'EA', 'C': '65', 'D': '7A', 'E': 'AE', 'F': '08'},
         'C': {'0': 'BA', '1': '78', '2': '25', '3': '2E', '4': '1C', '5': 'A6', '6': 'B4', '7': 'C6', '8': 'E8', '9': 'DD', 'A': '74', 'B': '1F', 'C': '4B', 'D': 'BD', 'E': '8B', 'F': '8A'},
         'D': {'0': '70', '1': '3E', '2': 'B5', '3': '66', '4': '48', '5': '03', '6': 'F6', '7': '0E', '8': '61', '9': '35', 'A': '57', 'B': 'B9', 'C': '86', 'D': 'C1', 'E': '1D', 'F': '9E'},
         'E': {'0': 'E1', '1': 'F8', '2': '98', '3': '11', '4': '69', '5': 'D9', '6': '8E', '7': '94', '8': '9B', '9': '1E', 'A': '87', 'B': 'E9', 'C': 'CE', 'D': '55', 'E': '28', 'F': 'DF'},
         'F': {'0': '8C', '1': 'A1', '2': '89', '3': '0D', '4': 'BF', '5': 'E6', '6': '42', '7': '68', '8': '41', '9': '99', 'A': '2D', 'B': '0F', 'C': 'B0', 'D': '54', 'E': 'BB', 'F': '16'}
         }

def strTopt(p):
    s = ""
    for x in p:
        s += bin2hex(dec2bin(ord(x)))
    d = len(s) - 2 * 16
    if d > 0:
        for i in range(d):
            s += bin2hex(dec2bin(ord('Z')))
    return s

p = 'AESUSESAMATRIX'
pt = strTopt(p)
state = intToState(pt)
print('Initial State:')
printState(state)
sub = subBytes(state)
print('State after Sub Bytes:')
printState(sub)
shift = shiftRows(sub)
print('State after Shift Rows:')
printState(shift)
mix = mixColumns(shift)
print('State after Mix Columns:')
printState(mix)

k = "2475A2B33475568831E2120013AA5487"
print(pt)
rk = aes_key_gen(k)
c, sts = aes_encrypt(pt, rk, show=True)
print(c)

def bit_diff(A, B):
    A = hex2bin(A)
    B = hex2bin(B)
    C = xor(A,B)
    return C.count('1')

k1 = "2475A2B33475568831E2120013AA5487"
k2 = "2475A2B33475568831E2120013AB5487"
rk1 = aes_key_gen(k1)
rk2 = aes_key_gen(k2)
c1, sts1 = aes_encrypt(pt, rk1)
c2, sts2 = aes_encrypt(pt, rk2)
rk1 = [concatState(x) for x in rk1 if type(x[0]) == type([])]
rk2 = [concatState(x) for x in rk2 if type(x[0]) == type([])]
diff = bit_diff(k1, k2)
print("Initial  Bit Difference: {:02d}".format(0), "\tKeys used: ", k1, k2, "\tBit Difference in Key: {:02d}".format(diff))
for i in range(len(sts1)):
    diff = bit_diff(sts1[i], sts2[i])
    d = bit_diff(rk1[i], rk2[i])
    print("Round {:02d} Bit Difference: {:02d}".format(i, diff), "\tKeys used: ", sts1[i], sts2[i], "\tBit Difference in Key: {:02d}".format(d))