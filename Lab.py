#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 23:08:16 2020

@author: Ayca
"""

#import random
import numpy as np
#messagelength lu =lx =2l=32 , 
#keylengthlk =32 , nr.ofroundsn=17
lk = 32
lu = 32
lx = 32
l = lu/2
n = 17
k= []

k0 = np.random.randint(2, size=lk)
u = np.random.randint(2, size=lu)

z0 = u[:int(lu/2)]
y0 = u[int(lu/2):]

#%%Methods
#import binascii

def hexToBinary(h):
    return"{0:b}".format(int(h))
    
def linearTF(z,w):
    v = []
    for i in range (0,len(z)):
        v.append((z[i]+w[i])%2)
    return v

def transposer(y,z):
    return z,y

def roundFunc(y,k): #task1
    w =[]
    for j in range(0,len(y)):
        if j>=0 and j<=len(y)/2: #0th bit added for first condition j>=1
            w.append(( y[j] + k[int(4*j-3)])%2)  #mod2 defined since 1+1 results 2
        elif j>len(y)/2 and j<=len(y):
            w.append((y[j] + k[int(4*j-2*l)])%2)
        
    
    return w

def nearlyLinear_roundFunc(y,k): #task 5
    w =[]
    for j in range(0,len(y)):
        if j>=0 and j<=len(y)/2: #0th bit added for first condition j>=1
            w.append(( y[j] + (k[int(4*j-3)] & (y[2*j-1] & k[2*j-1] & k[2*j] & k[4*j-2]))))  #mod2 defined since 1+1 results 2
        elif j>len(y)/2 and j<=len(y):
            w.append(( y[j] + (k[int(4*j-2*len(y))] &  k[2*j-1] & k[2*j] & y[2*j-len(y)])))
        
    
    return w
def nonLinear_roundFunc(y,k): #task7
    w = []
    for j in range(0,len(y)):
        if j>=0 and j<=len(y)/2: #0th bit added for first condition j>=1
            w.append((y[j] & k[2*j-1])  & (y[2*j-1] & k[2*j]) & k[4*j])
        elif j>len(y)/2 and j<=len(y):
            w.append((y[j] & k[2*j-1])  & (k[int(4*j-2*l)] & k[2*j]) & y[2*j-len(y)])
        
    
    return w
def subkeyGeneration(k,i,lk):
    temp_k=[]
    for j in range(0,len(k)):
        temp_k.append(k[((5*i+j-1)%lk)])

    return temp_k
#%%
y = [y0]
z = [z0]
w = []
v = []
k =[k0]
for i in range(0,n):
    print("\n\nIteration i = ",i)
    w.append(roundFunc(y[i],k[i]))
    print("w[{}]:{}".format(i,w[i]))
    v.append(linearTF(z[i],w[i]))
    print("v[{}]:{}".format(i,v[i]))
    temp_z_next,temp_y_next = transposer(y[i],z[i]) #def transposer(y,z):
    if(len(z)<n and len(y)<n):
        y.append(temp_y_next)
        z.append(temp_z_next)
        print("znext:{} ynext:{}".format(temp_z_next,temp_y_next))
        k.append(subkeyGeneration(k[i],i,lk)) #is next k defined by first key or last key?

x = np.concatenate((v[n-1],y[n-1]), axis=None)
print("Ciphertext x:",x)
        
#%%
