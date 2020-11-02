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

    for i in range(0,n):
        
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
        
        if (i<n-1):
            new_z,new_y = y,v #transposition
            y = new_y #y for the next round
            z = new_z #z for the next round
        
        x =  y +v

        
        
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
        print(matrixI)
        tmp = Encryption(matrixI[i],null_vector,17,1)
        a.append(tmp)
    return a

#find matrix B
def find_B(lu,lk):
    matrixI = np.identity(lk)
    b=[]
    null_vector = np.zeros(lu, dtype=int)
    for i in range (0, lu):
        tmp = Encryption(null_vector,matrixI[i],17,1)
        b.append(tmp)
    return b

#linear cryptoanalusis KPA
def linear_cryptoanalysis_KPA(u,x):
    a = find_A(int(len(u)),int(len(u)))
    a = np.linalg.inv(a)
    b = find_B(int(len(u)),int(len(u)))
    k = np.dot(a,x+np.dot(b,u))
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
u_res1 = Decryption(x1,k,n,1)

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

x5,k = Encryption(u,k0,n,7)
#%% Task 3-4 - Test

#trying to find k with linear cipher
#k_hacked = linear_cryptoanalysis_KPA(u,x1)

