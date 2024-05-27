import socket
import random # import randint  
import time 
from hashlib import sha256 
import datetime  
import pyexcel as pe 
import collections, ast 
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


reg_sheet1 = pe.get_sheet (file_name= "Provable_Reg_Veh_details.xlsx")
auth_sheet1 = pe.get_sheet (file_name= "Provable_Auth_Veh_details.xlsx")

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

VID_inp = sys.argv[1] # ZGYUCBJ VNDHTNX ABPPG67
print ("Given inp VID : ", VID_inp)

reg_flag =0
for row in reg_sheet1 : # Get ( VID, V, S1, S2, S3, A_str, PK_Vi_str, PK_TA_str, PID_str, VaI, Tou, Sigma, SK_V, Veh_Reg_comp_time )
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
        print ("  VID : ", VID_inp, "match found ...")
        break

# print ("V : ", V, type(V))
# print ("S1 : ", S1, type(S1))
# print ("S2 : ", S2, type(S2))
# print ("S3 : ", S3, type(S3))
# print ("A : ", A, type(A))
# print ("PK_Vi : ", PK_Vi, type (PK_Vi))
# print ("PK_TA : ", PK_TA, type(PK_TA))
# print ("PID_str : ", PID_str, type(PID_str))
# print ("VaI : ", VaI, type(VaI))
# print ("Tou : ", Tou, type(Tou))
# print ("Sigma : ", sigma, type(sigma))
# print ("SK_V : ", SK_V, type(SK_V))

start_latency = time.time ()

start1_comp_time = time.time ()

