import socket 
import string   
import random # import randint
import time
from hashlib import sha256
import pyexcel as pe 
import pyexcel as pe  
import collections 
from hashlib import sha256
import secrets 

def xor_sha_strings(s, t):
    # Pad the shorter string with a leading zero if its length is odd
    if len(s) % 2 == 1:
        s = '0' + s
    if len(t) % 2 == 1:
        t = '0' + t

    s_bytes = bytes.fromhex(s)
    t_bytes = bytes.fromhex(t)

    res_bytes = bytes(a ^ b for a, b in zip(s_bytes, t_bytes))
    return res_bytes.hex()

def listToString(s): 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += str(ele)
        str1 += ","
    str1 = str1[:len(str1)-1]
    return str1

def inverse_mod(k, p):
    """Returns the inverse of k modulo p.

    This function returns the only integer x such that (x * k) % p == 1.

    k must be non-zero and p must be a prime.
    """
    if k == 0:
        raise ZeroDivisionError('division by zero')

    if k < 0:
        # k ** -1 = p - (-k) ** -1  (mod p)
        return p - inverse_mod(-k, p)

    # Extended Euclidean algorithm.
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    gcd, x, y = old_r, old_s, old_t

    assert gcd == 1
    assert (k * x) % p == 1

    return x % p

# Functions that work on curve points #########################################

def is_on_curve(point):
    """Returns True if the given point lies on the elliptic curve."""
    if point is None:
        # None represents the point at infinity.
        return True

    x, y = point

    return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


def point_neg(point):
    """Returns -point."""
    assert is_on_curve(point)

    if point is None:
        # -0 = 0
        return None

    x, y = point
    result = (x, -y % curve.p)

    assert is_on_curve(result)

    return result


def point_add(point1, point2):
    """Returns the result of point1 + point2 according to the group law."""
    assert is_on_curve(point1)
    assert is_on_curve(point2)

    if point1 is None:
        # 0 + point2 = point2
        return point2
    if point2 is None:
        # point1 + 0 = point1
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and y1 != y2:
        # point1 + (-point1) = 0
        return None

    if x1 == x2:
        # This is the case point1 == point2.
        m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
    else:
        # This is the case point1 != point2.
        m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

    x3 = m * m - x1 - x2
    y3 = y1 + m * (x3 - x1)
    result = (x3 % curve.p,
              -y3 % curve.p)

    assert is_on_curve(result)

    return result


def scalar_mult(k, point):
    """Returns k * point computed using the double and point_add algorithm."""
    assert is_on_curve(point)

    if k % curve.n == 0 or point is None:
        return None

    if k < 0:
        # k * point = -k * (-point)
        return scalar_mult(-k, point_neg(point))

    result = None
    addend = point

    while k:
        if k & 1:
            # Add.
            result = point_add(result, addend)

        # Double.
        addend = point_add(addend, addend)

        k >>= 1

    assert is_on_curve(result)

    return result

# Keypair generation and ECDHE ################################################

'''
def make_keypair():
    """Generates a random private-public key pair."""
    private_key_bit_length = curve.n.bit_length()
    
    print ("111 private_key_bit_length : ", private_key_bit_length)
    private_key = random.getrandbits(256)
    print ("222 pri key : ", private_key)
    while private_key >= curve.n:
        private_key = random.getrandbits(private_key_bit_length)
    public_key = scalar_mult(private_key, curve.g)
    print ("******* Private key length : ", str(private_key), len(str(private_key)))

    return private_key, public_key

'''
def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, curve.n)
    public_key = scalar_mult(private_key, curve.g)

    return private_key, public_key

def convertTuple_str(tup):
    # Initialize an empty string
    dh_str = ''
    for item in tup:
        dh_str = dh_str + str(item) + ","
    # Remove the last comma
    dh_str = dh_str[:-1]
    return dh_str

def encrypt_data (cipher, plain_text) :

    encrypted_1 = []
    plain_text = plain_text.encode().hex()
    if len(plain_text) > 16 :
        splitted_pt = [plain_text[i:i+16] for i  in range(0, len(plain_text), 16)]
        for each_str in splitted_pt:
            #print ("Encrypting ", each_str)
            encrypted_1.append(cipher.present_encrypt(each_str))
    else :
        encrypted_1 = cipher.present_encrypt(plain_text)
    
    return listToString(encrypted_1)

