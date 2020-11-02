#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 04:23:08 2020
@author: Ayca & Emanuele
"""

#%%
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
        #yi(j) ^ {ki(4j−3) ∧ [yi(2j−1) ∨ ki(2j−1)∨ki(2j)∨ki(4j−2)]} , 1≤j≤l/2
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ (k[int(4*j-3)-1] & 
                            (y[(2*j -1) -1] #y[2j-1]
                            | k[(2*j -1) -1] #k[2j-1]
                            | k[(2*j)-1] #k[2j]
                            | k[(4*j -2) -1]))
        #yi(j) ^ {ki(4j−2l)∧[ki(4j−2l−1) ∨ ki(2j−1) ∨ ki(2j)∨yi(2j−l)]} , l/2<j≤l
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ (k[int(4*j-2*l) -1] & 
                            (k[(4*j-2*l-1) -1]
                             | k[(2*j-1) -1]
                             | k[(2*j) -1]
                             | y[(2*j-l)-1]))
        w.append(tmp)
    return w

def addition(z,w):
    v=[]
    for i in range(0,len(w)):
        v.append((w[i]^z[i]))
    return v

def keyGeneration(k,i):
    tmp = []
    for j in range(1,len(k)+1): # 1 to 32
        tmp.append(k[((5*(i+1)+j-1)%len(k))])
    return tmp

#%% Encryption
def Encryption(u,k,n,taskNumber):
    print("\n\nEncryption:\n")
    y = u[:int(len(u)/2)] #initialize y
    z = u[int(len(u)/2):] #initialize z
    k = []
    #lu = lx = int(len(u)) #messagelength lu=lx=2*l
    #l = int(lu/2)
    #lk = int(len(u)) #keylength lk
    #n = 17 #n nr.ofrounds
    
    for i in range(0,n):
        
        new_key = keyGeneration(k0,i) #generate key for i-th round
        k.append(new_key) ##attach it to list of key
        
        #Calculate round functions base on task number
        if taskNumber == 1:
            w = linear_f(y,k[i]) #compute w
        elif taskNumber == 5:
            w = nearlyLinear_f(y,k[i])
        v = addition(z,w) #compute v and attach to its list
        
        if (i<n-1):
            new_z,new_y = y,v #transposition
            y = new_y #y for the next round
            z = new_z #z for the next round
        
        x =  y +v
        print(x)
        
    print("x:", x)
    binaryToHex(x)
    return x,k

#%% Task 2 - Decryption 
def Decryption(x,k,n,taskNumber):
    print("\n\nDecryption:\n")

    y = x[:int(len(x)/2)] #initialize y
    v = x[int(len(x)/2):] #initialize v
    k.reverse()
    u_l = []
    for i in range(0,n):
        w = linear_f(y,k[i]) #compute w
        z = addition(v,w) #compute v and attach to its list
        
        if (i<n-1):
            new_v,new_y = y,z #transposition
            y = new_y #y for the next round
            v = new_v #z for the next round
        
        u =  y +z
        u_l.append(u)
        
    print("u:", u)
    binaryToHex(u)
    return u,u_l
#%%Task1 - Test
print("Task 1")
k0 = 0x80000000
k0 = list(hexToBinary(k0))
k0 = [int(i) for i in k0] 


u = 0x80000000
u = list(hexToBinary(u))
u = [int(i) for i in u] 
x1,k = Encryption(u,k0,17,1)
u_res1,u_l = Decryption(x1,k,17,1)


