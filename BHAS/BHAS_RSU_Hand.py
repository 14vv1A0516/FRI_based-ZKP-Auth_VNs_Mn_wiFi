
import socket 
import random # import randint 
import time 
import threading 
import pyexcel as pe
from hashlib import sha256
import datetime
import collections

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

def str_to_tuple (inp_str) :
    split_values = inp_str.strip('()').split(',')

    # Convert each string value to an integer and create a tuple
    tuple_of_integers = tuple(int(value.strip()) for value in split_values)
    return tuple_of_integers

def handle_client_veh(client_socket, client_address) : #, rsuj_socket) : 

    hand_sheet = pe.get_sheet(file_name="BHAS_Hand_RSU_details.xlsx")

    M0_M2_M3_M4_B_T3 = client_socket.recv(1024).decode()  # receive auth_req
    
    start_comp_time = time.time ()
    M0_M2_M3_M4_B_T3 = [ i for i in M0_M2_M3_M4_B_T3.split('&')]
    M00 = M0_M2_M3_M4_B_T3[0]
    M22 = M0_M2_M3_M4_B_T3[1]
    M33 = M0_M2_M3_M4_B_T3[2]
    M44 = M0_M2_M3_M4_B_T3[3]
    B = str_to_tuple( M0_M2_M3_M4_B_T3[4])
    T3 = float(M0_M2_M3_M4_B_T3[5])

    # print ("M00 : ", M00, type(M00), "\n")
    # print ("M22 : ", M22, type(M22), "\n")
    # print ("M33 : ", M33, type(M33), "\n")
    # print ("M44 : ", M44, type(M44), "\n")
    # print ("B : ", B, type(B), "\n")
    # print ("T3 : ", T3, type(T3), "\n")

    if get_timestamp () - T3 < 4 :
        print ("T4 timestamp check success ..")
        A= scalar_mult (Pri_RSU, B)
        #print ("A : ", A, type(A), "\n")

        Ax = A[0]
        Ay = A[1]
        DID = xor_sha_strings (M00, ID_RSU.encode('utf-8').hex())

        M11 = sha256(DID.encode('utf-8') + str(Ax).encode('utf-8') + str(T3).encode('utf-8') ).hexdigest()
        #print ("M11 : ", M11, type(M11))
        PID = xor_sha_strings (M22, M11)

        #print ("PID : ", PID, type(PID))
        
        M33 = sha256(PID.encode('utf-8') + ID_RSU.encode('utf-8') + convertTuple_str(A).encode('utf-8') + str(T3).encode('utf-8')).hexdigest()
        #print ("M33 : ", M33)
        #print ("DID : ", DID, type(DID))


        if M33 == M33:
            print ("M33 matched ...")
            BI_temp = sha256(PID.encode('utf-8') + str(Ay).encode('utf-8') + str(T3).encode('utf-8')).hexdigest()
            BI = xor_sha_strings (BI_temp, M44)

            # Get Init Auth details from Excel or BC
            c = random.randrange (1, 103)

            Z11 = scalar_mult (c, B)
            Z22 = scalar_mult (c, curve.g)
            T4 = get_timestamp ()

            M55 = sha256(ID_RSU.encode('utf-8') + convertTuple_str(Z11).encode('utf-8') + str(T4).encode('utf-8')).hexdigest()
            SK = sha256(convertTuple_str(Z11).encode('utf-8') + BI.encode('utf-8')).hexdigest()

            Veri = sha256(SK.encode('utf-8') + str(Ax).encode('utf-8')).hexdigest()
            # print ("Z22 : ", Z22, type(Z22), "\n")
            # print ("M55 : ", M55, type(M55))
            # print ("DID : ", DID, type(DID))

            Z22_M55_Veri_T4 = convertTuple_str(Z22) + "&"+ M55 + "&"+ Veri + "&"+ str(T4)
            end_comp_time = time.time ()
            RSU_comp_time = end_comp_time - start_comp_time
            client_socket.send(Z22_M55_Veri_T4.encode('utf'))

            print ("Total Hand Auth at RSU : ", RSU_comp_time, "\n=========================\n")
            hand_sheet.row += [ RSU_comp_time]

            hand_sheet.save_as ("BHAS_Hand_RSU_details.xlsx")

        else :
            print ("M33 not matched ...")
    else :
        print ("T3 timestamp check failed  ")

          
Pri_RSU = 28896912657901349689894586157299259653447038384704704939759214726597334795237
Pub_RSU = (106415322946774620779972128495151441125342886528160775819643398608002266674986, 46276119434053460364772345509604491264866428019260025358513227732146803003502)
ID_RSU = "RSU2"
 
host = "192.168.20.200" # socket.gethostname() 192.168.20.200
print("RSU IP is ", host)
# print ("-------------------")
port = 6012  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together for veh comm
server_socket.listen(40) 

i = 0
rsu_j = 0
auth_ct = 0

while True :

    if rsu_j == 0:
        print ("Thread for RSU j started ...")
        #client_thread1 = threading.Thread (target=handle_rsu_j, args= (rsuj_socket,))
        #client_thread1.start()
        rsu_j = 1

    veh_conn, client_address = server_socket.accept()
    
    if auth_ct == 0:
        start = time.time()
        print ("Time started")
    auth_ct = auth_ct + 1
    
    #print ("\nRecvd conn from veh ", veh_conn, client_address) 

    client_thread2 = threading.Thread (target=handle_client_veh, args= (veh_conn, client_address, )) #, rsuj_socket))
    client_thread2.start()
    # veh_threads.append(client_thread2)
    
    # start = time.time()
    client_thread2.join()

    #print ("Thread  ", i ,"started")
    #end = time.time()
    #print ("Total time for auth latency is ", (end-start)*10**3, " m.sec")

    i = i + 1
    if auth_ct == 30 :
        '''
        for each in veh_threads :
            each.join()
        '''
        end = time.time()
        print ("booooooo------------------------ooooooom")
        print ("Total time for auth latency is ", (end-start)*10**3, " m.sec")
        print ("Breaking ")
        break