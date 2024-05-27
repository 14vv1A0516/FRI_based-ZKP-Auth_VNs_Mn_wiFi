
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

    # print("The result of evaluating the polynomial at x =", chal, "is:", resp)
    return resp

def handle_client_veh(client_socket, client_address) : #, rsuj_socket) : 

    chal = random.randint (100, 100000)
    K1 = "74bc7ec38c6c724f25f1d7d2b9e1e61fbe6bc744c5b133715776145c91e7b5d9"
    K2 = "22e2bbbb9963d3340ac66e47dda1c8c9e936f3fe33f1419570200e07c0606be2"
    RID = "RSU1"
    SK_Rt = 55693636265582633547250325709343604133181924941441483722434614413440698775647
    PK_Rt = (53904887598037775061384661478667903563591540154136725910453540995709649842519, 88740702314748168147052938448749793303546580626336492001351766991347516498615)
    zt = 49147663601457822990889827367329936758956937633046902032058101896578144559878
    Zt = (2959716851119288862211622977008189861184327370367794918014840491536019771352, 24916489272082616250415904107688059381337864200569385515868851478016982485432)
    PK_TA = (52506523913431230393416036805457983909698589858860059609212415864381991957950, 19071479616544346939693675182890645267870202405760988611448411175387051499115)
    yt = 86120928924370209682624776553142006962272898465898125781318808663738865612764

    auth_sheet = pe.get_sheet(file_name="Provable_RSU_Auth.xlsx")
    auth_req_VPID = client_socket.recv(1024).decode()  # receive auth_req
    
    start1_comp_time = time.time ()
    
    # print ("auth_req_VPID : ", auth_req_VPID, "\n")
    PID_A_D_PK_V_c_T1 = [ i for i in auth_req_VPID.split('&')]
    PID = PID_A_D_PK_V_c_T1[0]
    A_str = PID_A_D_PK_V_c_T1[1]
    A = [ int(i) for i in PID_A_D_PK_V_c_T1[1].split(',')]
    D_str = PID_A_D_PK_V_c_T1[2]
    D = [ int(i) for i in PID_A_D_PK_V_c_T1[2].split(',') ]
    PK_V_str = PID_A_D_PK_V_c_T1[3]
    PK_V = [ int(i) for i in PID_A_D_PK_V_c_T1[3].split(',')] 
    c = int(PID_A_D_PK_V_c_T1[4])
    h_PID_T1_D_D_mult_recv = int(PID_A_D_PK_V_c_T1[5])
    T1 = PID_A_D_PK_V_c_T1[6]

    # print ("PID : ", PID, type (PID))
    # print ("A : ", A, type(A))
    # print ("D : ",D , type(D))

    # print ("PK_V : ",PK_V , type(PK_V))

    # print ("c : ",c , type(c))

    # print ("T1 : ", T1, type(T1))

    # print ("^^^^^^^ h_PID_T1_D_D_mult_recv : ", h_PID_T1_D_D_mult_recv, type(h_PID_T1_D_D_mult_recv))

    if get_timestamp () - float(T1) < 4: 
        c_P = scalar_mult (c, curve.g)
        #D_str = listToString(D)

        # print ("==========\nPID_str : ", PID, type(PID))
        # print ("T1 : ", T1, type (T1))
        # print ("D_str : ", D_str, type(D_str), "\n==========")

        h_PID_T1_D = sha256 ( PID.encode('utf-8') + str(T1).encode ('utf-8') + D_str.encode('utf-8') ).hexdigest()

        # print ("***** hash of PID_T1_D : ", h_PID_T1_D)

        h_PID_T1_D_D_mult = scalar_mult (int(sha256 ( PID.encode('utf-8') + T1.encode ('utf-8') + D_str.encode('utf-8') ).hexdigest(), 16), tuple(D))
        # print ("\n h_PID_T1_D_D_mult : ", h_PID_T1_D_D_mult, type(h_PID_T1_D_D_mult))

        c_P_temp = scalar_mult (h_PID_T1_D_D_mult_recv, curve.g ) 
        # print ("c_P_temp : ", c_P_temp)

        #h_PID_T1_D_D_P_mult = scalar_mult (c, curve.g)
        #print ("cccccc h_PID_T1_D_D_P_mult : ", h_PID_T1_D_D_P_mult )

        h_PID_PK_V_A_PK_TA_mult = scalar_mult (int(sha256 ( PID.encode('utf-8') + PK_V_str.encode ('utf-8') + A_str.encode('utf-8') ).hexdigest(), 16), PK_TA)

        # print ("\n h_PID_PK_V_A_PK_TA_mult : ", h_PID_PK_V_A_PK_TA_mult)
        add_hash = point_add (h_PID_T1_D_D_mult, h_PID_PK_V_A_PK_TA_mult)
        A_PK_V_add = point_add (A, PK_V)

        c_P_check = point_add (add_hash, A_PK_V_add)
        # print ("c_P_check is ", c_P_check)

        c_P = scalar_mult (c, curve.g)
        # print ("c_P : ", c_P)

        if c_P_temp == h_PID_T1_D_D_mult :
            print ("c_P check successful ------------")
            Res = eval_f_res_chal(chal)

            K_Rsu = xor_sha_strings (K1, sha256(str(Res).encode('utf-8')).hexdigest() )
            y_SKr = xor_sha_strings (K2, sha256(str(Res).encode('utf-8') + K1.encode ('utf-8')).hexdigest() )

            # print ("K_Rsu : ", K_Rsu)
            # print ("y_SKr : ", y_SKr)

            et, Et = make_keypair ()
            # print ("@@@@@ et : ", et)
            # print ("@@@@@ Et : ", Et)


            et_D_mult = scalar_mult (et, tuple(D))
            # print ("et_D_mult : ", et_D_mult, type(et_D_mult))

            SK_ti = sha256(convertTuple_str (et_D_mult).encode('utf-8')).hexdigest()
            # print ("SK_ti : ", SK_ti)

            T2 = get_timestamp ()
            Et_str = convertTuple_str(Et)

            # print ("^^^^^^^^^ ET_str : ", Et_str, type(Et_str))
            # print ("**** RID : ", RID, type(RID))
            # print ("**** T2 : ", str(T2), type(str(T2)))

            # print ("Hash to check : ", int (sha256 ( Et_str.encode('utf-8') + RID.encode ('utf-8') + str(T2).encode('utf-8') ).hexdigest(), 16))
            Et_RID_T2_et_mult = int (sha256 ( Et_str.encode('utf-8') + RID.encode ('utf-8') + str(T2).encode('utf-8') ).hexdigest(), 16) * et
            # print ("\n#######Et_RID_T2_et_mult : ", Et_RID_T2_et_mult)

            yt_SK_Rt_add = yt + SK_Rt
            ft = yt_SK_Rt_add + Et_RID_T2_et_mult
            # print ("\nft is ", ft)

            h_SK_ti = sha256 ( SK_ti.encode('utf-8') ).hexdigest()
            # print ("h_SK_ti : ", h_SK_ti, type (h_SK_ti))
            # print ("PID : ", PID, type (PID))
            # print ("RID : ", RID, type (RID))
            # print ("T2 : ", T2, type (T2))

            N1 = sha256 ( h_SK_ti.encode('utf-8') + PID.encode ('utf-8') + RID.encode('utf-8') + str(T2).encode('utf-8') ).hexdigest()

            # print ("N1 : ", N1)
            # print ("\n#######Et_RID_T2_et_mult : ", Et_RID_T2_et_mult)
            ft_PK_Rt_Et_Zt_N1_T2_PID_RID = convertTuple_str(PK_Rt) +"&"+ convertTuple_str(Et) +"&"+ convertTuple_str(Zt) +"&"+ N1 +"&"+ str(T2) +"&"+ PID +"&"+ RID +"&"+ str(Et_RID_T2_et_mult)
            end1_comp_time = time.time ()
            rsu_comp_time = end1_comp_time - start1_comp_time

            veh_conn.send (ft_PK_Rt_Et_Zt_N1_T2_PID_RID.encode())
            start2_comp_time = time.time ()

            jt, Jt = make_keypair ()
            T3 = get_timestamp ()
            h_SK_ti = sha256 ( SK_ti.encode('utf-8') ).hexdigest()

            # print ("\n ==================== \n N1 : ", N1, type(N1))
            # print ("h_SK_ti : ", h_SK_ti, type(h_SK_ti))
            # print ("RID : ", RID, type(RID))
            # print ("PID : ", PID, type(PID))
            # print ("Jt : ", Jt, type(Jt))
            # print ("T3 : ", T3, type(T3))

            h_N1_h_RID_PID_Jt_T3 = int(sha256 ( N1.encode('utf-8') + h_SK_ti.encode('utf-8') + RID.encode ('utf-8') + PID.encode('utf-8') + convertTuple_str(Jt).encode('utf-8') + str(T3).encode('utf-8') ).hexdigest(), 16)

            # print ("######## h_N1_h_RID_PID_Jt_T3 : ", h_N1_h_RID_PID_Jt_T3 )
            # print ("\n ==============\n######## jt : ", jt)
            h_N1_jt_mult = h_N1_h_RID_PID_Jt_T3* jt

            lt = SK_Rt + h_N1_jt_mult
            # print ("lt : ", lt, type (lt))

            K_ViRt = xor_sha_strings (h_SK_ti, sha256 (K_Rsu.encode('utf-8')).hexdigest () )
            #print ("K_ViRt : ", K_ViRt, type (K_ViRt))
            print ("Storing all data into Blockchain ==========")
            end2_comp_time = time.time ()
            # Send RID, PID, K_ViRt, N1, lt, Jt, T3 in Blockchain                           
            rsu_comp_time += end2_comp_time - start2_comp_time
            # print ("RID : ", RID, type(RID))
            # print ("PID : ", PID, type(PID))
            # print ("K_ViRt : ", K_ViRt, type(K_ViRt))
            # print ("N1 : ", N1, type(N1))
            # print ("lt : ", lt, type(lt))
            # print ("Jt : ", Jt, type(Jt))
            # print ("T3 : ", T3, type(T3))

            # import sys
            # RID_size = sys.getsizeof (RID)
            # PID_size = sys.getsizeof (PID)
            # K_ViRt_size = sys.getsizeof (K_ViRt)
            # N1_size = sys.getsizeof (N1)
            # lt_size = sys.getsizeof (lt)
            # Jt_size = sys.getsizeof (Jt)
            # T3_size = sys.getsizeof (T3)
            # h_SK_ti_size = sys.getsizeof (h_SK_ti)

            # print ("RID_size : ", RID_size)
            # print ("PID_size : ", PID_size)
            # print ("K_ViRt_size : ", K_ViRt_size)
            # print ("N1_size : ", N1_size)
            # print ("lt_size : ", lt_size)
            # print ("Jt_size : ", Jt_size)
            # print ("T3_size : ", T3_size)
            # print ("h_SK_ti_size : ", h_SK_ti_size)

            # total_size = RID_size + PID_size + K_ViRt_size + N1_size + lt_size + Jt_size + T3_size + h_SK_ti_size
            # print ("Total storage size at RSU Auth side : ", total_size)
            
            auth_sheet.row += [ RID, PID, K_ViRt, N1, str(lt), convertTuple_str(Jt), T3, h_SK_ti, rsu_comp_time]
            auth_sheet.save_as ("Provable_RSU_Auth.xlsx")

            print ("Total RSU Comp Time : ", rsu_comp_time,"\n=====================================\n")
        else :
            print ("c_P check FAILED ------------")
    else :
        print ("Timestamp Failed ...")        

        
host = "192.168.10.100" # socket.gethostname() 192.168.10.100
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
    print ("Waiting for next Veh conn ..")
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