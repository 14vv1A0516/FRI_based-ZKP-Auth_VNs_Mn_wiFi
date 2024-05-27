import socket
import threading  
import time
import random # import randint
from hashlib import sha256 
import collections
import pyexcel as pe
from ecdsa import SigningKey, SECP256k1
import datetime 

#sj = '190f4ebc6096e310a3a80b10b1e2a361f47aa014a842979772c25b148fb7b29b'
sj = 70697168185318818877363624420592789532113543602228244263078048953734882874292
P = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)
k = 'd185b023d9e93cc9b78a4a2c97b708ccd94f70cab5031116db29b8ec946b8919'

RSU_sign_key = SigningKey.generate(curve=SECP256k1)
RSU_ver_key = RSU_sign_key.verifying_key
print ("Priv key bfr hex is ", type(RSU_sign_key))
print ("Pub key bfr hash is ", type(RSU_ver_key))

RSU_sign_key_hex = 'b37dc350a4d29a2e22c51b7afa5ad1f3fe68ad2b7d6cb4ef1cf5f26cd5a33e52' #RSU_sign_key.to_string().hex()
RSU_ver_key_hex = '81c1fbb71519f2939145ae7fbdc29467b995e4677148793bef6cda91706fd36af14009df27219f7a64f3a692135a29bf10242ee95166407f1082a5bceab7ee60' #RSU_ver_key.to_string().hex()

print ("Priv key aftr hex is ", RSU_sign_key_hex)
print ("Pub key aftr hex is ", RSU_ver_key_hex)

print ("RSU sign key is ", RSU_sign_key)
print ("RSU ver key is ", RSU_ver_key)

global prev_nonce 
global current_nonce
prev_nonce = -1

def get_timestamp() :
    ct = datetime.datetime.now()
 
    ts = ct.timestamp()
    return ts

