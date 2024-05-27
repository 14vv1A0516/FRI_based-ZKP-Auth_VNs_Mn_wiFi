import socket
import time
import sys 
import random # import randint
import time
from hashlib import sha256 
import collections
import pyexcel as pe 
import datetime 

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

def convertTuple_str(tup):
    # Initialize an empty string
    dh_str = ''
    for item in tup:
        dh_str = dh_str + str(item) + ","
    # Remove the last comma
    dh_str = dh_str[:-1]
    return dh_str

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
    # ct stores current time
    ct = datetime.datetime.now()
    #print("current time:-", ct)
 
    # ts store timestamp of current time
    ts = ct.timestamp()
    #print("timestamp:-", ts)
    return ts

def xor_sha_strings(s,t): 
    s = bytes.fromhex(s)
    t = bytes.fromhex(t)

    res_bytes = bytes(a^b for a,b in zip(s,t))
    return res_bytes.hex()

def listToString(s): 
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += str(ele)
        str1 += ","
    str1 = str1[:len(str1)-1]
    #print ("str returning is ", str1)
    # return string
    return str1

veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

hand_sheet = pe.get_sheet (file_name = "SON_Veh_Hand.xlsx")

TIDi = sys.argv[1] # "b2fbda45fe4337e4e49190271e37358bac16155cbb47f1cfb028832774f37e28" #sys.argv[1]  # only I/P

auth_sheet = pe.get_sheet (file_name = "SON_Veh_Auth.xlsx")
row_flag = 0 

for row in auth_sheet :
    if row[0] == TIDi:
        RIDi = row[1]
        row_flag = 1
        print ("ID matched and extracted ...")
        break

hand1_start_latency = time.time ()

hand1_comp_start_time = time.time ()
ci = random.randint(100, 100000)
#Input : RID, TID, ID_RSU, T3 

if row_flag == 1 :
      
    #print("RIDi is ", type(RIDi))
    IDk = 'RSU2_hand'
    T3 = get_timestamp()

    hridtid =  sha256(RIDi.encode('utf-8') + TIDi.encode('utf-8') + str(IDk).encode('utf-8')+ str(T3).encode('utf-8')).hexdigest()
    ci = str(ci).zfill(64)
    #print("ci is ", ci)

    M5 = xor_sha_strings (hridtid, ci) 
    M6 = sha256(ci.encode('utf-8')+ RIDi.encode('utf-8') + TIDi.encode('utf-8')).hexdigest()
    msg1 = TIDi + ","+ M5+ ","+ M6+ ","+ str(T3)

    hand1_comp_end_time = time.time ()

    # import sys
    # TD_size = sys.getsizeof (TIDi)
    # M5_size = sys.getsizeof (M5)
    # M6_size = sys.getsizeof (M6)
    # T3_size = sys.getsizeof (str(T3))

    # print ("TD size : ", TD_size)
    # print ("M5_size : ", M5_size)
    # print ("M6 size : ", M6_size)
    # print ("T3 size : ", T3_size)

    # total_size = TD_size + M5_size + M6_size + T3_size

    # print ("^^^^^^^ Total comm cost for Hand at Veh : ", total_size)
    hand_comp_time = hand1_comp_end_time - hand1_comp_start_time

    # print ("data send : ", msg1)
    veh_socket.send(msg1.encode('utf'))  # send TIDi, M5, M6, T3 to RSU

    data = veh_socket.recv(1024).decode() # Got M7, M8, M9, T4

    hand2_comp_start_time = time.time ()

    values = [str(i) for i in data.split(',')]
    M7 = values[0]
    M8 = values[1]
    M9 = values[2]
    T4 = float(values[3])

    curr_time = get_timestamp ()

    if curr_time - T4 < 5 :
        print ("T4 check Success ...")

        hcrid = sha256(ci.encode('utf-8')+ RIDi.encode('utf-8')).hexdigest()
        TIDnew = xor_sha_strings (M7, hcrid)
        hcitidrid = sha256(ci.encode('utf-8')+ TIDnew.encode('utf-8')+ RIDi.encode('utf-8')).hexdigest()

        ck = xor_sha_strings(M8, hcitidrid)

        SKik = sha256(ck.encode('utf-8')+ ci.encode('utf-8')+ TIDnew.encode('utf-8')+ RIDi.encode('utf-8')).hexdigest()

        hskikt4 = sha256(SKik.encode('utf-8')+ str(T4).encode('utf-8')).hexdigest()

        if M9 == hskikt4 :
            print ("Handover Authentication successful ...")
            hand2_comp_end_time = time.time () 
            hand_comp_time += hand2_comp_end_time - hand2_comp_start_time

            hand1_end_latency = time.time()

            hand_latency = hand1_end_latency - hand1_start_latency

            print (" \nHandover Auth time at Veh is ", hand_comp_time, " sec")
            print ("Total Handover Latency is ", hand_comp_time, " sec")

            hand_sheet.row += [hand_comp_time,  hand_latency]
            hand_sheet.save_as ("SON_Veh_Hand.xlsx")
        else :
            print ("Handover Failed ...")
    else :
        print ("Time stamp failed.. Possible Session attack")
else :
    print ("TIDi not found in Excel sheet ...")

veh_socket.close ()



