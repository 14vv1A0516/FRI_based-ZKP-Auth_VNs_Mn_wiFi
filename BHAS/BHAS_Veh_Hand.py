import socket
import random # import randint 
import time
from hashlib import sha256 
import datetime
import pyexcel as pe 
import collections
import sys

def get_timestamp() :
    ct = datetime.datetime.now()
    ts = ct.timestamp() 
    return ts

def listToString(s): 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += str(ele)
        str1 += ","
    str1 = str1[:len(str1)-1]
    return str1

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

reg_sheet1 = pe.get_sheet (file_name= "BHAS_Reg_Veh_details.xlsx")
auth_sheet1 = pe.get_sheet (file_name= "BHAS_Auth_Veh_details.xlsx")
hand_sheet = pe.get_sheet (file_name= "BHAS_Hand_Veh_details.xlsx")

ID = sys.argv[1] #"UHDD3KC" #sys.argv[1]  # F2IPFKP  LI78DJK  8IQYQ9I
q = 103
ID_RSU = "RSU2"
auth_flag = 0
reg_flag = 0
Pub_RSU = (106415322946774620779972128495151441125342886528160775819643398608002266674986, 46276119434053460364772345509604491264866428019260025358513227732146803003502)

veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('192.168.20.200', 6012)  # 192.168.20.200

conn_flag = 0

while conn_flag == 0: 
    try :
        veh_socket.connect(server_address)
        print(f"Connected to {server_address}") 
        conn_flag = 1
    except :
        print ("Failed ... Trying to connect again")

for row in reg_sheet1 : # Get ( VID, PID, VPID, NVID, f(w^i), fe(w^2i), fo(w^2i), Veh_Reg_comp_time )
    if row[0] == ID :
        PIN = row[1]
        PID = row[2]
        A = row[3]
        Q = row[4]
        R = row[5]
        DID = row[6]
        reg_flag = 1 
        print ("  VPID : ", ID, "match found ...")
        break

for row in reg_sheet1 : # Get ( VID, PID, VPID, NVID, f(w^i), fe(w^2i), fo(w^2i), Veh_Reg_comp_time )
    if row[0] == ID : 
        BI = row[1]
        auth_flag = 1 
        print ("  VID : ", ID, "match found ...")
        break

start_latency = time.time ()
start1_comp_time = time.time ()

if reg_flag == 1 and auth_flag == 1:
    
    u = random.randrange (1, 103)

    A = scalar_mult (u, Pub_RSU)
    Ax = A[0]
    Ay = A[1]

    B = scalar_mult (u, curve.g)
    # print ("DID : ", DID, type (DID), "\n")
    # print ("ID_RSU : ", ID_RSU, type (ID_RSU), "\n")

    M00 = xor_sha_strings (DID, ID_RSU.encode('utf-8').hex())
    T3 = get_timestamp ()

    #print ("Ax : ", Ax, type (Ax), "\n")

    M11 = sha256(DID.encode('utf-8') + str(Ax).encode('utf-8') + str(T3).encode('utf-8') ).hexdigest()
    #print ("M11 : ", M11)
    M22 = xor_sha_strings (PID, M11)
    M33 = sha256(PID.encode('utf-8') + ID_RSU.encode('utf-8') + str(A).encode('utf-8') + str(T3).encode('utf-8')).hexdigest()

    #print ("PID : ", PID, type(PID), "\n")
    #print ("Ay : ", Ay, type(Ay), "\n")

    h_PID_Ay_T3 = sha256(PID.encode('utf-8') + str(Ay).encode('utf-8') + str(T3).encode('utf-8')).hexdigest()
    
    #print ("h_PID_Ay_T3 : ", h_PID_Ay_T3, type (h_PID_Ay_T3), "\n")
    #print ("BI : ", BI, type (BI), "\n")
    
    M44 = xor_sha_strings (h_PID_Ay_T3, BI.encode('utf-8').hex() )

    M0_M2_M3_M4_B_T3 = M00 +"&"+ M22 +"&"+ M33 +"&"+ M44 +"&"+ convertTuple_str(B) +"&"+ str(T3)
    end1_comp_time = time.time ()

    veh_comp_time = end1_comp_time - start1_comp_time

    veh_socket.send(M0_M2_M3_M4_B_T3.encode('utf'))

    Z22_M55_Veri_T4 = veh_socket.recv(1024).decode() 

    Z22_M55_Veri_T4 = [ i for i in Z22_M55_Veri_T4.split('&')]

    start2_comp_time = time.time ()
    
    Z22 = str_to_tuple (Z22_M55_Veri_T4[0])
    M55 = Z22_M55_Veri_T4[1]
    Veri = Z22_M55_Veri_T4[2]
    T4 = float(Z22_M55_Veri_T4[3])

    if get_timestamp () - T4 < 4 :
        Z11 = scalar_mult (u, Z22)
        M55_star = sha256(ID_RSU.encode('utf-8') + convertTuple_str(Z11).encode('utf-8') + str(T4).encode('utf-8')).hexdigest()
        
        if M55 ==  M55_star :
            print ("Auth of RSU is SUCCESS ...")
            end2_comp_time = time.time ()
            veh_comp_time += end2_comp_time - start2_comp_time

            end_latency = time.time ()
            hand_latency = end_latency - start_latency

            print ("Veh Hand Comp Time : ", veh_comp_time)
            print ("Total Hand Latency : ", hand_latency)
            hand_sheet.row += [ veh_comp_time, hand_latency]
            hand_sheet.save_as ("BHAS_Hand_Veh_details.xlsx")

        else: 
            print ("M55 Check Failed")
    else :
        print ("T4 Timestamp Failed ")
else :
    print ("Reg details not found in Excel ")




