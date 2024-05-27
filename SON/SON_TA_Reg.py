import socket
import threading
import time 
import random # import randint
import time
from hashlib import sha256  
import collections 
import pyexcel as pe 

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


def _test():
    import doctest
    doctest.testmod()

# Modular arithmetic ##########################################################

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

def handle_client(veh_socket, client_address):

    reg_sheet = pe.get_sheet (file_name = "SON_TA_Reg.xlsx")
    data = client_socket.recv(1024).decode()
    reg1_comp_start_time = time.time ()

    values = [str(i) for i in data.split(',')] # Got ID, RPW from veh
    ID = values[0]
    RPW = values[1]
    # print ("Received ID is ", ID)
    # print ("Recvd RPW is ", RPW)

    r =  random.randint(100, 100000) # 1000
    ri = str(r).zfill(64)
    print ("\n ================\nID : ", ID)
    print ("RPW : ", RPW)
    print ("ri : ", ri, "\n===================")

    RID = sha256(ID.encode('utf-8') + RPW.encode('utf-8') + ri.encode('utf-8')).hexdigest() # ID, PWD, r
    # print ("RID is ", RID)
    
    msg1 = ri+ ','+ str(l)

    # import sys
    # ri_size = sys.getsizeof (ri)
    # l_size = sys.getsizeof (l)


    # print ("ri_size : ", ri_size)
    # print ("l size : ", l_size)

    # total_size = ri_size + l_size

    # print ("^^^^^^^ Total comm cost for Reg at TA : ", total_size)


    reg1_comp_end_time = time.time ()
    reg_comp_time = reg1_comp_end_time - reg1_comp_start_time

    veh_socket.send(msg1.encode('utf')) # r, l

    reg2_comp_start_time = time.time ()

    print ("\n=================RID : ", RID, "\nk is ", k, "\n===============")
    hRIDk = sha256(str(RID).encode('utf-8') + str(k).encode('utf-8')).hexdigest()
    #reg_cont_inst = w3.eth.contract (address = reg_sc_address, abi = reg_abi)

    print ("h(RID,k) stored in BC is ", hRIDk)
    print ("Registration Successful ...")

    reg2_comp_end_time = time.time ()
    reg_comp_time += reg2_comp_end_time - reg2_comp_start_time

    print ("Total comp time at TA is ", reg_comp_time)

    reg_sheet.row += [ID, RID, ri, hRIDk, reg_comp_time ]

    reg_sheet.save_as ("SON_TA_Reg.xlsx")
    print ("Successfully wrote into excel sheet ")
    print ("======================\n \n")

k='d185b023d9e93cc9b78a4a2c97b708ccd94f70cab5031116db29b8ec946b8919'
l = 128 # fuzzy verifier

host = "localhost" # socket.gethostname()
print("Host IP is ", host)
port = 6012  # initiate port no above 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
server_socket.bind((host, port))  # bind host address and port together

server_socket.listen(40)

while True :
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread (target=handle_client, args= (client_socket, client_address, ))
    client_thread.start()

