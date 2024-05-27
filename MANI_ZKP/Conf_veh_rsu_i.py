import string
import socket
import random # import randint
import time 
import threading 
# import hashlib
import pyexcel as pe

def handle_client_veh(client_socket, rsuj_socket) : 

    n = 103
    N = 7 # size of VID
    print ("Into handle client of RSU i")
    RSU_sheet = pe.get_sheet(file_name="Conf_RSU_i.xlsx")
    TA_sheet = pe.get_sheet(file_name="Conf_ZKP_Reg_TA_details.xlsx")

    auth_req = client_socket.recv(1024).decode()  # receive  IPW, NVID, auth_r, auth_req

    auth_start_latency = time.time ()
    auth_comp1_start_time = time.time()
    print ("Auth req from veh is ", auth_req)

    values = [str(i) for i in auth_req.split('&')] 
    #print ("values are ", values)
    
    if values[3] == '02A' :
        print ("Received Authentication request ")
        row_flag = 0
        
        for row in TA_sheet :
            #print ("row is ", row)
            if row[1] == values[1] : # matching NVID       
                row_flag = 1
                break

        if row_flag == 1 :
            print ("Matched with row ", row) # Matched with row
            # if row[5] == values[2] : # compare HPW
            send1 = values[2]+ "&"+  row[2] # r and (g_s_i & g_alpha_s_i)
            alpha = int(row[3])
            auth_comp1_end_time = time.time()

            RSU_comp_time = auth_comp1_end_time - auth_comp1_start_time

            client_socket.send(send1.encode())  # sending r, and prove key

            proof = client_socket.recv(1024).decode() # recv NVID, r, proof pi 

            auth_comp2_start_time = time.time()
            #print ("Proof recvd from Veh is ", proof)

            proof_nvid_r = [str(i) for i in proof.split('&')]
            #print ("Proof NVId is ", proof_nvid_r)
            #ods_data = OrderedDict()
            
            #print ("proof recvd is ", proof_nvid_r) # (g^p, g^h, g^p')
            proof = [int(i) for i in proof_nvid_r[1].split(',')]

            if proof[2] == int(pow(proof[0], alpha, n)): # e(g^p', g) = e(g^p, g^alpha)
                print (" ----- First proof successful")
                tx_val_on_s = int(row[4])
                #print ("g_t_s_val finally is ", g_t_s_val)
                #print ("tx_val_on_s on s is ", tx_val_on_s)
                final_res = int(pow(proof[1], tx_val_on_s, n)) # (g_h * g_t_s_val) % n
                #print ("final res is ", final_res)
                #print ("--- proof[0] is ", proof[0])
                if proof[0] == final_res:
                    print ("---- Second proof successful")
                    
                    veh_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
                    auth_r = random.randint(2000, 10000)
                    session_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))
                    '''
                    print("Gen veh_id is ", veh_id)
                    print("Gen auth_r ", auth_r)
                    print("Gen session_key is ", session_key)
                    '''
                    sesn_key_vid = veh_id+ "&"+ session_key+ "&"+ str(auth_r)
                    auth_comp2_end_time = time.time()

                    RSU_comp_time += auth_comp2_end_time - auth_comp2_start_time
                    print ("Total comp time for a veh is ", RSU_comp_time, " sec")

                    client_socket.send(sesn_key_vid.encode())
                    rsuj_socket.send(sesn_key_vid.encode())
                    print ("Sending veh auth info and keys to RSU j")
                    
                    auth_end_latency = time.time ()
                    auth_latency = auth_end_latency - auth_start_latency

                    RSU_sheet.row += [veh_id, auth_r, session_key, RSU_comp_time, auth_latency]
                    print ("Saving info in xlsx ...")
                    RSU_sheet.save_as ("Conf_RSU_i.xlsx") 
                    print ("=========== RSU Init Auth SUCCESS  ===============\n\n")

                else :
                    print ("Second proof invalid")
            else :
                print ("First proof invalid")
        else :
            print ("Not matched in excel sheet")

    client_socket.close()
            
host_j = "192.168.20.200" # socket.gethostname()  192.168.20.200
port_j = 8010  # RSU_j connection & initiate port no above 1024
rsuj_socket = socket.socket()  # get instance
rsuj_socket.connect((host_j, port_j))  # connect to the RSU_j
print ("Had conn with RSU j")

host =  "192.168.10.100" # socket.gethostname() 192.168.10.100
print("RSU IP is ", host)
# print ("-------------------")
port = 6012  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together for veh comm
server_socket.listen(100) 
#print ("Had conn with Veh skt")

i = 0

print ("Going into hwile loop)")

while True :

    print ("Veh trying to connect ...")
    veh_conn, client_address = server_socket.accept()
    print ("\nRecvd conn from veh ", veh_conn, client_address) 

    client_thread2 = threading.Thread (target=handle_client_veh, args= (veh_conn, rsuj_socket)) 
    client_thread2.start()

    client_thread2.join()

    i = i + 1

