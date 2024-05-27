import socket  
import time, datetime   
from hashlib import sha256 
import hashlib
import pyexcel as pe  
from math import floor
from typing import List, Dict  
import sys

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
    #print("Root Hash: "+ mtree.getRootHash()+"\n")
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

prime_field = 17            # w= 7 (generator), F_p field
w = 7
N = 16
ID_size = 7 

w_i = [1, 7, 15, 3, 4, 11, 9, 12, 16, 10, 2, 14, 13, 6, 8, 5]  # w^i till N = 16, D domain
w_2i = [1, 15, 4, 9, 16, 2, 13, 8]    
reg_sheet1 = pe.get_sheet (file_name= "FRI_Veh_Reg.xlsx")
auth_sheet1 = pe.get_sheet (file_name= "FRI_Veh_Auth.xlsx")

server_address = ('192.168.10.100', 6002) # 192.168.10.100
veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server's address and port

conn_flag = 0

while conn_flag == 0: 
    try :
        veh_socket.connect(server_address)
        print(f"Connected to {server_address}") 
        conn_flag = 1
    except :
        print ("Failed ... Trying to connect again")

VID =  sys.argv[1]  # sys.argv[1]
print ("VID : ", VID)

for row in reg_sheet1 : # [ fx_list, VID, VPR, RSU_comp_time, MR_fx, MR_fstar, f_w_i, f_star_w_2i ]
    if row[1] == VID :
        VPR = row[2]
        f_w_i = [int(i) for i in row[3].split(',')]
        f_star_w_2i = [int(i) for i in row[4].split(',')]
        reg_flag = 1 
        print ("  VID : ", VID, "match found ...")
        break

if reg_flag == 1 :
    
    f_w_i_root_hash, f_w_i_mtree_obj = mixmerkletree (f_w_i)
    f_star_w_2i_root_hash, f_star_w_2i_mtree_obj = mixmerkletree (f_star_w_2i)

    T1 = str(get_timestamp ())
    Auth_Req_VPR_T1 = "A1" + "&"+ VPR +"&"+ T1

    veh_socket.send (Auth_Req_VPR_T1.encode('utf')) 
    ti_R_auth_i_val_T2 = veh_socket.recv(1024).decode()  # receive (alpha) from Veh

    start1_comp_time = time.time ()
    ti_R_auth_i_val_T2 = [i for i in ti_R_auth_i_val_T2.split('&')]

    ti = ti_R_auth_i_val_T2[0]
    R_auth = ti_R_auth_i_val_T2[1]
    i_val = int(ti_R_auth_i_val_T2[2])
    T2 = float (ti_R_auth_i_val_T2[3])

    if get_timestamp () - T2 < 4 :

        print ("Received Challenge \nti = ", ti, "\ni_val = ", i_val)

        f_star_len = floor(N/2) # - 1

        get_f_w_i_val = f_w_i[i_val]
        get_f_w_N2_i = f_w_i[int(floor(N / 2)) + i_val]
        get_f_star_w_2i = f_star_w_2i[i_val]

        ABC_proof = [get_f_w_i_val, get_f_w_N2_i, get_f_star_w_2i]
        ABC_proof = listToString(ABC_proof)

        if ti == "0" :
            auth_path_for_ti = f_w_i_mtree_obj.getAuthenticationPath(Node.hash(str(f_w_i[i_val])), i_val)

        elif ti == "1" :
            auth_path_for_ti = f_star_w_2i_mtree_obj.getAuthenticationPath(Node.hash(str(f_star_w_2i[i_val])), i_val)

        auth_path_for_ti = str(auth_path_for_ti)

        T3 = get_timestamp ()

        proof_pi_R_auth_T3 = ABC_proof + "&"+ auth_path_for_ti + "&"+ R_auth + "&"+ str(T3)

        end1_comp_time = time.time ()
        comp_time = end1_comp_time - start1_comp_time

        veh_socket.send (proof_pi_R_auth_T3.encode('utf')) 
        VIDnew_Auth_status_S_auth = veh_socket.recv(1024).decode()  # Auth status from RSU1

        VIDnew_Auth_status_S_auth = [i for i in VIDnew_Auth_status_S_auth.split('&')]
        VIDnew = VIDnew_Auth_status_S_auth[0]
        S_auth = VIDnew_Auth_status_S_auth[2]

        if VIDnew_Auth_status_S_auth[1] == "S" :
            print ("Init Auth Success") 
            '''
            VIDnew_size = sys.getsizeof (VIDnew)
            S_auth_size = sys.getsizeof (S_auth)

            print ("Total storage size for Init Auth at Veh : ", VIDnew_size+ S_auth_size)
            '''
            auth_sheet1.row += [ VID, VIDnew, S_auth, comp_time ]

            print ("Veh Auth Comp Time : ", comp_time)

            auth_sheet1.save_as ("FRI_Veh_Auth.xlsx")
            print ("Saved in xlsx")
    else :
        print ("T2 Timestamp check failed")
else :
    print ("Reg details Fetch failed")
