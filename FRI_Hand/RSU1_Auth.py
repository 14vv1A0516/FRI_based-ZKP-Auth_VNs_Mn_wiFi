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

def handle_client(veh_conn, RSU2_conn) :
    reg_sheet1 = pe.get_sheet (file_name= "FRI_TA_Reg.xlsx")
    auth_sheet1 = pe.get_sheet (file_name= "FRI_RSU1_Auth.xlsx")

    fetch_reg_details = 0

    Auth_Req_VPR_T1 =  veh_conn.recv (1024).decode('utf')
    Auth_Req_VPR_T1 = [i for i in Auth_Req_VPR_T1.split('&')]

    Auth_Req = Auth_Req_VPR_T1[0]
    VPR_star = Auth_Req_VPR_T1[1]
    T1 = float(Auth_Req_VPR_T1[2])

    print ("CLient connnnected -------------")
    start_latency = time.time ()
    start1_comp_time = time.time ()

    if Auth_Req == "A1" and get_timestamp() - T1 < 4 :
        # Fetch details from TA or Neighbour RSU1 sheet

        for row in reg_sheet1 : # [ VID, VPR, alpha, R_reg, MR_fx, MR_fstar ]
            if row[1] == VPR_star :
                VPR = row[1]
                alpha = row[2]
                MR_fx = row[4]
                MR_fstar = row[5]
                fetch_reg_details = 1 
                print ("  VPR : ", VPR, "match found ...")
                break

        if fetch_reg_details == 1 :
            print ("Reg details found in Excel ...")

            i_val = random.randint(0, floor(N/2)-1)
            ti = random.randint(0, 1)
            T2 = get_timestamp ()
            R_auth = random.randint(100, 100000)
                
            ti_R_auth_i_val_T2 = str(ti)+ "&"+ str(R_auth) + "&"+ str(i_val) + "&"+ str(T2)
            end1_comp_time = time.time ()

            auth_comp_time = end1_comp_time - start1_comp_time

            veh_conn.send (ti_R_auth_i_val_T2.encode('utf')) 
            proof_pi_R_auth_T3 = veh_conn.recv (1024).decode('utf') # Recv ( ABC_proof )

            proof_pi_R_auth_T3 = [i for i in proof_pi_R_auth_T3.split('&')]
            print ("Proof Received from Vehicle \nVerifying Proof ....") #is ", ABC_authpath_rA)

            start2_comp_time = time.time ()
            ABC = proof_pi_R_auth_T3[0] # Ay, By, Cy values
            Authpath_ti = eval(proof_pi_R_auth_T3[1])
            R_auth_star = int(proof_pi_R_auth_T3[2])
            T3 = proof_pi_R_auth_T3[3]

            if get_timestamp () - float(T3) < 4 and R_auth_star == R_auth :

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
                        S_auth = random.randint(100, 10000)

                        end2_comp_time = time.time ()
                        auth_comp_time += end2_comp_time - start2_comp_time

                        VIDnew_Hand_status_S_auth = VIDnew + "&"+ "S" + "&"+ str(S_auth)

                        veh_conn.send (VIDnew_Hand_status_S_auth.encode('utf'))
                        VIDnew_VPR_Hand = VIDnew + "&"+ str(S_auth) + "&"+ MR_fx + "&"+ MR_fstar + "&"+ str(alpha)
                        RSU2_conn.send (VIDnew_VPR_Hand.encode('utf')) 

                        end_latency = time.time ()
                        total_latency = end_latency - start_latency
                        print ("******Initial Authentication SUCCESS *****")
                        '''
                        import sys
                        VIDnew_size = sys.getsizeof (VIDnew)
                        S_auth_size = sys.getsizeof (S_auth)

                        print ("Total storage size for Init Auth at Veh : ", VIDnew_size+ S_auth_size)

                        '''
                        auth_sheet1.row += [ VIDnew, S_auth, auth_comp_time, total_latency ]
                        auth_sheet1.save_as ("FRI_RSU1_Auth.xlsx")

                        print ("RSU Auth comp time is ", auth_comp_time)
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

host_j = "192.168.20.200" # 192.168.20.200
port_j = 8010  # RSU_j connection & initiate port no above 1024
rsu2_socket = socket.socket()  # get instance
rsu2_socket.connect((host_j, port_j))  # connect to the RSU_j
print ("Had conn with RSU 2")

host = "192.168.10.100" #  192.168.10.100
print("Host IP is ", host, "\nWaiting for Connection ....")
port = 6002  # initiate port no above 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
server_socket.bind((host, port))  # bind host address and port together

server_socket.listen(40)
i =0 

while True :
    print ("For loop i = ", i)

    print ("Veh trying to connect ...")
    veh_conn, client_address = server_socket.accept()
    print ("\nRecvd conn from veh ", veh_conn, client_address) 

    client_thread2 = threading.Thread (target=handle_client, args= (veh_conn, rsu2_socket)) #, rsuj_socket))
    client_thread2.start()

    i = i + 1