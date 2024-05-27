import socket
import threading
import time 
import random # import randint
from hashlib import sha256 
import collections 
import pyexcel as pe
from ecdsa import SigningKey, SECP256k1, VerifyingKey
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


RSU_sign_key = SigningKey.generate(curve=SECP256k1)
RSU_ver_key = RSU_sign_key.verifying_key

print ("RSU sign key is ", RSU_sign_key)
print ("RSU ver key is ", RSU_ver_key)
print ("---------------------------\n")

RSU_sign_key = SigningKey.generate(curve=SECP256k1)
RSU_ver_key = RSU_sign_key.verifying_key
print ("Priv key bfr hex is ", type(RSU_sign_key))
print ("Pub key bfr hash is ", type(RSU_ver_key))

RSU_sign_key_hex = RSU_sign_key.to_string().hex()
RSU_ver_key_hex = RSU_ver_key.to_string().hex()
print ("Priv key aftr hex is ", RSU_sign_key_hex)
print ("Pub key aftr hex is ", RSU_ver_key_hex)

print ("RSU sign key is ", RSU_sign_key)
print ("RSU ver key is ", RSU_ver_key)

def get_timestamp() :
    # ct stores current time
    ct = datetime.datetime.now()
    print("current time:-", ct)
 
    # ts store timestamp of current time
    ts = ct.timestamp()
    print("timestamp:-", ts)
    return ts

def xor_sha_strings( s, t): 
    s = bytes.fromhex(s)
    t = bytes.fromhex(t)

    res_bytes = bytes(a^b for a,b in zip(s,t))
    return res_bytes.hex()


