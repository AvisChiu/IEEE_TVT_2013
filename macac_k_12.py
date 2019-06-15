import math
import numpy as np
import time

# wi-fi capacity
capacity_C = 58

C = capacity_C
	
# number of share channel, number of guard channel = C - S
share_S = 50

S = share_S
	
queue_size_K = 12

K = queue_size_K
	
# handoff call arrival rate
lambda_H = 24.0
	
# new call arrival rate
lambda_N = 44
	
# dwell time at stop or moving phase
xi_S = 1.0/3.0
xi_M = 1.0/6.0
	
# call duration time at stop or moving phase
mu_S = 1.0/6.0
mu_M = 1.0/6.0
	

max_i = 1+1
max_j = (capacity_C+queue_size_K)+1

pi = np.full((max_i,max_j),1.0/(max_i*max_j))

pi_new = pi.copy()

pi_list = []


while True:
	for i in range(max_i):
		for j in range(max_j):
            
				# (1)
			if i==0 and j==0:
				pi_new[i][j] = (( j + 1)*mu_S*pi[i,j+1] + xi_M*pi[1,j])/((lambda_N + lambda_H)+xi_S)
				
				# (2)
			elif i==0 and 0<j and j<share_S:
				pi_new[i][j] = ((lambda_N + lambda_H)*pi[i,j-1] +( j + 1)*mu_S*pi[i,j+1] + xi_M*pi[1,j])/((lambda_N + lambda_H)+j*mu_S + xi_S)

				# (3)
			elif i==0 and j==share_S:
				pi_new[i][j] = ((lambda_N + lambda_H)*pi[i,j-1] +( j + 1)*mu_S*pi[i,j+1] + xi_M*pi[1,j])/(lambda_H + j*mu_S + xi_S)

				# (4)		 
			elif i==0 and share_S<j and j<capacity_C:
				pi_new[i][j] = (lambda_H*pi[i,j-1]+(j+1)*mu_S*pi[i,j+1]+xi_M*pi[1,j])/(lambda_H+j*mu_S+xi_S)

				# (5)
			elif i==0 and capacity_C<=j and j<(capacity_C+queue_size_K):
				pi_new[i][j] = (lambda_H*pi[i,j-1] + C*mu_S*pi[i,j+1] + xi_M*pi[1,j])/(lambda_H + C*mu_S + xi_S)

				# (6)
			elif i==0 and j==(capacity_C+queue_size_K):
				pi_new[i][j] = (lambda_H*pi[i,j-1] + xi_M*pi[1,j])/(C*mu_S + xi_S)

				# (7)
			elif i==1 and j==0:
				pi_new[i][j] = (( j + 1)*mu_M*pi[i,j+1] + xi_S*pi[0,j])/(lambda_N + xi_M)

				# (8)
			elif i==1 and 0<j and j<capacity_C:
				pi_new[i][j] = (lambda_N*pi[i,j-1]+(j+1)*mu_M*pi[i,j+1]+xi_S*pi[0,j])/(lambda_N +j*mu_M +xi_M)

				# (9)
			elif i==1 and j==capacity_C:
				pi_new[i][j] = (lambda_N*pi[i,j-1] + C*mu_M*pi[i,j+1] + xi_S*pi[0,j])/(j*mu_M + xi_M)

				# (10)
			elif i==1 and capacity_C<j and j<(capacity_C+queue_size_K):
				pi_new[i][j] = (C*mu_M*pi[i,j+1] + xi_S*pi[0,j])/(C*mu_M + xi_M)

				# (11)
			elif i==1 and j==(capacity_C+queue_size_K):
				pi_new[i][j] = (xi_S*pi[0,j])/(C*mu_M + xi_M)
				
			else:
				print("OUCH")
				pass
		
		
	pi_sum = 0
	for i in range(max_i):
		for j in range(max_j):
			pi_sum += pi_new[i,j]
		
	pi_new /= pi_sum
		
	#print(pi_new)
	
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

for j in range(S,C+K+1):
	NCBP += pi[0][j]

for j in range(C,C+K+1):
	NCBP += pi[1][j]

# print(NCBP)
	
HCDP = 0
	
for j in range(0,C+K+1):
	HCDP += pi[0,j]
		
HCDP = pi[0,C+K]/HCDP
	
print(HCDP)