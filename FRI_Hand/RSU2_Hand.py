import socket  
import string    
import random # import randint
import time, datetime 
from hashlib import sha256
import hashlib, threading 
import pyexcel as pe  
from math import floor
from typing import List, Dict 

class Node: 
    def __init__(self, left, right, value: str, content, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied
         
    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()
 
    def __str__(self):
        return (str(self.value))
 
    def copy(self):
        """
        class copy function
        """
        return Node(self.left, self.right, self.value, self.content, True)
       
class MerkleTree:
    def __init__(self, values: List[str]) -> None:
        self.__buildTree(values)
 
    def __buildTree(self, values: List[str]) -> None:
 
        leaves: List[Node] = [Node(None, None, Node.hash(str(e)), str(e)) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)
 
    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())  # duplicate last elem if odd number of elements
        half: int = len(nodes) // 2
 
        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)
 
        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Node(left, right, value, content)
 
    def printTree(self) -> None:
        self.__printTreeRec(self.root)
         
    def __printTreeRec(self, node: Node) -> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
                 
            if node.is_copied:
                print('(Padding)')
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)
 
    def getRootHash(self) -> str: 
        return self.root.value
    '''
    def inorderTraversal(self, node: Node) -> None:
        if node:
            self.inorderTraversal(node.left)
            print(node.value)
            self.inorderTraversal(node.right)
    '''
    def getAuthenticationPath(self, value: str, i_val) -> Dict[int, str]:
        path = {}
        
        def findNode(node: Node, depth: int, leaf_index: int) -> bool:
            nonlocal i_val
            if node is None:
                return False
            
            if node.left is None and node.right is None:
                # Check if this is the leaf node and matches the value we're looking for
                if leaf_index == i_val:
                    #print("\nFound leaf node with value:", value)
                    if i_val % 2 == 0:
                        #print("\n1 l depth : ", depth, "& Node : ", node.value)
                        path[str(depth)+"l"] = node.value
                    else:
                        #print("\n1 r depth : ", depth, "& Node : ", node.value)
                        path[str(depth)+"r"] = node.value
                    return True
                else:
                    return False
                
            else:
                if node.left and findNode(node.left, depth + 1, leaf_index * 2):
                    #print("2 r depth : ", depth, "& Node : ", node.right.value)
                    path[str(depth)+"r"] = node.right.value
                    return True
                elif node.right and findNode(node.right, depth + 1, leaf_index * 2 + 1):
                    path[str(depth)+"l"] = node.left.value
                    #print("2 l depth : ", depth, "& Node : ", node.left.value)
                    return True
                return False 

        findNode(self.root, 0, 0)
        path[str(len(path))+ "z"] = self.root.value  # Add the root hash at the end of the path with the maximum depth
        #print("\n3 depth : ", len(path), "& Node : ", self.root.value,"\n")

        return path
    
    def getAncestorslist(self, value: str) -> List[str]:
        path = []
        def findNode(node: Node, value: str) -> bool:
            if node is None:
                return False
            elif node.value == value:
                # path.append(node.value)
                return True
            else:
                if node.left and findNode(node.left, value):
                    path.append(node.left.value)
                    return True
                elif node.right and findNode(node.right, value):
                    path.append(node.right.value)
                    return True
                return False
        findNode(self.root, value)
        path.append(self.root.value)
        return path
    
def mixmerkletree(f_w_i) -> None:
    #print("Inputs: ")
    #print(*f_w_i, sep=" | ")
    #print("")
    mtree = MerkleTree(f_w_i)
    print("Root Hash: "+ mtree.getRootHash()+"\n")
    #mtree.printTree()
    #print("\nInorder Traversal:\n")
    #mtree.inorderTraversal(mtree.root)
    return mtree.getRootHash(), mtree

def Ver_merkle_path(auth_path, root_hash):
    skip_count = 0

    for key, value in auth_path.items():
        #print(f"Key: {key}, Value: {value}")

        if skip_count >= 3:
            #print ("Into If part ****")
            
            if key[1] == "l" :
                prev_hash = sha256(auth_path[key].encode('utf-8') + prev_hash.encode('utf-8')).hexdigest()
                #print ("11 Prev hash is ", prev_hash)

            elif key[1] == "r" :
                prev_hash = sha256(prev_hash.encode('utf-8') + auth_path[key].encode('utf-8')).hexdigest()
                #print ("22 Prev hash is ", prev_hash)

        else:
            #print ("Into else ---")
            if key[1] == "l" :
                value1 = auth_path[key]
            elif key[1] == "r" :
                value2 = auth_path[key]

            skip_count += 1

            if skip_count == 2 :
                prev_hash = sha256(value1.encode('utf-8') + value2.encode('utf-8')).hexdigest()
                #print ("33 Prev hash is ", prev_hash)
                skip_count += 1

    if prev_hash == root_hash :
        return 1
    else :
        return 0

