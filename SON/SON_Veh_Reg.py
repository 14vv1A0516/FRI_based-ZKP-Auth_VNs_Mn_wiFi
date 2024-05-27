import socket
import time
import random # import ra ndint
import time 
from hashlib import sha256 
import string
import pyexcel as pe

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

host = "localhost" # socket.gethostname()
port = 6012  # socket server port number
veh_socket = socket.socket()  # instantiate
veh_socket.connect((host, port))  # connect to the server
N = 7

reg_sheet = pe.get_sheet (file_name = "SON_Reg_Veh.xlsx")

reg_start_latency = time.time ()

reg1_comp_start_time = time.time ()
ID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N)) # 'VID'
PWD = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N)) # 'PWD'

print ("ID is ", ID)
print ("PWD is ", PWD) 

HPW = sha256(ID.encode('utf-8') + PWD.encode('utf-8')).hexdigest() # ID and PWD

xi = random.randint(100, 100000) # 1000
xi = str(xi).zfill(64)
hxi = sha256(str(xi).encode('utf-8')).hexdigest()

RPW = xor_sha_strings(HPW, hxi)

print ("RPW is ", RPW)
msg1 = ID + "," + RPW
print ("Sending ID and RPW : ", msg1)

# import sys
# ID_size = sys.getsizeof (ID)
# RPW_size = sys.getsizeof (RPW)

# print ("ID size : ", ID_size)
# print ("RPW size : ", RPW_size)

# total_size = ID_size + RPW_size

# print ("^^^^^^^ Total comm cost for Reg at Veh : ", total_size)

reg1_comp_end_time = time.time ()
reg_comp_time = reg1_comp_end_time - reg1_comp_start_time

veh_socket.send(msg1.encode('utf'))  # send ID + RPW to TA
data = veh_socket.recv(1024).decode()  # receive r, l

reg2_comp_start_time = time.time ()
values = [str(i) for i in data.split(',')]
ri = values[0]
l = values[1]

# print ("Recvd r, l are ", ri, l)
# print ("HPw is ", HPW)

RID = sha256(ID.encode('utf-8') +  RPW.encode('utf-8') + ri.encode('utf-8')).hexdigest()
# print ("RID is ", RID)
ri = ri.zfill(64)
hr = sha256(ri.encode('utf-8')).hexdigest() # h(ri)
# print ("hri is ", hr) 

A =  xor_sha_strings (ri, HPW) 

# print("xi is ", xi)
B =  xor_sha_strings (xi, hr)
temp = sha256(RID.encode('utf-8') + str(xi).encode('utf-8')).hexdigest()
C = sha256(temp.encode('utf-8')).hexdigest()
# print ("A, B, C is ", A, B, C)

reg2_comp_end_time = time.time () 

reg_comp_time += reg2_comp_end_time - reg2_comp_start_time
reg_end_latency = time.time ()

reg_latency = reg_end_latency - reg_start_latency

reg_sheet.row += [ID, PWD, A, B, C, reg_comp_time, reg_latency]
reg_sheet.save_as ("SON_Reg_Veh.xlsx")

print ("\nVeh Reg time is ", reg_comp_time, "sec")
print ("Total Reg Latency is ", reg_latency, "sec")

print ("Registration Successful ...\n") 
