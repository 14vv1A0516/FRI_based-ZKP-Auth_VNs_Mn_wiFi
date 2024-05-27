import socket  
import string   
import random # import randint
import time
from hashlib import sha256
import pyexcel as pe 
import pyexcel as pe  
import collections  
from hashlib import sha256

'''
def xor_sha_strings(s,t): 
    s = bytes.fromhex(s)
    t = bytes.fromhex(t) 

    res_bytes = bytes(a^b for a,b in zip(s,t))
    return res_bytes.hex()
'''
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

reg_sheet1 = pe.get_sheet (file_name= "Provable_Reg_Veh_details.xlsx")

PK_TA_enc = "0x4cfba5a1ed64402a123939a7c4670d7eafb87adb4999f1b4d25364fd26d87f93a87ad84b5d3cde86df9c3da71c19eb09e3eea0e85439217ee17f2116fb6f7079"
ID_size = 7

start1_comp_time = time.time ()
SK_Vi, PK_Vi = make_keypair()

print ("SK_Vi : ", SK_Vi, len(str(SK_Vi)))
print ("PK_Vi : ", PK_Vi)
start_latency = time.time ()

VID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))
VaI = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))

PK_Vi_str = ','.join(str(num) for num in PK_Vi)

print ("PK_Vi_str : ", PK_Vi_str, type (PK_Vi_str))

VID_PK_VaI = VID +"&"+ PK_Vi_str +"&"+ VaI
end1_comp_time = time.time ()
veh_comp_time = end1_comp_time - start1_comp_time

veh_socket.send(VID_PK_VaI.encode('utf'))

PID_A_b_PK_TA_r = veh_socket.recv(1024).decode() 
start2_comp_time = time.time ()
PID_A_b_PK_TA_r = [str(i) for i in PID_A_b_PK_TA_r.split('$$')]

PID_str = PID_A_b_PK_TA_r[0]
PID = PID_A_b_PK_TA_r[0]
A_str = PID_A_b_PK_TA_r[1]
A = str_to_tuple(PID_A_b_PK_TA_r[1])
#print ("\nA_str : ", A, type(A_str))
b = int(PID_A_b_PK_TA_r[2])
PK_TA_str = PID_A_b_PK_TA_r[3]

PK_TA = str_to_tuple(PID_A_b_PK_TA_r[3])
r = PID_A_b_PK_TA_r[4]

# print ("\nPID : ", PID, type(PID))      
# print ("\nA : ", A, type(A))
# print ("\nbi : ", b, type(b))
# print ("\nPK_TA : ", PK_TA, type(PK_TA[0]))
# print ("\nr : ", r, "\n=============\n")
PID = bytes.fromhex(PID)
# print ("PID : ", PID, type(PID))
# print ("\nPK_Vi : ", PK_Vi_str, type(PK_Vi_str))
# print ("\nA_str : ", A_str, type(A_str))
# print ("\n===================\n")

#tuple_of_integers = tuple(int(num) for num in tuple_of_strings)
# print ("Hased Innt : ", int(sha256(PID + PK_Vi_str.encode('utf-8') + A_str.encode('utf-8')).hexdigest(), 16))
temp_bi = scalar_mult (int(sha256(PID + PK_Vi_str.encode('utf-8') + A_str.encode('utf-8')).hexdigest(), 16), PK_TA) 
# print ("\ntemp bi is ", temp_bi, type(temp_bi))

final_bi = point_add (temp_bi, A)

# print ("bi at Veh : ", final_bi)
check_bi = scalar_mult (b, curve.g)
# print ("\n --- Check bi is ", check_bi, type(check_bi))

