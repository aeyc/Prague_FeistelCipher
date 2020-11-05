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
    print("Hex verison: ",hex(int(x_str, 2)))
    return x_hex

#printEnc function to format output of Encryption
def printEnc(x):
    print("\nEncryption:")
    print("x:", x)
    binaryToHex(x)
    
#printDec function to format output of Decryption
def printDec(u)  :
    print("\nDecryption:")
    print("u:", u)
    binaryToHex(u)
    
    
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
#%%
import numpy as np
#Task 3/4
#find matrix A

def find_A(lu,lk):
    matrixI = np.identity(lk)
    matrixI = matrixI.astype(int)
    a=[]
    null_vector = np.zeros(lu,dtype=int)
    null_vector = null_vector.astype(int)
    for i in range (0, lu):
        tmp = Encryption(matrixI[i],null_vector,17,1)[0]
        #Encryption func returns 2 values: x and k
        # in that case we need to specify whether we want x or k
        a.append(tmp)
    return a

#find matrix B
def find_B(lu,lk):
    matrixI = np.identity(lk)
    b=[]
    null_vector = np.zeros(lu, dtype=int)
    for i in range (0, lu):
        tmp = Encryption(null_vector,matrixI[i],17,1)[0]
        b.append(tmp)
    return b

#linear cryptoanalusis KPA
def linear_cryptoanalysis_KPA(u,x):
    a = find_A(int(len(u)),int(len(u)))
    

    a_inv = np.linalg.inv(a)
    det = np.linalg.det(a)
    a_invb = np.mod(((a_inv.astype(int))*det),2)
    #print("\n\na_inv",a_invb)
   
   
    b = find_B(int(len(u)),int(len(u)))
    #print("\n\nb",b)
    
    k = np.matmul(a_invb,x + np.matmul(b,u))
    k = np.mod(k,2)
    return a,a_invb,b,k

########################################################################################
#main()

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

#%%Task 3-4 
print("\n\nTask 3-4")
#trying to find k with linear cipher
# u = 0x80000000
# u = list(hexToBinary(u))
# u = [int(i) for i in u] 


# k_hacked = linear_cryptoanalysis_KPA(u,x1)
# print(k0==k_hacked)
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
# for i in data:
#     if len(i[0]) == len(i[1]):
#         print("Elements of pair have same lengths")
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