# -*- coding: utf-8 -*-
"""
Test file
"""

#from ahp import ahp
import numpy as np

# Random Consistency Index (RI)
RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 
      1.51, 1.48, 1.56, 1.57, 1.59]

# Read data
data = np.fromfile('C:\\Users\\Administrator\\Desktop\\Graduation_Project\\Code\\fAHPy\\data', dtype=np.longdouble, sep=" ")
n=int(len(data)**(0.5))
A = np.reshape(data, (n, n))

# Complete inferior part with inverse values 1/x
for a in range(len(A)):
    for b in range(len(A)):
        if a > b:
            A[a][b] = 1./A[b][a]
#进行数组小数点约定

A[A > 1] = np.round(A[A > 1])
A[A < 1] = np.round(A[A < 1], 3) # Round values

print("Decision Matrix:\n", A)

# Normalize matrix
A = A**1

# Eigenvalue
alpha = A.sum(axis=1)
w = alpha/A.sum()
print("\nWeights:\n", w.round(4))

# Consistency ratio calculation
CI = (np.amax(alpha)-n)/(n-1)
CR = CI/RI[n-1]
print("\nConsistency Ratio:", CR)