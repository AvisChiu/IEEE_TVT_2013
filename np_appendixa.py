import math
import numpy as np
import time



# wi-fi capacity
capacity_C = 58
    
# number of share channel, number of guard channel = C - S
share_S = 58   


C = capacity_C
S = share_S

    
# handoff call arrival rate
lambda_H = 24.0
    
# new call arrival rate
lambda_N = 44
    
# dwell time at stop or moving phase
xi_S = 1/3.0
xi_M = 1/6.0
    
# call duration time at stop or moving phase
mu_S = 1/6.0
mu_M = 1/6.0
    
	

max_i = 1+1
max_j = capacity_C+1

pi = np.full((max_i,max_j),1.0/(max_i*max_j))

pi_new = pi.copy()

pi_list = []


while True:

    for i in range(max_i):
        for j in range(max_j):
            
            # (1)
            if i==0 and j==0:
                pi_new[i][j] = ((j+1)*mu_S*pi[i][j+1] + xi_M*pi[1][j]) / (lambda_H+lambda_N+xi_S)

            # (2)
            if i==0 and j>0 and j<capacity_C:
                pi_new[i][j] = ((lambda_H+lambda_N)*pi[i][j-1] + (j+1)*mu_S*pi[i][j+1] + xi_M*pi[1][j]) / (lambda_H+lambda_N+xi_S+j*mu_S)

            # (3)  
            if i==0 and j==capacity_C:
                # pi[i][j] = (lambda_H*pi[i][j-1] + xi_M*pi[1][j]) / (capacity_C*mu_S + xi_S)
                pi_new[i][j] = ((lambda_H+lambda_N)*pi[i][j-1] + xi_M*pi[1][j]) / (capacity_C*mu_S + xi_S)

            # (4)
            if i==1 and j==0:
                pi_new[i][j] = ((j+1)*mu_M*pi[i][j+1] + xi_S*pi[0][j]) / (lambda_N + xi_M)

            # (5)
            if i==1 and j>0 and j<capacity_C:
                pi_new[i][j] = (lambda_N*pi[i][j-1] + (j+1)*mu_M*pi[i][j+1] + xi_S*pi[0][j]) / (lambda_N+j*mu_M+xi_M)

            # (6)
            # if i==1 and j==capacity_C:
            #     pi[i][j] = (lambda_N*pi[i][j] + capacity_C*mu_M*pi[i][j] + xi_S*pi[0][j]) / (j*mu_M+xi_M)

            if i==1 and j==capacity_C:
                pi_new[i][j] = (lambda_N*pi[i][j-1] + xi_S*pi[0][j]) / (j*mu_M+xi_M)
	

    
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




NCBP = pi[0][C]+pi[1][C]
HCDP_m = 0

for j in range(0,C+1):
    HCDP_m += pi[0][j]


HCDP = pi[0][C] / HCDP_m  
	
	
print(NCBP)
print(HCDP)


