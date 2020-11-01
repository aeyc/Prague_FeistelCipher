#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 04:23:08 2020

@author: Ayca
"""

#%%
def hexToBinary(h):
    return "{0:b}".format(int(h))
def linear_f(y,k,l):
    w =[]
    for j in range(1,l+1):
        if j>=1 and j<=l/2:
            tmp = (y[j-1] + k[int(4*j-3 -1)])%2
        elif j>l/2 and j <=l:
            tmp = (y[j-1] + k[int(4*j-2*l -1)])%2
        w.append(tmp)
        # print("w in linear f",w)
    return w
def addition(z,w):
    v=[]
    for i in range(0,len(w)):
        v.append((w[i]+z[i])%2)
    return v
def transposer(v,y):
    return y,v #call z,y=(z,y)
def keyGeneration(k,lk):
    tmp = []
    for j in range(1,len(k)+1):
        #ki(j)=k(((5i+j−1)modlk)+1)
        #print(((5*i+j-1)%lk)+1 -1)
        tmp.append(k[((5*i+j-1)%lk)+1 -1])
    return tmp
#%%
# k0 = np.random.randint(2, size=lk)
# u = np.random.randint(2, size=lu)
k0 = 0x80000000
k0 = list(hexToBinary(k0))
k0 = [int(i) for i in k0] 
k=[]
k.append(k0)

u = 0x80000000
u = list(hexToBinary(u))
u = [int(i) for i in u] 

print("u: ", u)
print("k0: ", k0)

z = []
y = []
w = []
v = []
#%%
z.append(u[:int(len(u)/2)])
y.append(u[int(len(u)/2):])
print("z0:{}, len(z0):{} ".format(z[0],len(z[0])))
print("y0:{}, len(y[0]):{}".format(y[0],len(y[0])))
lu = 32
lx = 32
l = int(lu/2)
lk = 32
n = 17

# w.append(linear_f(y[0],k[0],l))
# print("w[0]",w[0])
# v.append(addition(z[0],w[0]))
# print("v[0]",v[0])
# new_z,new_y = transposer(z,y)
# y.append(new_y)
# z.append(new_z)

for i in range(1,n):
    print("\n\n Iteration:",i)
    w_temp = linear_f(y[i-1],k[i-1],l)
    w.append(w_temp)
    print("w[{}]:{}".format(i,w[i-1]))
    v.append(addition(z[i-1],w[i-1]))
    print("v[{}]:{}".format(i,v[i-1]))
    new_z,new_y = y[i-1],v[i-1]
    print("potential_x: ", v[-1]+y[-1])
    print("new_z:{}\nnew_y:{}".format(new_z,new_y))
    y.append(new_y)
    z.append(new_z)
    new_key = keyGeneration(k[i-1],lk)
    
    k.append(new_key)
    print("new_key",k[i])
    