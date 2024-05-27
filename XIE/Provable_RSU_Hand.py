
import socket
import random # import randint 
import time 
import threading   
import pyexcel as pe
from hashlib import sha256 
import datetime
import collections 
import numpy as np

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

def eval_f_res_chal(chal) :

    # Define the coefficients of the polynomial, highest degree first
    coefficients = [5, 6, -4, 2, -3, 8, 1]  # Represents 5x^6 + 6x^5 - 4x^4 + 2x^3 - 3x^2 + 8x + 1

    # Create a numpy polynomial object
    polynomial = np.poly1d(coefficients)

    # Evaluate the polynomial at the given value
    resp = polynomial(chal)

    #print("The result of evaluating the polynomial at x =", chal, "is:", resp)
    return resp

def handle_client_veh(client_socket, client_address) : #, rsuj_socket) : 
    RID = "RSU2"
    
    chal = random.randint (100, 100000)
    K1 = "dbed60219a67946c65aef80f339a30628ea937c7d0a6a74a0498a37bae060f63"
    K2 = "01456dfb6ca4768469c9d77f726609cb17e9b444ec75dce74f0c163e9c4ffb1b"
    SK_Rt = 85704990221646376385997633937426299036441112639784931034249119205586685820338
    PK_Rt = (37453207132833339021865519235089049756159445688339513144542139268290255922179, 6128574117743178398953464494297838738260768996100453270950627783141308749043)
    zt = 28896912657901349689894586157299259653447038384704704939759214726597334795237
    Zt = (106415322946774620779972128495151441125342886528160775819643398608002266674986, 46276119434053460364772345509604491264866428019260025358513227732146803003502)
    PK_TA = (52506523913431230393416036805457983909698589858860059609212415864381991957950, 19071479616544346939693675182890645267870202405760988611448411175387051499115)
    yt = 86120928924370209682624776553142006962272898465898125781318808663738865612764

    auth_sheet = pe.get_sheet(file_name="Provable_RSU_Auth.xlsx")
    hand_sheet = pe.get_sheet(file_name="Provable_RSU_hand_details.xlsx")

    PID_AC_N2_T4 = client_socket.recv(1024).decode()  # receive auth_req
    start_latency = time.time ()
    
    PID_AC_N2_T4 = [ i for i in PID_AC_N2_T4.split('&')]

    PID = PID_AC_N2_T4[0]
    AC = PID_AC_N2_T4[1]
    N2 = PID_AC_N2_T4[2]
    T4 = PID_AC_N2_T4[3]

    print ("N2 Recvd from Veh :", N2, " =============\n")
    # print ("PID ", PID, type(PID))
    # print ("AC ", AC, type(AC))
    # print ("N2 ", N2, type(N2))
    # print ("T4 ", T4, type(T4))

    start_comp_time = time.time ()
    auth_flag = 0
    # Get details from BC { RID, PID, K_Virt, N1, lt, Jt, T3 } or excel sheet
    if get_timestamp () - float(T4) < 4: 
        print ("Time stamp T4 success ....")
        for row in auth_sheet :
            if row[1] == PID :
                print ("Found in Excel sheet ...")
                RID = row[0]
                K_ViRt = row[2]
                N1 = row[3]
                lt = row[4]
                Jt = row[5]
                T3 = row[6]
                h_SK_it = row[7]
                auth_flag = 1
                break

        # print ("Jt is : ", Jt, type(Jt))

        if auth_flag == 1 :
            print ("Auth Flag check success ...")
            Res = eval_f_res_chal(chal)
            K_Rsu = xor_sha_strings (K1, sha256(str(Res).encode('utf-8')).hexdigest() )
            y_SKr = xor_sha_strings (K2, sha256(str(Res).encode('utf-8') + K1.encode ('utf-8')).hexdigest() )

            h_K_Rsu = sha256(K_Rsu.encode("utf-8")).hexdigest()

            # print ("K_ViRt : ", K_ViRt, type(K_ViRt))
            # print ("h_K_Rsu : ", h_K_Rsu, type(h_K_Rsu))

            h_SK_ti = sha256 ( K_ViRt.encode('utf-8') + h_K_Rsu.encode('utf-8')).hexdigest()
            h_AC = sha256 ( AC.encode('utf-8') ).hexdigest()

            # print("^^^^^^^^^^^^^^^^^^^^^")
            # print ("PID : ", PID, type(PID))
            # print ("RID : ", RID, type(RID))
            # print ("h_SK_ti : ", h_SK_ti, type(h_SK_ti))
            # print ("T4 : ", T4, type(T4))
            # print ("h_AC : ", h_AC, type(h_AC))
            
            N2_temp = sha256 ( PID.encode('utf-8') + RID.encode ('utf-8') + h_SK_it.encode('utf-8') + str(T4).encode ('utf-8') + h_AC.encode('utf-8') ).hexdigest() 

            print ("N2_temp : ", N2_temp, "^^^^^^^^^^^^^^^^^^^^^")

            # print ("N1 : ", N1, type(N1))

            # print ("h_SK_ti : ", h_SK_ti, type(h_SK_ti))
            # print ("RID : ", RID, type(RID))
            # print ("PID : ", PID, type(PID))
            # print ("Jt : ", Jt, type(Jt))
            # print ("T3 : ", T3, type(T3))

            N1_h_SK_ti_RID_PID_Jt_T3 = int(sha256 ( N1.encode('utf-8') + h_SK_ti.encode('utf-8') + RID.encode ('utf-8') + PID.encode ('utf-8') + Jt.encode('utf-8') + str(T3).encode('utf-8')).hexdigest(), 16) 
            # print ("\n ####### N1_h_SK_ti_RID_PID_Jt : ", N1_h_SK_ti_RID_PID_Jt_T3)

            h_N1_Jt_temp = scalar_mult (N1_h_SK_ti_RID_PID_Jt_T3, str_to_tuple(Jt))
                    
            lt_P_check = point_add (PK_Rt, h_N1_Jt_temp)

            # print ("lt : ", lt, type(lt), "\n================\n")
            lt_P = scalar_mult (int(lt), curve.g)
            # print ("lt_P : ", lt_P, type(lt_P))
            # print ("lt_P_check : ", lt_P_check, type(lt_P_check))

            # print ("N2 : ", N2, type(N2))
            # print ("N2_temp : ", N2_temp, type(N2_temp))
            # print ("\n================\n")

            if N2 ==  N2_temp : #and lt_P == lt_P_check :
                print ("N2 Check SUCCCCCESS ...")
                jm, Jm = make_keypair ()
                T5 = get_timestamp ()

                h_Jm_AC_PID_RID_T4_T5 = int(sha256 ( convertTuple_str(Jm).encode('utf-8') + AC.encode('utf-8') + PID.encode ('utf-8') + RID.encode ('utf-8') + str(T4).encode('utf-8') + str(T5).encode('utf-8')).hexdigest(), 16) 

                h_Jm_AC_PID_RID_T4_T5_jm = h_Jm_AC_PID_RID_T4_T5 * jm
                lm = SK_Rt + h_Jm_AC_PID_RID_T4_T5_jm

                end_comp_time = time.time ()
                RSU_comp_time = end_comp_time - start_comp_time

                end_latency = time.time ()
                total_latency = end_latency - start_latency

                print ("RSU comp Time : ", RSU_comp_time)
                print ("RSU Latency : ", total_latency)

                # Send RID, PID, K_ViRt, N1, lt, T2, T3 in Blockchain                           

                # import sys
                # RID_size = sys.getsizeof (RID)
                # PID_size = sys.getsizeof (PID)
                # K_ViRt_size = sys.getsizeof (K_ViRt)
                # N1_size = sys.getsizeof (N1)
                # lt_size = sys.getsizeof (lt)
                # T3_size = sys.getsizeof (T3)

                # print ("RID_size : ", RID_size)
                # print ("PID_size : ", PID_size)
                # print ("K_ViRt_size : ", K_ViRt_size)
                # print ("N1_size : ", N1_size)
                # print ("lt_size : ", lt_size)
                # print ("T3_size : ", T3_size)

                # total_size = RID_size + PID_size + K_ViRt_size + N1_size + lt_size + T3_size 
                # print ("Total storage size at RSU Hand side : ", total_size)

                hand_sheet.row += [ RID, PID, K_ViRt, N1, lt, T3, RSU_comp_time, total_latency]
                hand_sheet.save_as ("Provable_RSU_hand_details.xlsx")

                print ("\n==== AUTH SUCCESS ==================\n")
            else :
                print ("N2 check failed ")
        else :
            print ("Auth details not found in Excel sheet ")
    else :
        print ("T4 Timestamp failed")

        

host = "192.168.20.200" # socket.gethostname() 192.168.20.200
print("RSU IP is ", host)
# print ("-------------------")
port = 6012  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together for veh comm
server_socket.listen(4) 

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
    if auth_ct == 31:
        '''
        for each in veh_threads :
            each.join()
        '''
        end = time.time()
        print ("booooooo------------------------ooooooom")
        print ("Total time for auth latency is ", (end-start)*10**3, " m.sec")
        print ("Breaking ")
        break