def handle_client_veh( veh_socket):  # give RID as input

    hand_sheet = pe.get_sheet (file_name = "SON_RSU_Hand.xlsx")

    ver_key = "81c1fbb71519f2939145ae7fbdc29467b995e4677148793bef6cda91706fd36af14009df27219f7a64f3a692135a29bf10242ee95166407f1082a5bceab7ee60" 
    ver_key_bytes = bytes.fromhex(ver_key)
    print ("Into Handle client for conn ", veh_socket)
    data = veh_socket.recv(1024).decode()
    auth_sheet = pe.get_sheet (file_name = "SON_RSU_Auth.xlsx")

    # Input : TIDi, nj, IDj, signature
    k = 'd185b023d9e93cc9b78a4a2c97b708ccd94f70cab5031116db29b8ec946b8919' # fix  

    print ("data recvd : ", data)
    values = [str(i) for i in data.split(',')]
    TIDi = values[0]
    M5 = values[1]
    M6 = values[2]
    T3 = float (values[3])
    curr_time = get_timestamp ()

    IDk = "RSU2_hand"

    row_flag = 0
    for row in auth_sheet :
        if row[0] == TIDi :
            nj = row[1]
            IDj = row[2]
            signature = row[3]
            row_flag = 1
            print ("ID matched and extracted ...")
            break

    hand1_comp_start_time = time.time ()
    
    if row_flag == 1 :
        #RIDi = row[1]
        print ("Excel sheet details found")

        if curr_time - T3 < 5 :
            #get_TID_data = auth_cont_inst.functions.retrieve_auth_details(TIDi).call()
            #print ("Data from BC is ", get_TID_data)

            # Get data from BC
            hnIDk = sha256(str(nj).encode('utf-8') + IDj.encode('utf-8') + k.encode('utf-8')).hexdigest()

            RIDi = xor_sha_strings(TIDi, hnIDk)
            #print ("RIDc is ", RIDic)

            BChash = sha256(str(TIDi).encode('utf-8') + RIDi.encode('utf-8') + str(nj).encode('utf-8')).digest()
            #BChash = bytes.fromhex(BChash)

            sign_in_bytes = bytes.fromhex(signature) # .hex()
            #print ("Current computed sign hash is ", sign_in_bytes)
        
            #print ("BC hash is ", BChash)
                
            ver_key_obj = VerifyingKey.from_string(ver_key_bytes, curve=SECP256k1)

            #print ("Ver key in bytes is ", ver_key_bytes)
            is_valid = ver_key_obj.verify(sign_in_bytes, BChash)
            
            #print("Is valid?", is_valid)

            if is_valid : # BChash == sign_hash :
                print ("BC hashes matched ...")
                hridtid =  sha256(RIDi.encode('utf-8') + TIDi.encode('utf-8') + str(IDk).encode('utf-8')+ str(T3).encode('utf-8')).hexdigest()
                ci = xor_sha_strings (M5, hridtid)
                #print ("ci is ", ci)

                check_M6 = sha256(ci.encode('utf-8') + RIDi.encode('utf-8') + TIDi.encode('utf-8')).hexdigest()
                if M6 == check_M6 :
                    print ("M6 matched ...")
                    ck = random.randint(100, 100000)
                    nk = random.randint(100, 100000)
                    T4 = get_timestamp()

                    hnkidk = sha256(str(nk).encode('utf-8') + IDk.encode('utf-8') + k.encode('utf-8')).hexdigest()
                    TIDnew = xor_sha_strings(RIDi,  hnkidk)
                    hcirid = sha256(ci.encode('utf-8') + RIDi.encode('utf-8')).hexdigest()
                    M7 = xor_sha_strings(TIDnew,  hcirid)
                    hcitidrid = sha256(ci.encode('utf-8')+ TIDnew.encode('utf-8')+ RIDi.encode('utf-8')).hexdigest()
                    ck = str(ck).zfill(64)
                    M8 = xor_sha_strings(ck, hcitidrid)

                    SKik = sha256(ck.encode('utf-8')+ ci.encode('utf-8')+ TIDnew.encode('utf-8')+ RIDi.encode('utf-8')).hexdigest()
                    M9 = sha256(SKik.encode('utf-8')+ str(T4).encode('utf-8')).hexdigest()
                    msg1 = M7+ ","+ M8+ ","+ M9+ ","+ str(T4)
                    hand1_comp_end_time = time.time ()

                    # import sys
                    # M7_size = sys.getsizeof (M7)
                    # M8_size = sys.getsizeof (M8)
                    # M9_size = sys.getsizeof (M9)
                    # T4_size = sys.getsizeof (str(T4))

                    # print ("M7_size : ", M7_size)
                    # print ("M8_size : ", M8_size)
                    # print ("M9_size : ", M9_size)
                    # print ("T4_size : ", T4_size)

                    # total_size = M7_size + M8_size + M9_size + T4_size

                    # print ("^^^^^^^ Total comm cost for Hand at RSU : ", total_size)

                    hand_comp_time = hand1_comp_end_time - hand1_comp_start_time

                    veh_socket.send(msg1.encode('utf'))
                    hand2_comp_start_time = time.time ()
                    msg_hash = sha256(TIDnew.encode('utf-8') + RIDi.encode('utf-8') + str(nk).encode('utf-8')).hexdigest()
                    #print ("msg hash is ", msg_hash)

                    msg_hash_bytes = str.encode(msg_hash)

                    signature = RSU_sign_key.sign(msg_hash_bytes)
                    print ("SIgn is ", signature.hex)
                    is_valid = RSU_ver_key.verify (signature, msg_hash_bytes)
                    # print ("is valid ", is_valid)
                    #print ("Msg decoded is ", msg_hash_bytes.decode())

                    hand2_comp_end_time = time.time ()
                    hand_comp_time += hand2_comp_end_time - hand2_comp_start_time

                    hand_sheet.row += [ hand_comp_time]
                    hand_sheet.save_as ("SON_RSU_Hand.xlsx")

                    print ("Hand comp time at RSU : ", hand_comp_time)
                    print ("handover Auth successful ...\n")
                    print ("************ DONE ********* ...\n")
                else :
                    print ("M6 does not match") 
            else :
                print ("BC hashes do not match")
        else :
            print ("T3 check Failed ...")
    else :
        print ("Excel sheet details not found")
        
host = "192.168.20.200" # socket.gethostname() 192.168.20.200
print("RSU IP is ", host)
# print ("-------------------")
port = 6012  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together for veh comm
server_socket.listen(40) 

i = 0

while True :

    veh_conn, client_address = server_socket.accept()
    
    client_thread2 = threading.Thread (target=handle_client_veh, args= (veh_conn,  )) #, rsuj_socket))
    client_thread2.start()
    
    client_thread2.join()

    i = i + 1