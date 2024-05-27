
import socket
import time 
import random # import randint
import time
from hashlib import sha256  
import collections
import pyexcel as pe  
import datetime
import sys

def get_timestamp() :
    ct = datetime.datetime.now()
 
    ts = ct.timestamp()
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
    print ("str returning is ", str1)
    # return string
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

server_address = ('192.168.10.100', 6012) # 192.168.10.100
veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server's address and port

conn_flag = 0
print ("Trying to connect ...")

while conn_flag == 0: 
    try :
        veh_socket.connect(server_address)
        print(f"Connected to {server_address}") 
        conn_flag = 1
    except :
        print ("Failed ... Trying to connect again") 


#Pj = (hex(5004551491635526979949013210228172335096988664199489580314557584289929163579), hex(70620065914923519059686305151984054453339921207029706643584790926109949938845))
Pj = (81799720190750772883998351673452111198805322623148698779815673189217354960557, 63453719299546664706295282443298248360915397730763986116910871256310735888969)

ID = sys.argv[1] # sys.argv[1]  only I/P
auth_sheet = pe.get_sheet (file_name = "SON_Veh_Auth.xlsx")

print ("Input given is ", ID)
reg_sheet = pe.get_sheet (file_name = "SON_Reg_Veh.xlsx")

row_flag = 0
for row in reg_sheet :
    if row[0] == ID :
        row_flag = 1
        print ("ID matched and extracted ...")
        break

auth_start_latency = time.time ()
auth1_comp_start_time = time.time ()

if row_flag == 1 :
    PWD = row[1] 
    A = row[2]
    B = row[3]
    C = row[4] 

    #print ("ID is ", ID)
    #print ("PWD is ", PWD)
    #print ("A, B, C is ", A, B, C)

    HPW = sha256(ID.encode('utf-8') + PWD.encode('utf-8')).hexdigest() # ID and PWD
    #print ("HPW is ", HPW)

    r = xor_sha_strings (A, HPW)
    #print ("ri is ", r)

    temp_hr = sha256(r.encode('utf-8')).hexdigest()
    x = xor_sha_strings (B, temp_hr)
    #print("xi is ", x)

    temp_hx = sha256(x.encode('utf-8')).hexdigest()
    RPW = xor_sha_strings (HPW, temp_hx)
    #print ("RPW is ", RPW)

    RID = sha256(ID.encode('utf-8') + RPW.encode('utf-8') + r.encode('utf-8')).hexdigest()
    print ("RID is ", RID)
    temp_h = sha256(RID.encode('utf-8') + x.encode('utf-8')).hexdigest()

    #print ("temp_h is ", temp_h)

    if C == sha256(temp_h.encode('utf-8')).hexdigest() :
        print ("C matching is ", C)
        b = random.randint(100, 100000)

        sj_int = int(r) # , base=16) # r
        #print ("---Pj is ", Pj)
        #print ("sj int is ", type(sj_int))
        rb = sj_int*b
        Pij = scalar_mult(rb, Pj) # r*b*Pj 
        Pi = scalar_mult(rb, curve.g) # r*b*P

        #print ("Pij is ", Pij)
        #print ("Pi is ", Pi)
        IDj = 'RSUID123456'
        T1 = get_timestamp()
        temp_h = sha256(IDj.encode('utf-8') + str(Pij).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()
        M1 = xor_sha_strings (RID, temp_h)
        M2 = sha256(RID.encode('utf-8') + str(Pij).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()
        #print ("M1 is ", M1)
        #print ("M2 is ", M2)

        msg1 = M1 + "#"+ M2 +"#"+ str(Pi[0]) +"#"+ str(Pi[1]) +"#"+ str(T1) 

        # import sys
        # M1_size = sys.getsizeof (M1)
        # M2_size = sys.getsizeof (M2)
        # Pi0_size = sys.getsizeof (str(Pi[0]))
        # Pi1_size = sys.getsizeof (str(Pi[1]))
        # T1_size = sys.getsizeof (str(T1))

        # print ("M1_size : ", M1_size)
        # print ("M2_size : ", M2_size)
        # print ("Pi0_size : ", Pi0_size)
        # print ("Pi1_size : ", Pi1_size)
        # print ("T1_size : ", T1_size)

        # total_size = M1_size + M2_size + Pi0_size + Pi1_size + T1_size

        # print ("^^^^^^^ Total comm cost for Auth at Veh : ", total_size)
        #print ("msg1 sent to RSU is ", msg1)

        auth1_comp_end_time = time.time ()
        auth_comp_time = auth1_comp_end_time - auth1_comp_start_time

        veh_socket.send(msg1.encode('utf'))  # send  M1, M2, Pi, T1

        data = veh_socket.recv(1024).decode()  # receive M3, M4, Qj,T2
        auth2_comp_start_time = time.time ()

        values = [str(i) for i in data.split('#')]

        M3 = values[0]
        M4 = values[1]
        Qj = []
        # check time stamp time
        T2 = float(values[4])
        '''
        print ("----------------------------\n")
        print ("M3 is ", M3)
        print ("M4 is ", M4)

        print ("Qj point is ", Qj)
        print ("T2 is ", T2)
        '''
        curr_time = get_timestamp ()
        if curr_time - T2 < 5 :
            Qj.append(int(values[2]))
            Qj.append(int(values[3]))

            Qj = tuple(Qj)
            #print ("Tuple is ", Pi)
            Qij = scalar_mult(rb, Qj) 

            TIDi = xor_sha_strings (M3, sha256(str(Qij).encode('utf-8') + RID.encode('utf-8')).hexdigest() )
            SKij = sha256(str(Qij).encode('utf-8') + str(TIDi).encode('utf-8') + RID.encode('utf-8')).hexdigest()
            #print ("TID is ", TIDi)

            if M4 == sha256(SKij.encode('utf-8') + str(T2).encode('utf-8')).hexdigest() :
                print ("Authentication successful")
                auth2_comp_end_time = time.time ()
                auth_end_latency = time.time ()

                auth_latency = auth_end_latency - auth_start_latency
                
                auth_comp_time += auth2_comp_end_time - auth2_comp_start_time
                auth_sheet.row += [TIDi, RID, auth_comp_time, auth_latency]
                auth_sheet.save_as ("SON_Veh_Auth.xlsx")
                
                print ("Total Auth comp time is ", auth_comp_time, " sec")
                print ("Total Auth Latency is ", auth_latency, " sec")

            else :
                print ("M4 mismatch ...")
        else :
            print ("Time stamp check failed .. Possible Session key attack ")
    else :
        print ("C not matching ......")
else :
    print ("ID not found, Authentication not possible")

veh_socket.close ()