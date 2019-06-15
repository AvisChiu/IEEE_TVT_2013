import math
import numpy as np
import time



C = 58
S = 50

lam_H = 24.0
    

lam_N = 44

xi_S = 1/3.0
xi_M = 1/6.0

mu_S = 1/6.0
mu_M = 1/6.0


max_i = 1+1
max_j = C+1
    

pi = np.full((max_i,max_j),1.0/(max_i*max_j))

pi_new = pi.copy()

pi_list = []


while True:
    for i in range(max_i):
        for j in range(max_j):
            
            # (1)
            if i==0 and j==0:
                pi_new[ i,j] =(( j + 1)*mu_S*pi[ i,j+1 ]+ xi_M*pi[ 1,j])/((lam_N + lam_H)+xi_S)
            # (2)
            if i==0 and 0<j and j<S:
                pi_new[ i,j ]=((lam_N + lam_H)*pi[ i,j-1 ]+( j + 1)*mu_S*pi[ i,j+1 ]+ xi_M*pi[ 1,j])/((lam_N + lam_H)+j*mu_S + xi_S)
            # (3)
            if i==0 and j==S:
                pi_new[ i,j ]=((lam_N + lam_H)*pi[ i,j-1 ]+( j + 1)*mu_S*pi[ i,j+1 ]+ xi_M*pi[ 1,j])/(lam_H + j*mu_S + xi_S)
            # (4)
            if i==0 and S<j and j<C:
                pi_new[ i,j ]=(lam_H*pi[ i,j-1]+(j + 1)*mu_S*pi[ i,j+1]+xi_M*pi[ 1,j])/(lam_H+j*mu_S+xi_S)
            # (5)
            if i==0 and j==C:
                pi_new[ i,j ]= (lam_H*pi[ i,j-1 ]+ xi_M*pi[ 1,j])/(C*mu_S + xi_S)
            # (6)
            if i==1 and j==0:
                pi_new[ i,j ]=(( j + 1)*mu_M*pi[ i,j+1 ]+ xi_S*pi[ 0,j])/(lam_N + xi_M)
            # (7)
            # if i==1 and 0<j and j<S:
            #     pi_new[ i,j ]= (lam_N *pi[ i,j-1 ]+( j + 1)*mu_M*pi[ i,j+1 ]+ xi_S*pi[ 1,j])/(lam_N + j*mu_M + xi_M)
            if i==1 and 0<j and j<S:
                pi_new[ i,j ]= (lam_N *pi[ i,j-1 ]+( j + 1)*mu_M*pi[ i,j+1 ]+ xi_S*pi[ 0,j])/(lam_N + j*mu_M + xi_M)
            
            
            # (8)
            # if i==1 and j==S:
            #     pi_new[ i,j] =(lam_N*pi[ i,j-1]+(j + 1)*mu_M*pi[ i,j+1]+xi_S*pi[ 1,j])/(j*mu_M +xi_M)
            if i==1 and j==S:
                pi_new[ i,j] =(lam_N*pi[ i,j-1]+(j + 1)*mu_M*pi[ i,j+1]+xi_S*pi[ 0,j])/(j*mu_M +xi_M)
            
            # (9)
            # if i==1 and S<j and j<C:
            #     pi_new[ i,j] =(( j + 1)*mu_M*pi[ i,j+1 ]+ xi_S*pi[ 1,j])/(j*mu_M + xi_M)
            if i==1 and S<j and j<C:
                pi_new[ i,j] =(( j + 1)*mu_M*pi[ i,j+1 ]+xi_S*pi[ 0,j])/(j*mu_M + xi_M)
            
            # (10)
            # if i==1 and j==C:
            #     pi_new[ i,j] = (xi_S*pi[ 1,j])/(C*mu_M + xi_M)
            if i==1 and j==C:
                pi_new[ i,j] = (xi_S*pi[0,j])/(C*mu_M + xi_M)
	
	

    
    pi_sum = 0
    for i in range(max_i):
        for j in range(max_j):
            pi_sum += pi_new[i,j]
            
    pi_new /= pi_sum            # important: sum = 1

    pi = pi_new.copy()
    pi_list.append(pi_new.copy())
		
    if len(pi_list)<3:
        continue
			
    while len(pi_list)>3:
        pi_list.pop(0)
        
    oscillate = True
    for i in range(max_i):
        for j in range(max_j):
            if abs(pi_list[2][i,j]-pi_list[0][i,j])>0.000001:
                oscillate = False
    if oscillate:
        for i in range(max_i):
            for j in range(max_j):
                pi[i,j] = (pi_list[1][i,j]+pi_list[2][i,j])/2
                
        continue
        
    converge = True
    for i in range(max_i):
        for j in range(max_j):
            if abs(pi_list[2][i,j]-pi_list[1][i,j])>0.000001:
                converge = False

    if converge:
        break



NCBP = 0 
HCBP_m = 0
HCBP = 0

for j in range(S,C+1):
    NCBP += pi[0][j] + pi[1][j]

for j in range(0,C+1):
    HCBP_m += pi[0][j]

HCBP = pi[0][C] / HCBP_m

print(NCBP)
# print(HCBP)
