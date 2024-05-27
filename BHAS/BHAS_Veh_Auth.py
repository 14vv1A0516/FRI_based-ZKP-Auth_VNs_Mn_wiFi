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

ID = sys.argv[1] #"UHDD3KC"  # sys.argv[1] # F2IPFKP  LI78DJK  8IQYQ9I
reg_sheet1 = pe.get_sheet (file_name= "BHAS_Reg_Veh_details.xlsx")
auth_sheet1 = pe.get_sheet (file_name= "BHAS_Auth_Veh_details.xlsx")

q = 103
ID_RSU = "RSU1"
auth_flag = 0
reg_flag = 0
Pub_RSU = (52506523913431230393416036805457983909698589858860059609212415864381991957950, 19071479616544346939693675182890645267870202405760988611448411175387051499115)

veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('192.168.10.100', 6012) # 192.168.10.100

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
        R_excel = row[5]
        DID = row[6]
        reg_flag = 1 
        print ("  VID : ", ID, "match found ...")
        break

'''
print ("ID : ", ID, type(ID))
print ("PIN : ", PIN, type(PIN))
print ("PID : ", PID, type(PID))
print ("A : ", A, type(A))
print ("Q : ", Q, type(Q))
print ("R_excel : ", R_excel, type(R_excel))
print ("DID : ", DID, type(DID), "\n")
'''
start_latency = time.time ()
start1_comp_time = time.time ()

if reg_flag == 1 :

    print ("Reg details found in Excel")
    h_ID_PIN = sha256(ID.encode('utf-8') + PIN.encode('utf-8')).hexdigest()
    #print ("h_ID_PIN : ", h_ID_PIN, type(h_ID_PIN), "\n")

    r = xor_sha_strings (h_ID_PIN, A)
    h_r = sha256(r.encode('utf-8') ).hexdigest()
    BI = xor_sha_strings (Q, h_r)
    #print ("r : ", r, type(r))
    #print ("h_r : ", h_r, type(h_r))
    #print ("BI : ", BI, type(BI), "\n")

    R = sha256(PID.encode('utf-8') + BI.encode('utf-8') + Q.encode('utf-8')).hexdigest()
    #print ("R : ", R, type(R))

    if R == R_excel :
        print ("R check SUccess ")

        v = random.randrange (1, 103)

        X = scalar_mult (v, Pub_RSU)
        #print ("!!!!!!!!!!! X : ", X, type(X), "\n")

        Xx = X[0]
        Xy = X[1]

        Y = scalar_mult (v, curve.g)

        M0 = xor_sha_strings (DID, ID_RSU.encode('utf-8').hex())

        #print ("M0 : ", M0, type(M0), "\n")
        T1 = get_timestamp ()

        #print ("^^^^^^^^^\nDID : ", DID, type (DID), "\n")
        #print ("Xx : ", Xx, type (Xx), "\n")

        #print ("T1 : ", T1, type (T1), "\n^^^^^^^^^^^^^")

        M1 = sha256(DID.encode('utf-8') + str(Xx).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()
        M2 = xor_sha_strings (PID, M1)

        #print ("M1 : ", M1, type(M1), "\n")
        #print ("M2 : ", M2, type(M2), "\n")

        #print ("============\nPID : ", PID, type(PID), "\n")
        #print ("ID_RSU : ", ID_RSU, type(ID_RSU), "\n")
        #print ("X : ", X, type(X), "\n")
        #print ("T1 : ", T1, type(T1), "\n================")

        M3 = sha256(PID.encode('utf-8') + ID_RSU.encode('utf-8') + convertTuple_str(X).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()

        M4 = sha256(PID.encode('utf-8') + str(Xy).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()
        M4 = xor_sha_strings (M4, BI)

        #print ("M3 : ", M3, type(M3), "\n")
        #print ("M4 : ", M4, type(M4), "\n")

        M0_M2_M3_M4_Y_T1 = M0 +"&"+ M2 +"&"+ M3 +"&"+ M4 +"&"+ convertTuple_str(Y) +"&"+ str(T1)
        end1_comp_time = time.time ()

        veh_comp_time = end1_comp_time - start1_comp_time

        veh_socket.send(M0_M2_M3_M4_Y_T1.encode('utf'))
        Z2_M5_Veri_T2 = veh_socket.recv(1024).decode() 

        start2_comp_time = time.time ()
        Z2_M5_Veri_T2 = [ i for i in Z2_M5_Veri_T2.split('&')]

        Z2 = str_to_tuple(Z2_M5_Veri_T2[0])
        M5 = Z2_M5_Veri_T2[1]
        Veri = Z2_M5_Veri_T2[2]
        T2 = float(Z2_M5_Veri_T2 [3])

        if get_timestamp () - T2 < 4:
            Z1 = scalar_mult (v, Z2)

            M5_star = sha256(ID_RSU.encode('utf-8') + convertTuple_str(Z1).encode('utf-8') + str(T2).encode('utf-8')).hexdigest()
            if M5 == M5_star :
                print ("RSU Auth Done")
                end2_comp_time = time.time ()

                veh_comp_time +=  end2_comp_time - start2_comp_time
                end_latency = time.time ()

                Auth_latency = end_latency - start_latency

                # import sys
                # ID_size = sys.getsizeof (ID)
                # BI_size = sys.getsizeof (BI)

                # total_size = ID_size + BI_size
                # print ("total size for veh Auth : ", total_size)
                
                auth_sheet1.row += [ ID, BI, veh_comp_time, Auth_latency]
                auth_sheet1.save_as ("BHAS_Auth_Veh_details.xlsx")

                print ("Veh Comp Time : ", veh_comp_time)
                print ("Auth Latency : ", Auth_latency)
            else :
                print ("M5 Check Failed ...")
        else :
            print ("T2 Timestamp check Failed")
    else :
        print ("R Excel Fetch failed")
else :
    print ("Veh Reg details not found in Excel sheet ...")




        



         