def decrypt_data (cipher, enc_text) :

    decrypted_1 = []
    splitted_pt = [str(i) for i in enc_text.split(',')]
    for each_str in splitted_pt:
        #print ("Decrypting ", each_str)
        decrypted_1.append(bytes.fromhex(cipher.present_decrypt(each_str)).decode())
    decrypt_temp = ""
    decrypted_1 = decrypt_temp.join(decrypted_1)
    decrypted_1 = decrypted_1.rstrip('\x00').replace('\x00', '')
    
    return decrypted_1

def str_to_tuple (inp_str) :
    split_values = inp_str.strip('()').split(',')

    # Convert each string value to an integer and create a tuple
    tuple_of_integers = tuple(int(value.strip()) for value in split_values)
    return tuple_of_integers

EllipticCurve = collections.namedtuple('EllipticCurve', 'name p a b g n h')

curve = EllipticCurve(
    'secp256k1',
    # Field characteristic.
    p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
    # Curve coefficients.
    a=0,
    b=7,
    # Base point.
    g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
       0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
    # Subgroup order.
    n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,
    # Subgroup cofactor.
    h=1,
)

veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 6002)
veh_socket.connect(server_address)
print(f"Connected to {server_address}") 

reg_sheet1 = pe.get_sheet (file_name= "BHAS_Reg_Veh_details.xlsx")

start_latency = time.time ()

ID_size = 7

start1_comp_time = time.time ()

DID = ''.join(secrets.choice('0123456789abcdef') for _ in range(8))
ID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))
PIN = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))
SI = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))

print ("DID : ", DID, type (DID))
print ("ID : ", ID, type (ID))
print ("PIN : ", PIN, type (PIN))
print ("SI : ", SI, type (SI))

ID_SI = ID + "&"+ SI

end1_comp_time = time.time ()
veh_comp_time = end1_comp_time - start1_comp_time

veh_socket.send(ID_SI.encode('utf'))
PID_BI = veh_socket.recv(1024).decode() 

start2_comp_time = time.time ()
r = random.randrange(1, 103)

PID_BI = [str(i) for i in PID_BI.split('&')]
PID = PID_BI[0]
BI = PID_BI[1]

print ("PID : ", PID, type(PID))
print ("BI : ", BI, type(BI), "\n")

A = xor_sha_strings( sha256(ID.encode('utf-8') + PIN.encode('utf-8')).hexdigest(), str(r))
h_r = sha256(str(r).encode('utf-8') ).hexdigest()

print ("A : ", A, type(A))
print ("h_r : ", h_r, type(h_r), "\n")

Q = xor_sha_strings (BI, h_r)
R = sha256(PID.encode('utf-8') + BI.encode('utf-8')+ Q.encode('utf-8')).hexdigest()

print ("Q : ", Q, type(Q), "\n")
print ("R : ", R, type(R), "\n")

end2_comp_time = time.time ()
veh_comp_time += end2_comp_time - start2_comp_time

end_latency = time.time ()
Reg_latency = end_latency - start_latency
print ("Total Comp Time : ", veh_comp_time)

print ("Total Reg latency : ", Reg_latency) 

# import sys
# ID_size = sys.getsizeof (ID)
# PIN_size = sys.getsizeof (PIN)
# PID_size = sys.getsizeof (PID)
# A_size = sys.getsizeof (A)
# Q_size = sys.getsizeof (Q)
# R_size = sys.getsizeof (R)
# DID_size = sys.getsizeof (DID)

# print ("ID : ", ID_size)
# print ("PIN : ", PIN_size) 
# print ("PID : ", PID_size)
# print ("A : ", A_size)
# print ("Q : ", Q_size)
# print ("R : ", R_size)
# print ("DID : ", DID_size)

# total_size = ID_size + PIN_size + PID_size + A_size + Q_size + R_size + DID_size 
# print ("Total storage size for veh Reg : ", total_size)

reg_sheet1.row += [ ID, PIN, PID, A, Q, R, DID, veh_comp_time, Reg_latency]
reg_sheet1.save_as ("BHAS_Reg_Veh_details.xlsx")