def xor_sha_strings( s, t): 
    s = bytes.fromhex(s)
    t = bytes.fromhex(t)

    res_bytes = bytes(a^b for a,b in zip(s,t))
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
def handle_client_veh( veh_socket):
      
    IDj = 'RSUID123456'
    
    print ("Into Handle client for conn ")
    TA_sheet = pe.get_sheet (file_name = "SON_TA_Reg.xlsx")
    auth_sheet = pe.get_sheet (file_name = "SON_RSU_Auth.xlsx")

    data = veh_socket.recv(1024).decode()
    auth1_comp_start_time = time.time()

    Pi = []
    values = [str(i) for i in data.split('#')]
    #print ("Values are ", values)
    M1 = values[0]
    M2 = values[1]

    #print ("Val[0] is ", values[2])
    #print ("Val[1] is ", values[3])
    Pi.append(int(values[2]))
    Pi.append(int(values[3]))

    Pi = tuple(Pi)
    #print ("Tuple is ", Pi)
    # Pi = h
    T1 = float(values[4])

    #print ("Received Pi is ", type(Pi[0]))
    #print ("Recvd time stamp is ", T1)
    curr_time = get_timestamp ()

    if curr_time-T1 < 5 :

        Pij = scalar_mult(sj, Pi)
    
        #print ("Pij is ", Pij)

        #hRIDk = 'd234968b375fbb7e558378926b6fe435518ece226a1d748a210058ac0e9373a7' # from BC
        k = 'd185b023d9e93cc9b78a4a2c97b708ccd94f70cab5031116db29b8ec946b8919'
        temp_h = sha256(IDj.encode('utf-8') + str(Pij).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()
        RID = xor_sha_strings (M1, temp_h)

        # print ("\n=================RIDi : ", RID, "\nk is ", k, "\n===============")

        hridk = sha256(RID.encode('utf-8') + k.encode('utf-8')).hexdigest()
        print ("Computed hridk is ", hridk, "\n")
        #get_BC_hRIDk = reg_cont_instance.functions.retrieve_reg_details(hridk).call()


        row_flag = 0
        for row in TA_sheet :
            if row[3] == hridk :
                row_flag = 1
                get_BC_hRIDk = row[3]
                print ("hridk matched and extracted ...")
                break

        #print ("hridk recvd from BC is ", get_BC_hRIDk)

        if get_BC_hRIDk == hridk and row_flag == 1:
            print ("Blockchain data matched ...")
            # Check if BC exists in BC
            match_m2 = sha256(RID.encode('utf-8') + str(Pij).encode('utf-8') + str(T1).encode('utf-8')).hexdigest()

            if M2 == match_m2 :
                print ("M2 matched ... ")
                bj = random.randint(100, 100000)
                nj = random.randint(100, 100000)
                T2 = get_timestamp()
                Qij = scalar_mult(bj, Pi)
                Qj = scalar_mult(bj, P)

                #print ("Qij is ", Qij)
                #print ("Qj is ", Qj) 

                temp_h = sha256(str(nj).encode('utf-8') + IDj.encode('utf-8') + k.encode('utf-8')).hexdigest()    
                TIDi = xor_sha_strings (RID, temp_h)
                #print("TIDi is ", TIDi)

                M3 = xor_sha_strings (sha256(str(Qij).encode('utf-8') + RID.encode('utf-8')).hexdigest(), TIDi)
                SKij = sha256(str(Qij).encode('utf-8') + TIDi.encode('utf-8') + RID.encode('utf-8')).hexdigest()
                M4 = sha256(SKij.encode('utf-8') + str(T2).encode('utf-8')).hexdigest()
            
                msg1 = M3 + "#"+ M4 +"#"+ str(Qj[0]) +"#"+ str(Qj[1]) +"#"+ str(T2)
                auth1_comp_end_time = time.time ()

                # import sys
                # M3_size = sys.getsizeof (M3)
                # M4_size = sys.getsizeof (M4)
                # Qj0_size = sys.getsizeof (str(Qj[0]))
                # Qj1_size = sys.getsizeof (str(Qj[1]))
                # T2_size = sys.getsizeof (str(T2))

                # print ("M3_size : ", M3_size)
                # print ("M4_size : ", M4_size)
                # print ("Qj0_size : ", Qj0_size)
                # print ("Qj1_size : ", Qj1_size)
                # print ("T2_size : ", T2_size)


                # total_size = M3_size + M4_size + Qj0_size + Qj1_size + T2_size

                # print ("^^^^^^^ Total comm cost for Auth at RSU : ", total_size)
                veh_socket.send(msg1.encode('utf')) 

                auth_comp_time = auth1_comp_end_time - auth1_comp_start_time
                auth2_comp_start_time = time.time ()
                msg_hash = sha256(TIDi.encode('utf-8') + RID.encode('utf-8') + str(nj).encode('utf-8')).digest()

                #print ("msg hash type is ", msg_hash)  # bytes
                #print ("sign key is ", RSU_sign_key_hex)

                sign_key_bytes = bytes.fromhex(RSU_sign_key_hex)

                signing_key = SigningKey.from_string(sign_key_bytes, curve=SECP256k1)

                # Sign the message using the signing key
                signature = signing_key.sign(msg_hash)
                
                auth2_comp_end_time =  time.time ()

                auth_comp_time += auth2_comp_end_time - auth2_comp_start_time

                #sheet = pe.get_sheet (file_name = "SON_Store_auth_details.xlsx")
                #sheet.row += [TIDi, nj, RID]
                #sheet.save_as ("SON_Store_auth_details.xlsx")

                #print ("Msg decoded is ", msg_hash_bytes.decode())
                # print ("Uploading in BC \n TIDi : ", TIDi, "nj : ", nj, "IDj : ", IDj, "Signature : ", signature.hex)
                print ("Authen successful ....\n")
                
                # print ("------- Signature : ", signature, type (signature))

                auth_sheet.row += [TIDi, nj, IDj, signature.hex(), auth_comp_time]
                auth_sheet.save_as ("SON_RSU_Auth.xlsx")

                print ("Total time for Auth Comp at RSU is ", auth_comp_time , " sec")
                print ("************** DONE ***********************\n\n")
                # upload in BC TIDi, nj, IDj, signature.hex
                veh_socket.close()
            else :
                print ("M2 Mismatch .....")
        else :
            print ("BC data mismatch .... quit")
                
host = "192.168.10.100" # socket.gethostname() 192.168.10.100
print("RSU IP is ", host)
# print ("-------------------")
port = 6012  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together for veh comm
server_socket.listen(40)  

i = 0
auth_ct = 0

while True :

    print ("Waiting for next Veh conn ..")
    veh_conn, client_address = server_socket.accept()

    client_thread2 = threading.Thread (target=handle_client_veh, args= (veh_conn, )) #, rsuj_socket))
    client_thread2.start()
    client_thread2.join() 

    i = i + 1