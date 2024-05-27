import socket
import random # import randint 
import time
from hashlib import sha256
import datetime 
import pyexcel as pe   
import collections
import sys

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

def make_keypair():
    """Generates a random private-public key pair."""
    private_key = random.randrange(1, curve.n)
    public_key = scalar_mult(private_key, curve.g)

    return private_key, public_key

def convertTuple_str(tup):
        # initialize an empty string
    dh_str = ''
    for item in tup:
        dh_str = dh_str + str(item) + ","
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

def get_timestamp() :
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    return ts

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

reg_sheet1 = pe.get_sheet (file_name= "Provable_Reg_Veh_details.xlsx")
auth_sheet1 = pe.get_sheet (file_name= "Provable_Auth_Veh_details.xlsx")
hand_sheet1 = pe.get_sheet (file_name= "Provable_Hand_Veh_details.xlsx")

VID_inp = sys.argv[1] # ZGYUCBJ VNDHTNX ABPPG67

auth_flag = 0
reg_flag = 0
RID = "RSU1"

for row in reg_sheet1 : # Get ( V, S1.decode(), S2.decode(), S3.decode(), A_str, PK_Vi_str, PK_TA_str, PID_str, VaI, Tou, Veh_Reg_comp_time )
    if row[0] == VID_inp :
        V = row[1]
        S1 = row[2]
        S2 = row[3]
        S3 = row[4]
        A = row[5]
        PK_Vi = row[6]
        PK_TA = row[7]
        PID_str = row[8]
        VaI = row[9]
        Tou = row[10]
        sigma = row[11]
        SK_V = row[12]
        reg_flag = 1 
        print ("  V : ", VID_inp, "match found ...")
        break

for row in auth_sheet1 :
    if row[0] == VID_inp :
        V = row[1]
        S1 = row[2]
        S2 = row[3]
        S3 = row[4]
        A = row[5]
        PK_V = row[6]
        PK_TA = row[7]
        PID = row[8]
        VaI = row[9]
        Tou = row[10]
        sigma = row[11]
        SK_it = row[12]
        auth_flag = 1
        break

veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('192.168.20.200', 6012) # 192.168.20.200

conn_flag = 0
print ("Trying to connect ...")

while conn_flag == 0: 
    try :
        veh_socket.connect(server_address)
        print(f"Connected to {server_address}") 
        conn_flag = 1
    except :
        print ("Failed ... Trying to connect again")


comp_start_time = time.time ()

if reg_flag == 1 and auth_flag == 1 :
    print ("Excel details found  ...")

    AC = random.randint (100, 10000)
    h_SKit = sha256 ( SK_it.encode('utf-8')).hexdigest()
    h_AC = sha256 ( str(AC).encode('utf-8') ).hexdigest()
    T4 = get_timestamp ()

    # print ("\n ^^^^^^^^^^^^^^^^^\nPID : ", PID_str, type(PID_str))
    # print ("RID : ", RID, type(RID))
    # print ("h_SKit : ", h_SKit, type(h_SKit))
    # print ("T4 : ", T4, type(T4))
    # print ("h_AC : ", h_AC, type(h_AC), "\n^^^^^^^^^^^^^^^^^^^^\n")

    N2 = sha256 ( PID_str.encode('utf-8') + RID.encode ('utf-8') + h_SKit.encode('utf-8') + str(T4).encode ('utf-8') + h_AC.encode('utf-8') ).hexdigest() 

    PID_AC_N2_T4 = PID_str +"&"+ str(AC) +"&"+ N2 +"&"+ str(T4)
    veh_socket.send(PID_AC_N2_T4.encode('utf-8'))

    
    comp_end_time = time.time ()
    veh_comp_time = comp_end_time - comp_start_time
    print ("Total Comp Time : ", veh_comp_time)

    # import sys
    # vid_size = sys.getsizeof (VID_inp)
    # v_size = sys.getsizeof (V)
    # s1_size = sys.getsizeof (S1)
    # s2_size = sys.getsizeof (S2)
    # s3_size = sys.getsizeof (S3)
    # astar_size = sys.getsizeof (A)
    # PK_Vi_str_size = sys.getsizeof (PK_Vi)
    # PK_TA_str_size = sys.getsizeof (PK_TA)
    # PID_str_size = sys.getsizeof (PID_str)
    # VaI_size = sys.getsizeof (VaI)
    # Tou_size = sys.getsizeof (Tou)
    # sigma_size = sys.getsizeof (sigma)
    # SK_Vi_size = sys.getsizeof (SK_it)

    # print ("vid_size : ", vid_size)
    # print ("v_size : ", v_size)
    # print ("s1_size : ", s1_size)
    # print ("s2_size : ", s2_size)
    # print ("s3_size : ", s3_size)
    # print ("astar_size : ", astar_size)
    # print ("PK_Vi_str_size : ", PK_Vi_str_size)
    # print ("PK_TA_str_size : ", PK_TA_str_size)
    # print ("PID_str_size : ", PID_str_size)
    # print ("VaI_size : ", VaI_size)
    # print ("Tou_size : ", Tou_size)
    # print ("sigma_size : ", sigma_size)
    # print ("SK_Vi_size : ", SK_Vi_size)

    # total_size = SK_Vi_size + sigma_size + Tou_size + VaI_size + vid_size + v_size + s1_size + s2_size + s3_size + astar_size + PK_Vi_str_size + PK_TA_str_size + PID_str_size 
    # print ("Total storage size for veh Reg : ", total_size)
    
    hand_sheet1.row += [ VID_inp, V, S1, S2, S3, A, PK_Vi, PK_TA, PID_str, VaI, Tou, sigma, str(SK_it), veh_comp_time]
    hand_sheet1.save_as ("Provable_Hand_Veh_details.xlsx")

    print ("===========  Auth Success ========== \n")
else :
    print ("Excel sheet details not found")

