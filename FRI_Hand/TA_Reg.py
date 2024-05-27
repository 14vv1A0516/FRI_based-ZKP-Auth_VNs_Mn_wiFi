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

def handle_client(veh_conn) :
    reg_sheet1 = pe.get_sheet (file_name= "FRI_TA_Reg.xlsx")

    VID_RPR_MRfx_T1 = veh_conn.recv(1024).decode('utf')  # Send (Auth_Req_f_wi) from Veh

    print ("CLient connnnected -------------")
    start_latency = time.time ()

    VID_VPR_MRfx_T1 = [i for i in VID_RPR_MRfx_T1.split('&')]

    VID = VID_VPR_MRfx_T1[0]
    VPR = VID_VPR_MRfx_T1[1]
    MR_fx = VID_VPR_MRfx_T1[2]
    T1 = VID_VPR_MRfx_T1[3]
    start1_comp_time = time.time ()

    if get_timestamp() - float(T1) < 4 :
        print ("Received Authentication Request ...")
        #print ("Received f_wi hash is ", f_wi_root_hash)

        alpha = random.randint(0, 16)
        R_reg = random.randint(100, 100000)
        T2 = get_timestamp ()

        R_reg_alpha_T2 = str(alpha) +"&"+ str(R_reg) +"&"+ str(T2)

        end1_comp_time = time.time ()
        TA_comp_time = end1_comp_time - start1_comp_time 

        veh_conn.send (R_reg_alpha_T2.encode('utf')) 
        R_reg_MR_fstar_T3 = veh_conn.recv (1024).decode('utf') # Recv ( ABC_proof )

        start2_comp_time = time.time ()
        R_reg_MR_fstar_T3 = [i for i in R_reg_MR_fstar_T3.split('&')]

        R_reg_star = int(R_reg_MR_fstar_T3[0])
        MR_fstar = R_reg_MR_fstar_T3[1]
        T3 = float(R_reg_MR_fstar_T3[2])

        #print ("Reg_str : ", R_reg_star) 
        
        if get_timestamp() - T3 < 4 and R_reg == R_reg_star :
            print (" TA Reg Success ...")
            #print (VID, VPR, R_reg, MR_fx, MR_fstar)

            end2_comp_time = time.time ()

            TA_comp_time += end2_comp_time - start2_comp_time 
            Reg_status = "S"
            veh_conn.send (Reg_status.encode('utf')) 

            end_latency = time.time ()
            reg_latency = end_latency - start_latency
            '''
            import sys
            VID_size = sys.getsizeof (VID)
            VPR_size = sys.getsizeof (VPR)
            alpha_size = sys.getsizeof (alpha)
            R_reg_size = sys.getsizeof (R_reg)
            MR_fx_size = sys.getsizeof (MR_fx)
            MR_fstar_size = sys.getsizeof (MR_fstar)

            print ("VID_size : ", VID_size)
            print ("VPR_size : ", VPR_size)
            print ("alpha_size : ", alpha_size)
            print ("R_reg_size : ", R_reg_size)
            print ("MR_fx_size : ", MR_fx_size)
            print ("MR_fstar_size : ", MR_fstar_size)

            total_size = VID_size + VPR_size + alpha_size + R_reg_size + MR_fx_size + MR_fstar_size
            print ("Total size storage at TA reg : ", total_size)
            '''
            reg_sheet1.row += [ VID, VPR, alpha, R_reg, MR_fx, MR_fstar, TA_comp_time, reg_latency ]
            reg_sheet1.save_as ("FRI_TA_Reg.xlsx")

            print ("\nTA Reg comp_time : ", TA_comp_time)
            print ("Reg_latency : ", reg_latency)

            print ("Auth Done SUCCESS\n----------------------\n")
        else : 
            Reg_status = "F" 
            veh_conn.send (Reg_status.encode('utf')) 

            print ("R_reg match Failed")
    else :
        print ("T1 timestamp Failed ")
        
    veh_conn.close ()

prime_field = 17 # w= 7 (generator), F_p field
w = 7
N = 16
ID_size = 7

host = "localhost" # socket.gethostname()
print("Host IP is ", host, "\nWaiting for Connection ....")
port = 6002  # initiate port no above 1024
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
server_socket.bind((host, port))  # bind host address and port together

server_socket.listen(40)
i =0 

while True :
    client_socket, client_address = server_socket.accept()
    i = i + 1
    client_thread = threading.Thread (target=handle_client, args= (client_socket,))
    client_thread.start()

