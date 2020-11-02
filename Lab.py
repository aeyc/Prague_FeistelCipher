#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 04:23:08 2020
@author: Ayca & Emanuele
"""

#%%
def hexToBinary(h):
    return "{0:b}".format(int(h))

##Feistel cipher with linear f
def linear_f(y,k):
    l=int(len(y))
    w =[]
    for j in range(1,l+1): #1 to 16
        if j>=1 and j<=l/2: #1 to l/2 = 8
            tmp = y[j-1] ^ k[int(4*j-3)-1]
        elif j>l/2 and j <=l: #15
            tmp = y[j-1] ^ k[int(4*j-2*l)-1]
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

#%%
k0 = 0x80000000
k0 = list(hexToBinary(k0))
k0 = [int(i) for i in k0] 
k=[]

u = 0x80000000
u = list(hexToBinary(u))
u = [int(i) for i in u] 


z = [] #create z
y = [] #create y
w = [] #create w
v = [] #create v

#%% Encryption

y.append(u[:int(len(u)/2)]) #initialize y
z.append(u[int(len(u)/2):]) #initialize z

lu = lx = int(len(u)) #messagelength lu=lx=2*l
l = int(lu/2)
lk = int(len(u)) #keylength lk
n = 17 #n nr.ofrounds

for i in range(0,n):
    
    new_key = keyGeneration(k0,i) #generate key for i-th round
    k.append(new_key) ##attach it to list of key
    
    w_temp = linear_f(y[i],k[i]) #compute w
    w.append(w_temp) ##attach it to list of w
    
    v.append(addition(z[i],w[i])) #compute v and attach to its list
    
    new_z,new_y = y[-1],v[-1] #transposition
    
    y.append(new_y) #y for the next round
    z.append(new_z) #z for the next round
    
    x =  y[i] +v[i]
    
print("x:", x)

#%%
#outputing the hex version of cipher text
x_str = ""
for i in range(0,len(x)):
    x_str += str(x[i])
x_hex = hex(int(x_str, 2))
print("Hex verison of x: ",hex(int(x_str, 2)))
#%% Decryption - Task2
yx = u[:int(len(x)/2)] #initialize y
vx = u[int(len(x)/2):] #initialize z
k.reverse()
u_l = []
for i in range(0,n):
    wx = linear_f(yx,k[0])
    zx = addition(vx,wx)
    vx = yx
    yx = zx
    ux = yx + vx

u_str = ""
for i in range(0,len(u)):
    u_str += str(u[i])
u_hex = hex(int(u_str, 2))
print("Hex verison of u: ",hex(int(u_str, 2)))    
