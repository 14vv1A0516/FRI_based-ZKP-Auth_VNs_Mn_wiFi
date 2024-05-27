import socket    
import string    
import random # import randint
import time, datetime
from hashlib import sha256
import hashlib
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

prime_field = 17            # w= 7 (generator), F_p field
w = 7
N = 16
ID_size = 7

w_i = [1, 7, 15, 3, 4, 11, 9, 12, 16, 10, 2, 14, 13, 6, 8, 5]  # w^i till N = 16, D domain
w_2i = [1, 15, 4, 9, 16, 2, 13, 8]   # w^2i till N = 8, D* domain

reg_sheet1 = pe.get_sheet (file_name= "FRI_Veh_Reg.xlsx")

# Create a TCP/IP socket
veh_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
server_address = ('localhost', 6002)
veh_socket.connect(server_address)
print(f"Connected to {server_address}\n****************************************") 

start1_comp_time = time.time ()

VID = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))
PIN = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(ID_size))

r = random.randint(100, 100000) 

VPR = hashlib.sha256(VID.encode('utf-8') + PIN.encode('utf-8') + str(r).encode('utf-8')).hexdigest()
# Compute the subgroup
                           
#print("Polynomial f(x)= ")
fx_list = []

f_deg = random.randint(6, 12)

for i in range(0, f_deg + 1):
    fx_list.append(random.randint(-100, 100))

#fx_list = [2, 5, 10, 6, 7, 9, 4, 14]

f_len = len(fx_list)
#print ("f list from lowest degree term  is ", f_list)  # [a_n, a_{n-1}, ..., a_1, a_0]
#printPoly(fx_list, f_len)
fx_list.reverse ()

#print ("Poly f list highest degree term is ", fx_list) # [a_0, a_1, ..., a_{n-1}, a_n]

f_w_i = []

for each in w_i :
    result = evaluate_polynomial(fx_list, each) # f_list : [a_n, a_{n-1}, ..., a_1, a_0]
    f_w_i.append(result % prime_field)  

#print(f"The result of evaluating the polynomial at x = {each} is: {result}")
#print("Subgroup D(w^i): ", w_i)

f_w_i_str = [str(num) for num in f_w_i]
MR_fx, f_w_i_mtree_obj = mixmerkletree (f_w_i_str)

#print ("f_w_i is ", f_w_i)

f_star_w_2i = []
f_star_len = floor(N/2) # - 1

fo_list = []
fe_list = []

#print ("fx_list : ", fx_list)
deg = len(fx_list)
i = 0

if deg % 2 == 0: # fx is odd degree
    while i < len(fx_list)-2:
        fo_list.append(fx_list[i])
        i = i + 1
        fe_list.append(fx_list[i])
        i = i + 1
    if i == len(fx_list)-2 :
        fo_list.append(fx_list[i])
        i = i + 1
        fe_list.append(fx_list[i])
        
elif deg % 2 != 0: # fx is even degree
    while i < len(fx_list)-2:
        fe_list.append(fx_list[i])
        i = i + 1
        if i == len(fx_list)-2 :
            fo_list.append(fx_list[i])
            i = i + 1
            fe_list.append(fx_list[i])
        else:
            fo_list.append(fx_list[i])
            i = i + 1

#print ("fe(x) : ", fe_list)
#print ("fo(x) : ", fo_list)

fe_w_2i = []
fo_w_2i = []

for each in w_2i :
    result = evaluate_polynomial(fe_list, each) # f_list : [a_n, a_{n-1}, ..., a_1, a_0]
    fe_w_2i.append(result % prime_field)  

for each in w_2i :
    result = evaluate_polynomial(fo_list, each) # f_list : [a_n, a_{n-1}, ..., a_1, a_0]
    fo_w_2i.append(result % prime_field)

#print ("fe_w_2i : ", fe_w_2i)
#print ("fo_w_2i : ", fo_w_2i)

T1 = str(get_timestamp())
VID_RPR_MRfx_T1 = VID + "&"+ VPR + "&"+ MR_fx + "&"+ T1

end1_comp_time= time.time ()

veh_comp_time = end1_comp_time - start1_comp_time

veh_socket.send (VID_RPR_MRfx_T1.encode('utf')) # send (f_w_i_root_hash) to Parent
R_reg_alpha_T2 = veh_socket.recv(1024).decode()  # receive (alpha) from Veh

R_reg_alpha_T2 = [i for i in R_reg_alpha_T2.split('&')]

alpha = int(R_reg_alpha_T2[0])
R_reg = R_reg_alpha_T2[1]
T2 = R_reg_alpha_T2[2]

#print ("R_reg : ", R_reg)
start2_comp_time = time.time ()

if get_timestamp () - float(T2) < 4 :
    for i in range(f_star_len) :
        f_star_w_2i.append( (fe_w_2i[i] + alpha * fo_w_2i[i]) % prime_field ) 
    
    #print ("f_star_w_2i : ", f_star_w_2i)

    MR_fstar, f_star_w_2i_mtree_obj = mixmerkletree (f_star_w_2i)

    T3 = get_timestamp ()

    end2_comp_time = time.time () 

    veh_comp_time += end2_comp_time - start2_comp_time

    R_reg_MR_fstar_T3 = str(R_reg) + "&"+ MR_fstar + "&"+ str(T3)
    veh_socket.send (R_reg_MR_fstar_T3.encode('utf'))
    Reg_status = veh_socket.recv(1024).decode()  # receive (alpha) from Veh
    
    if Reg_status == "S" :
        print ("Reg Done SUccess for Veh")
        '''
        import sys
        fx_list_size = sys.getsizeof (fx_list)
        VID_size = sys.getsizeof (VID)
        VPR_size = sys.getsizeof (VPR)

        total_size = VID_size + fx_list_size + VPR_size
        print ("Total storage size at Veh Reg : ", total_size)
        '''
        reg_sheet1.row += [ listToString(fx_list), VID, VPR, listToString(f_w_i), listToString(f_star_w_2i), veh_comp_time ]
        reg_sheet1.save_as ("FRI_Veh_Reg.xlsx")

        print ("Veh Comp Time for ZKP Authentication is ", veh_comp_time)
    else :
        print ("Reg failed")
else :
    print ("T2 check Failed ")