if final_bi == check_bi :
    print ("-------Matched ------")
    sigma = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))
    Tou = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))

    V = sha256 (sigma.encode ('utf-8') + VaI.encode('utf-8')).hexdigest ()
    # print ("V is ", V, type(V))
    # print ("\nb : ", b, type(b))
    # print ("b in hex : ",  format(b, 'x'), type(hex(b)))

    # print ("\nCalling XOR for S1 *************")
    S1 = xor_sha_strings (str(b), sha256 (sigma.encode ('utf-8') + V.encode('utf-8')).hexdigest () )
    # print ("S1 is ", S1, type(S1))
    # print ("r is ", r, type(r))
    # print ("\nCalling XOR for S3 *************")

    S3 = xor_sha_strings (r, sha256 ( VID.encode('utf-8') + sigma.encode ('utf-8') ).hexdigest())
    # print ("S3 is ", S3)

    # print ("int(SK_Vi) : ", SK_Vi, type(SK_Vi))
    # print ("str(SK_Vi) : ", str(SK_Vi), len(str(SK_Vi)))

    # print ("sha256 ( V.encode('utf-8') + sigma.encode ('utf-8') ).hexdigest() : ", sha256 ( V.encode('utf-8') + sigma.encode ('utf-8') ).hexdigest())
    # print ("\nCalling XOR for S2 *************")

    S2 = xor_sha_strings (str(SK_Vi), sha256 ( V.encode('utf-8') + sigma.encode ('utf-8') ).hexdigest())
    #print ("\nS2 is ", S2)

    end2_comp_time = time.time ()
    veh_comp_time += end2_comp_time - start2_comp_time
    end_latency = time.time ()

    reg_latency = end_latency - start_latency
    print ("Total Reg Latency : ", reg_latency)

    print ("veh_comp_time : ", veh_comp_time)

    # print ("V : ", V)
    # print ("S1 : ", S1)
    # print ("S2 : ", S2)
    # print ("S3 : ", S3)

    # print ("A_str : ", A_str)

    # print ("PK_Vi_str : ", PK_Vi_str)
    # print ("PK_TA_str : ", PK_TA_str)
    # print ("PID_str : ", PID_str)

    # print ("VID : ", VID)
    # print ("VaI : ", VaI)
    # print ("Tou : ", Tou)
    # print ("Total Comp Time : ", veh_comp_time)
    '''
    import sys
    vid_size = sys.getsizeof (VID)
    v_size = sys.getsizeof (V)

    s1_size = sys.getsizeof (S1)
    s2_size = sys.getsizeof (S2)
    s3_size = sys.getsizeof (S3)
    astar_size = sys.getsizeof (A_str)
    PK_Vi_str_size = sys.getsizeof (PK_Vi_str)
    PK_TA_str_size = sys.getsizeof (PK_TA_str)
    PID_str_size = sys.getsizeof (PID_str)
    VaI_size = sys.getsizeof (VaI)
    Tou_size = sys.getsizeof (Tou)
    sigma_size = sys.getsizeof (sigma)

    SK_Vi_size = sys.getsizeof (SK_Vi)

    print ("vid_size : ", vid_size)
    print ("v_size : ", v_size)
    print ("s1_size : ", s1_size)
    print ("s2_size : ", s2_size) 
    print ("s3_size : ", s3_size)
    print ("astar_size : ", astar_size)
    print ("PK_Vi_str_size : ", PK_Vi_str_size)
    print ("PK_TA_str_size : ", PK_TA_str_size)
    print ("PID_str_size : ", PID_str_size)
    print ("VaI_size : ", VaI_size)
    print ("Tou_size : ", Tou_size)
    print ("sigma_size : ", sigma_size)
    print ("SK_Vi_size : ", SK_Vi_size)

    total_size = SK_Vi_size + sigma_size + Tou_size + VaI_size + vid_size + v_size + s1_size + s2_size + s3_size + astar_size + PK_Vi_str_size + PK_TA_str_size + PID_str_size 
    print ("Total storage size for veh Reg : ", total_size)
    '''
    reg_sheet1.row += [ VID, V, S1, S2, S3, A_str, PK_Vi_str, PK_TA_str, PID_str, VaI, Tou, sigma, str(SK_Vi), veh_comp_time, reg_latency]
    reg_sheet1.save_as ("Provable_Reg_Veh_details.xlsx")