def printPoly(poly, n):
    # Initialize an empty string to store the polynomial
    polynomial_str = ""

    for i in range(n):
        # Append the coefficient and x term to the string
        if poly[i] != 0:
            polynomial_str += str(poly[i]) + "x^" + str(i) + " + "

    # Remove the trailing " + " from the end of the string
    polynomial_str = polynomial_str[:-3]

    # Print the entire polynomial in a single line
    print(polynomial_str)

def evaluate_polynomial(coefficients, x):
    result = 0
    for i, coef in enumerate(coefficients):
        result += coef * (x ** (len(coefficients) - 1 - i))
    return result

def listToString(s): 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        str1 += str(ele)
        str1 += ","
    str1 = str1[:len(str1)-1]
    return str1

def get_timestamp() :
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    return ts

def handle_RSU2(rsu1_conn) :
    while(1) :
        print ("Waiting to recv data ...")
        veh_Auth_details = rsu1_conn.recv(1024).decode() # recv auth session key, r , VID from RSU_i
        print ("Recd veh keys from RSU_i is ", veh_Auth_details)
        print ("\n=====================\n")

        sheet = pe.get_sheet(file_name="RSU2_store_Veh.xlsx")
        sheet.row += [str(i) for i in veh_Auth_details.split('&')]
        sheet.save_as ("RSU2_store_Veh.xlsx")

