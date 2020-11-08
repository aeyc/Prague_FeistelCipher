#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 04:23:08 2020
@author: Ayca & Emanuele
"""

#%%
#readFile_Binary Func takes filename, returns list with pairs in given filename
#CALL: 
#    readFile_Binary('KPApairsPrague_linear')
#    readFile_Binary('KPApairsPrague_nearly_linear')
#    readFile_Binary('KPApairsPrague_non_linear')
#returns 2 dimensional list - list of pairs
#USAGE:
#   lst = readFile_Binary('KPApairsPrague_non_linear')
#   lst[0] = first pair, 
#   lst[0][0] = first u in first pair
#   lst[0][1] = first x in first pair
def readFile_Binary(filename):
    with open(filename,'r') as f:
        data = f.read()
        
    data = data.split()
    l = []
    pairs = []
    for i in range(0,len(data)):
        hexadecimal = data[i]
        end_length = len(hexadecimal) * 4
        hex_as_int = int(hexadecimal, 16)
        hex_as_binary = bin(hex_as_int)
        padded_binary = hex_as_binary[2:].zfill(end_length)
        padded_binary = list(padded_binary)
        padded_binary = [int(i) for i in padded_binary]
        if (len(pairs)==0):
            pairs.append(padded_binary)
        elif len(pairs) == 1:
            pairs.append(padded_binary)
            l.append(pairs)
            pairs = []
    return l

def hexToBinary(h):
    return "{0:b}".format(int(h))

#outputing the hex version of cipher text
def binaryToHex(x):
    x_str = ""
    for i in range(0,len(x)):
        x_str += str(x[i])
    x_hex = hex(int(x_str, 2))
    return x_hex

#printEnc function to format output of Encryption
def printEnc(x):
    print("\nEncryption:")
    print("x:", x)
    print(binaryToHex(x))
    
#printDec function to format output of Decryption
def printDec(u)  :
    print("\nDecryption:")
    print("u:", u)
    print(binaryToHex(u))
    
    
##Feistel cipher with linear f - Task 1
def linear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ k[int(4*j-3)-1]
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ k[int(4*j-2*l)-1]
        w.append(tmp)
    return w


##Feistel cipher with nearly-linear f - Task 5
def nearlyLinear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ (k[int(4*j-3)-1] & 
                            (y[(2*j -1) -1] #y[2j-1]
                            | k[(2*j -1) -1] #k[2j-1]
                            | k[(2*j)-1] #k[2j]
                            | k[(4*j -2) -1]))
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ (k[int(4*j-2*l) -1] and 
                            (k[(4*j-2*l-1) -1]
                             or k[(2*j-1) -1]
                             or k[(2*j) -1]
                             or y[(2*j-l)-1]))        
        w.append(tmp)
    return w


##Feistel cipher with non-linear f - Task 7
def nonLinear_f(y,k):
    l=len(y)
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = ((y[j-1] & k[(2*j-1) -1]) | 
                   (y[(2*j-1) -1] & k[(2*j) -1]) | 
                   k[(4*j) -1])
        elif j>l/2 and j <=l: #15
            tmp = ((y[j-1] & k[(2*j-1) -1]) | 
                   (k[(4*j-2*l-1) -1] & k[(2*j) -1]) | 
                   y[(2*j-l) -1])
        w.append(tmp)
    return w

##bitwise addition function
def addition(z,w):
    v=[]
    for i in range(0,len(w)):
        v.append((w[i]^z[i])) #(w[i]+z[i])%2
    return v

##key generation function - depends only on k0 and roundNumber
def keyGeneration(k,i):
    tmp = []
    for j in range(1,len(k)+1): # 1 to 32
        tmp.append(k[((5*(i+1)+j-1)%len(k))])
    return tmp

#%% Encryption
def Encryption(u,k0,n,taskNumber):
    #print("\n\nEncryption:\n")
    y = u[:int(len(u)/2)] #initialize y
    z = u[int(len(u)/2):] #initialize z
    k = []

    for i in range(0,n): # i represents the roundnumber here
        
        new_key = keyGeneration(k0,i) #generate key for i-th round
        k.append(new_key) ##attach it to list of key
        
        #Calculate round functions base on task number
        if taskNumber == 1:
            w = linear_f(y,k[i]) #compute w
        elif taskNumber == 5:
            w = nearlyLinear_f(y,k[i])
        elif taskNumber ==7:
            w = nonLinear_f(y,k[i])
            
        v = addition(z,w) #compute v and attach to its list
        
        if (i<n-1): # we are ignoring the last transposition
            new_z,new_y = y,v #transposition
            y = new_y #y for the next round
            z = new_z #z for the next round
        
        x =  y + v
    return x,k
#calling encryption:
# x = Encryption(null_vector,matrixI[i],17,1)[0]
# k = Encryption(null_vector,matrixI[i],17,1)[1]
# x,k = Encryption(null_vector,matrixI[i],17,1)
#%% Task 2 - Decryption 
def Decryption(x,k,n,taskNumber): # k = is list of generated keys
    #print("\n\nDecryption:\n")

    y = x[:int(len(x)/2)] #initialize y
    v = x[int(len(x)/2):] #initialize v
    k.reverse()
    u_l = []
    for i in range(0,n):
        if taskNumber == 1:
            w = linear_f(y,k[i]) #compute w
        elif taskNumber == 5:
            w = nearlyLinear_f(y,k[i]) #compute w
        elif taskNumber == 7:
            w = nonLinear_f(y,k[i]) #compute w
        z = addition(v,w) #compute v and attach to its list
        
        if (i<n-1):
            new_v,new_y = y,z #transposition
            y = new_y #y for the next round
            v = new_v #z for the next round
        
        u =  y +z
        u_l.append(u)
    return u
#%% Task 3-4
import numpy as np
from numpy.linalg import inv,det

#find matrix A
def find_A(lu,lk):
    matrixI = np.identity(lk).astype(int)
    a=[]
    null_vector = np.zeros(lu,dtype=int) 
    for i in range (0, lu):
        a.append(Encryption(matrixI[i],null_vector,17,1)[0])
    a = np.transpose(a)
    return a

def find_B(lu,lk):
    matrixI = np.identity(lk).astype(int)
    b=[]
    null_vector = np.zeros(lu, dtype=int)
    for i in range (0, lu):
        b.append(Encryption(null_vector,matrixI[i],17,1)[0])
    b = np.transpose(b)
    return b

def binaryInv(a):
    a_invb = (inv(a)*det(a)).astype(int)
    a_mod = np.remainder(a_invb, 2)
    return a_mod
#a = np.array([[0,0,0,1,1],[1,0,1,0,1],[1,1,1,1,0],[1,1,0,0,1],[0,0,1,0,1]])
#binaryInv(a)

#linear cryptoanalysis KPA
def linear_cryptoanalysis_KPA(u,x):
    a=find_A(len(u),len(u))
    a_inv = binaryInv(a)
    b= find_B(len(u),len(u)) 
    tmp = np.dot(b,u)
    tmp = tmp+x
    tmp = np.remainder(tmp,2)
    k = np.dot(a_inv,tmp)
    k = np.remainder(k,2)
    return k

#nearly-linear cryptoanalysis KPA
def nearly_linear_cryptoanalysis_KPA(u,x):
    a=find_A(len(u),len(u))
    a_inv = binaryInv(a)
    b= find_B(len(u),len(u)) 
    c = np.identity(len(u)).astype(int)
    tmp = np.dot(b,u)
    tmp = tmp+np.dot(c,x)
    tmp = np.remainder(tmp,2)
    k = np.dot(a_inv,tmp)
    k = np.remainder(k,2)
    return k
#%%Task1 - Test
print("Task 1")
lu = 32
lx = 32
l = 16
lk = 32
n = 17

k0 = 0x80000000
k0 = list(hexToBinary(k0))
k0 = [int(i) for i in k0] 


u = 0x80000000
u = list(hexToBinary(u))
u = [int(i) for i in u] 
x1,k = Encryption(u,k0,n,1)
printEnc(x1)

print("\n\nTask 2")
u_res1 = Decryption(x1,k,n,1)
printDec(u_res1)

#%%Task 3
print("\n\nTask 3")
#trying to find k with linear cipher
u = 0x80000000
u = list(hexToBinary(u))
u = [int(i) for i in u] 

a = find_A(lu,lk)
b = find_B(lu,lk)
x3 = np.remainder(np.dot(a,k0) + np.dot(b,u),2)
result = np.array_equal(x3, x1)
if result == True:
    print("x from Encryption function:", binaryToHex(x1))
    print("x from the equation Ak+Bu:", binaryToHex(x3))
    print("Linearity of the system is proven")
    
import matplotlib.pyplot as plt

plt.matshow(a);
plt.colorbar()
plt.title("Matrix A")
plt.show()

plt.matshow(b);
plt.colorbar()
plt.title("Matrix B")
plt.show()
#%%Task 4
print("\n\nTask 4")
filename = "KPApairsPrague_linear.hex"
data = readFile_Binary(filename)

lu = len(data[0][0])
lx = len(data[0][1])
lk = lu
kg_l = [] #list of key guesses
x_g =[] #list of x guesses
for i in data:
    k_guess = linear_cryptoanalysis_KPA(i[0],i[1])
    kg_l.append(k_guess)
    a = find_A(lu,lk)
    b = find_B(lu,lk)
    x3 = np.remainder(np.dot(a,k_guess) + np.dot(b,i[0]),2)
    x_g.append(Encryption(i[0],k_guess,17,1)[0])
    print("A(k_guess = {}) + Bu = x ->{}".format( binaryToHex(k_guess),np.array_equal(x3, i[1])))

appr = np.array(kg_l)
appr = appr.sum(axis = 0)
for j in range(0,len(appr)):
    if appr[j] > 2.5:
        appr[j] = 1
    else:
        appr[j] = 0
x_guess_l = []

for j in data:
    x_guess = Encryption(j[0],appr,17,1)[0]
    x_guess_l.append(x_guess)
x_real = []
for i in data:
    x_real.append(i[1])
truth_e = 0
truth_a = 0
truth_e_l = []
truth_a_l = []
for j in range(0,len(x_g)):
    truth_e = 0
    truth_a = 0
    for i in range(0,len(x_g[0])):
        if x_g[j][i] == x_real[j][i]:
            truth_e +=1
        if x_guess_l[j][i] == x_real[j][i]:
            truth_a +=1
    truth_e_l.append(truth_e)
    truth_a_l.append(truth_a) 
    print("Approximate key result for x(={}) = {}".format(binaryToHex(x_real[j]),truth_a))
    print("Guessed key result for x(={}) = {}".format(binaryToHex(x_real[j]),truth_e))

#%%Task5 - Test
print("\n\nTask 5")
lu = 32
lx = 32
l = 16
lk = 32
n = 5 

k0 = 0x87654321
k0 = hexToBinary(k0)
k0 = k0.zfill(lk) 
k0 = list(k0)
k0 = [int(i) for i in k0] 


u = 0x12345678 #problem with this hex - in slides zero paddling applied
u = hexToBinary(u)
u = u.zfill(lu) #zfill func to equalize current size of u to lu
u = list(u)
u = [int(i) for i in u] 

x5,k = Encryption(u,k0,n,5)
printEnc(x5)
#%%%Task 6 
print("\n\nTask 6")
filename = "KPApairsPrague_nearly_linear.hex"
data = readFile_Binary(filename)

lu = len(data[0][0])
lx = len(data[0][1])
lk = lu
k6_l = []
c = np.identity(lu)
a = find_A(lu,lk)
b = find_B(lu,lk)
for i in data:
    k6 = nearly_linear_cryptoanalysis_KPA(i[0], i[1])
    print("k_guess",binaryToHex(k6))
    k6_l.append(k6)
    #Ak⊕Bu⊕Cx=0
    # res6 = np.dot(a,k) + np.dot(b,i[0])
    # res6 = np.remainder((res6 + np.dot(c,i[1])),2)
    # print("A(k_guess = {}) XOR Bu XOR Cx= {}".format( binaryToHex(k_guess),res6))
#%%Task 7 - Test
print("\n\nTask 7")
lu = 16
lx = 16
l = 8
lk = 16
n = 13

k0 = 0x369C
k0 = hexToBinary(k0)
k0 = k0.zfill(lk)
k0 = list(k0)
k0 = [int(i) for i in k0] 

u = hexToBinary(0x0000)
u = hexToBinary(u)
u = u.zfill(lu) #zfill func to equalize current size of u to lu
u = list(u)
u = [int(i) for i in u] 

x7,k = Encryption(u,k0,n,7)
printEnc(x7)

u_res7 = Decryption(x7,k,n,7) #Decryption test of Task7
printDec(u_res7)
#%% Task 8 - Meet in Middle Attack

print("\n\nTask 8")
filename = "KPApairsPrague_non_linear.hex"
data = readFile_Binary(filename)
lu = len(data[0][0])
lx = len(data[0][1])
import time

start = time.time()
cardinality_k = 2**len(data[0][0])
x_pp_list = []
x_p_list = []
keys_list = []
for i in data:
    for k in range(0,cardinality_k):
        k_p = np.random.randint(2, size=lu)
        x_p= Encryption(i[0],k_p,n,7)[0]
        k_pp = np.random.randint(2, size=lu)
        k_pp_l = []
        for j in range(0,lu):
            k_pp_l.append(keyGeneration(k_pp, j))
        x_pp = Decryption(i[1],k_pp_l,n,7)
        if x_p == x_pp:
            keys_list.append([[k_p],[k_pp]])
            print("For u = {}\nFor x = {}\nk' = {}\nk'' = {}".format(binaryToHex(i[0]),binaryToHex(i[1]),k_p,k_pp))

end = time.time()
print("Elapsed time in seconds:",end - start)