if reg_flag == 1 :
    if V == sha256 ( sigma.encode('utf-8') + VaI.encode ('utf-8') ).hexdigest() :
        print ("V also matched ....")

        b = xor_sha_strings (S1, sha256 ( sigma.encode('utf-8') + V.encode ('utf-8') ).hexdigest()  )
        SK_v = xor_sha_strings (S2, sha256 ( V.encode('utf-8') + sigma.encode ('utf-8') ).hexdigest()  )   
        
        # print ("b : ", b)
        # print ("SK_v : ", SK_v)

        T1 = get_timestamp ()
        d, D = make_keypair ()

        # print ("d : ", d)
        # print ("D : ", D)

        D_str = ','.join(str(num) for num in D)

        # print ("===========\n")
        # print ("PID_str : ", PID_str, type(PID_str))
        # print ("T1 : ", str(T1), type (str(T1)))
        # print ("D_str : ", D_str, type(D_str))
        # print ("\n===========")
        #T1 = str(T1)
        T1 = str(format(T1, '.2f'))
        h_PID_T1_D = sha256 ( PID_str.encode('utf-8') + T1.encode ('utf-8') + D_str.encode('utf-8') ).hexdigest()
        # print ("***** hash of PID_T1_D : ", h_PID_T1_D)

        h_PID_T1_D_d_mult = int (sha256 ( PID_str.encode('utf-8') + str(T1).encode ('utf-8') + D_str.encode('utf-8') ).hexdigest(), 16) *d
        # print ("^^^^^^^^ h_PID_T1_D_d_mult : ", h_PID_T1_D_d_mult, "\n")

        b_SKV_add = int(b) + int(SK_v)
        c = b_SKV_add + h_PID_T1_D_d_mult

        # print ("c is ", c)
        PID_A_D_PK_V_c_T1 = PID_str +"&"+ A +"&"+ D_str +"&"+ PK_Vi +"&"+ str(c) +"&"+  str(h_PID_T1_D_d_mult) +"&"+ str(T1)
        # print ("PID_A_D_PK_V_c_T1 is ", PID_A_D_PK_V_c_T1)

        end1_comp_time = time.time ()
        veh_comp_time = end1_comp_time - start1_comp_time

        veh_socket.send(PID_A_D_PK_V_c_T1.encode('utf-8'))

        ft_PK_Rt_Et_Zt_N1_T2_PID_RID = veh_socket.recv(1024).decode()  

        start2_comp_time = time.time ()

        ft_PK_Rt_Et_Zt_N1_T2_PID_RID = [ i for i in ft_PK_Rt_Et_Zt_N1_T2_PID_RID.split('&')]


        PK_Rt = [ int(i) for i in ft_PK_Rt_Et_Zt_N1_T2_PID_RID[0].split(',')]

        PK_Rt_str = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[0]
        Et_str = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[1]

        Et = [ int(i) for i in ft_PK_Rt_Et_Zt_N1_T2_PID_RID[1].split(',')]
        Zt_str = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[2]
        Zt = [ int(i) for i in ft_PK_Rt_Et_Zt_N1_T2_PID_RID[2].split(',')]
        N1 = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[3]
        T2 = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[4]
        PID = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[5]
        RID = ft_PK_Rt_Et_Zt_N1_T2_PID_RID[6]
        Et_RID_T2_et_mult = int(ft_PK_Rt_Et_Zt_N1_T2_PID_RID[7])


        # print ("\nft_PK_Rt_Et_Zt_N1_T2_PID_RID : ", ft_PK_Rt_Et_Zt_N1_T2_PID_RID, "\n")
        # print ("PK_Rt : ", PK_Rt, type(PK_Rt))
        # print ("^^^^^^ Et : ", Et , type(Et))
        # print ("Zt : ", Zt , type(Zt))
        # print ("N1 : ", N1 , type(N1))
        # print ("T2 : ", T2 , type(T2))
        # print ("PID : ", PID , type(PID))
        # print ("RID : ", RID, type(RID))
        # print ("\n#######Et_RID_T2_et_mult : ", Et_RID_T2_et_mult, type(Et_RID_T2_et_mult))

        if get_timestamp () - float(T2) < 4: 
            # print ("\nPK_TA : ", PK_TA, type(PK_TA))
            PK_TA = ast.literal_eval(PK_TA)
            # print ("PK_TA : ", PK_TA, type(PK_TA[1]))

            RID_PK_Rt_Zt_PK_TA_mult = scalar_mult (int( sha256 ( RID.encode('utf-8') + PK_Rt_str.encode ('utf-8') + Zt_str.encode('utf-8') ).hexdigest(), 16), PK_TA )
            # print ("\nRID_PK_Rt_Zt_PK_TA_mult : ", RID_PK_Rt_Zt_PK_TA_mult)

            # print ("**** ET_str : ", Et_str, type(Et_str))
            # print ("**** RID : ", RID, type(RID))
            # print ("**** T2 : ", T2, type(T2))

            # print ("hash to check : ", int(sha256 ( Et_str.encode('utf-8') + RID.encode ('utf-8') + T2.encode('utf-8') ).hexdigest(), 16))
            Et_RID_T2_Et_mult = scalar_mult (int(sha256 ( Et_str.encode('utf-8') + RID.encode ('utf-8') + T2.encode('utf-8') ).hexdigest(), 16), Et )

            # print ("Et_RID_T2_Et_mult : ", Et_RID_T2_Et_mult)

            h1 = point_add (RID_PK_Rt_Zt_PK_TA_mult, Zt)
            h2 = point_add (Et_RID_T2_Et_mult, PK_Rt)
            ft_P_check = point_add (h1, h2)

            # print ("ft_P_check : ", ft_P_check, type(ft_P_check))
            # print ("Et_RID_T2_et_mult : ", int(Et_RID_T2_et_mult), type(Et_RID_T2_et_mult))

            ft_P = scalar_mult (int(Et_RID_T2_et_mult), curve.g)
            # print ("ft_P : ", ft_P)

            if ft_P == Et_RID_T2_Et_mult :
                print ("ft_p check Success: ")
                d_Et_mult = scalar_mult (d, Et)
                SK_it = sha256 ( convertTuple_str(d_Et_mult).encode('utf-8') ).hexdigest()
                # print ("SK_it : ", SK_it)

                h_SK_ti = sha256 ( SK_it.encode('utf-8') ).hexdigest()

                # print ("h_SK_ti : ", h_SK_ti, type (h_SK_ti))
                
                N_star = sha256 ( h_SK_ti.encode('utf-8') + PID.encode ('utf-8') + RID.encode('utf-8') + T2.encode('utf-8') ).hexdigest()
                # print ("N_star : ", N_star)

                if N1 == N_star :
                    print ("Auth Success ")

                    end2_comp_time = time.time ()

                    veh_comp_time += end2_comp_time - start2_comp_time
                    print ("Total Comp Time : ", veh_comp_time)

                    end_latency = time.time ()
                    auth_latency = end_latency - start_latency
                    '''
                    import sys
                    vid_size = sys.getsizeof (VID_inp)
                    v_size = sys.getsizeof (V)
                    s1_size = sys.getsizeof (S1)
                    s2_size = sys.getsizeof (S2)
                    s3_size = sys.getsizeof (S3)
                    astar_size = sys.getsizeof (A)
                    PK_Vi_str_size = sys.getsizeof (PK_Vi)
                    PK_TA_str_size = sys.getsizeof (PK_TA)
                    PID_str_size = sys.getsizeof (PID_str)
                    VaI_size = sys.getsizeof (VaI)
                    Tou_size = sys.getsizeof (Tou)
                    sigma_size = sys.getsizeof (sigma)
                    SK_Vi_size = sys.getsizeof (SK_it)

                    print ("vid_size : ", vid_size)
                    print ("v_size : ", v_size)
                    print ("s1_size : ", s1_size)
                    print ("s2_size : ", s2_size)
                    print ("s3_size : ", s3_size)
                    print ("astar_size : ", astar_size)
                    print ("PK_Vi_str_size : ", PK_Vi_str_size)
                    print ("PK_TA_str_size : ", PK_TA_str_size)
                    print ("PID_str_size : ", PID_str_size)
                    print ("VaI_size : ", VaI_size)
                    print ("Tou_size : ", Tou_size)
                    print ("sigma_size : ", sigma_size)
                    print ("SK_Vi_size : ", SK_Vi_size)

                    total_size = SK_Vi_size + sigma_size + Tou_size + VaI_size + vid_size + v_size + s1_size + s2_size + s3_size + astar_size + PK_Vi_str_size + PK_TA_str_size + PID_str_size 
                    print ("Total storage size for veh AUth : ", total_size)
                    '''
                    auth_sheet1.row += [VID_inp, V, S1, S2, S3, A, PK_Vi, convertTuple_str(PK_TA), PID_str, VaI, Tou, sigma, str(SK_it), veh_comp_time, auth_latency]
                    auth_sheet1.save_as ("Provable_Auth_Veh_details.xlsx")

                    print ("Total Latency ::: ",auth_latency, " sec")

                else :
                    print ("Auth Failed ")
            else :
                print ("ft_p check Failed")
        else :
            print ("Time stamp T2 Failed ...")
    else :
        print ("V Not matched ....")
else :
    print ("Unfound in Excel sheet")



# print ("V : ", V, type(V))
# print ("S1 : ", S1, type(S1))
# print ("S2 : ", S2, type(S2))
# print ("S3 : ", S3, type(S3))
# print ("A : ", A, type(A))
# print ("PK_Vi : ", PK_Vi, type(PK_Vi))
# print ("PK_TA : ", PK_TA, type(PK_TA))
# print ("PID_str : ", PID_str, type(PID_str))
# print ("VaI : ", VaI, type(VaI))
# print ("Tou : ", Tou, type(Tou))
# print ("sigma : ", sigma, type(sigma))
# print ("str(SK_it) : ", str(SK_it), type(str(SK_it)))