def handle_client(veh_conn) :

    #reg_sheet1 = pe.get_sheet (file_name= "FRI_TA_Reg.xlsx")
    auth_sheet1 = pe.get_sheet (file_name= "FRI_RSU1_Auth.xlsx")
    store_init_auth_sheet1 = pe.get_sheet (file_name= "RSU2_store_Veh.xlsx")
    hand_sheet1 = pe.get_sheet (file_name= "FRI_RSU2_Hand.xlsx")

    fetch_init_auth_details = 0

    VIDnew_Hand_req_S_auth_T1 =  veh_conn.recv (1024).decode('utf')  #VIDnew + "&"+ "H1"+ "&"+ S_auth+ "&"+ str(T1)
    VIDnew_Hand_req_S_auth_T1 = [i for i in VIDnew_Hand_req_S_auth_T1.split('&')]

    VIDnew = VIDnew_Hand_req_S_auth_T1[0]
    #S_auth = VIDnew_Hand_req_S_auth_T1[2]
    T1 = float(VIDnew_Hand_req_S_auth_T1[3])

    print ("CLient connnnected -------------")
    start_latency = time.time ()
    start1_comp_time = time.time ()

    if VIDnew_Hand_req_S_auth_T1[1] == "H1" and get_timestamp() - T1 < 4 :
        # Fetch details from TA or Neighbour RSU1 sheet

        for row in store_init_auth_sheet1 : # [ VID, VPR, alpha, R_reg, MR_fx, MR_fstar ]
            if row[0] == VIDnew :
                MR_fx = row[2]
                MR_fstar = row[3]
                alpha = int(row[4])
                fetch_init_auth_details = 1 
                print ("  VIDnew : ", VIDnew, " found in Store init sheet...")
                break

        if fetch_init_auth_details == 1 :

            i_val = random.randint(0, floor(N/2)-1)
            ti = random.randint(0, 1)
            T2 = get_timestamp ()
            R_hand = random.randint(100, 100000)
                
            ti_R_auth_i_val_T2 = str(ti)+ "&"+ str(R_hand) + "&"+ str(i_val) + "&"+ str(T2)
            end1_comp_time = time.time ()

            hand_comp_time = end1_comp_time - start1_comp_time

            veh_conn.send (ti_R_auth_i_val_T2.encode('utf')) 
            proof_pi_R_hand_T3 = veh_conn.recv (1024).decode('utf') # Recv ( ABC_proof )

            proof_pi_R_hand_T3 = [i for i in proof_pi_R_hand_T3.split('&')]
            print ("Proof Received from Vehicle \nVerifying Proof ....") #is ", ABC_authpath_rA)

            start2_comp_time = time.time ()
            ABC = proof_pi_R_hand_T3[0] # Ay, By, Cy values
            Authpath_ti = eval(proof_pi_R_hand_T3[1])
            R_hand_star = proof_pi_R_hand_T3[2]
            T3 = proof_pi_R_hand_T3[3]

            if get_timestamp () - float(T3) < 4 and R_hand_star == str(R_hand) :

                if ti == 0 :
                    #print ("\nVer merkle path for f(w^i) ")
                    merkle_ver_status = Ver_merkle_path (Authpath_ti, MR_fx )
                elif ti == 1 :
                    #print ("\nVer merkle path for fstar(w^2i) ")
                    merkle_ver_status = Ver_merkle_path (Authpath_ti, MR_fstar )

                if merkle_ver_status == 1 :
                    print ("---------Merkle  path Verified SUCCESSFUL ---------")

                    ABC_proof_list = [int(i) for i in ABC.split(',')]

                    x_values = [ (w**i_val) % prime_field, (w**(floor(N/2)+ i_val)) % prime_field] #, alpha 
                    y_values = [ ABC_proof_list[0] , ABC_proof_list[1] ] # , ABC_proof_list[2]

                    # print ("A : (", x_values[0], ",", y_values[0], ")")
                    # print ("B : (", x_values[1], ",", y_values[1], ")")

                    w_minus_i_mod_p = pow(w, -i_val, prime_field)
                    inv_2_mod_p = pow(2, -1, prime_field)

                    term1 = 1 + alpha * w_minus_i_mod_p 
                    term2 = 1 - alpha * w_minus_i_mod_p

                    y3_for_alpha = ((term1 *  y_values[0] + term2 * y_values[1] ) * inv_2_mod_p) % prime_field
                    # print ("\nComputed C : (", alpha, ",", y3_for_alpha, ")")

                    if y3_for_alpha == ABC_proof_list[2]:
                        print ("---- Lagrange interpolation Ver SUCCESSFUL-----------")

                        VIDnew  = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))

                        S_hand= random.randint(100, 10000)
                        VIDnew_Hand_status_S_hand = VIDnew + "&"+ "S" + "&"+ str(S_hand)

                        veh_conn.send (VIDnew_Hand_status_S_hand.encode('utf')) 
                        #VIDnew_VPR_Hand = VIDnew + "&"+ VPR + "&"+ MR_fx + "&"+ MR_fstar + "&"+ str(S_auth)
                        #RSU2_conn.send (VIDnew_VPR_Hand.encode('utf')) 

                        print ("******Authentication SUCCESS *****")

                        end2_comp_time = time.time ()
                        hand_comp_time += end2_comp_time - start2_comp_time

                        end_latency = time.time ()
                        total_latency = end_latency - start_latency
                            
                        hand_sheet1.row += [ VIDnew, hand_comp_time, total_latency ]
                        hand_sheet1.save_as ("FRI_RSU2_Hand.xlsx")

                        print ("RSU Hand comp time is ", hand_comp_time)
                        print ("Total latency is ", total_latency,"\n\n*******************************")
                                
                    else :
                        Auth_status = "F"
                        veh_conn.send (Auth_status.encode('utf')) 
                        print ("Lagrange interpolation Failed")
                else :
                    print ("Merkle Auth failed ")
            else :
                print ("T3 timestamp check failed")
        else :
            print ("Unable to fetch Reg details ")
    else :
        print ("T1 timestamp check failed")

    veh_conn.close ()

prime_field = 17            # w= 7 (generator), F_p field
w = 7
N = 16
ID_size = 7

i = 0
rsu_j = 0

host = "192.168.20.200" # socket.gethostname()  192.168.20.200

print("RSU j IP is ", host)
port_i = 8010  # RSU_i connection & initiate port no above 1024
rsu1_socket = socket.socket()  # get instance
rsu1_socket.bind((host, port_i))  # bind host address and port together
rsu1_socket.listen(4) 
rsu1_conn, rsui_address = rsu1_socket.accept() # comment for handover auth

print ("-----RSU1 connected--------------")
port = 6003  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together
server_socket.listen(40) 

i = 0
rsu_j = 0 # For comment hand auth keep 1 else 0

while True :
    print ("For loop i = ", i)

    if rsu_j == 0:
        print ("Thread for RSU 1 started ...")
        client_thread1 = threading.Thread (target=handle_RSU2, args= (rsu1_conn,)) # rsui_conn, rsuk_conn))
        client_thread1.start()
        rsu_j = 1

    print ("Trying to connect with veh ...")
    
    veh_conn, veh_address = server_socket.accept()  
    print ("\nRecvd conn from veh ", veh_conn, veh_address)  
    
    client_thread3 = threading.Thread (target=handle_client, args= (veh_conn,)) # , rsui_conn, rsuk_conn)) 
    client_thread3.start()

    i = i + 1
