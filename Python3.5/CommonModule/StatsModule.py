#!/home/wdcai/anaconda3/bin/python3.5 -tt

import sys
import os
import os.path
import numpy as np
import statsmodels

def Regression(y, X):
  '''
  multiple linear regression:
  y is a nxk matrix: n is observation sample size, k is observation channel size
  X is a nxp matrix: p is number of regressors
  note: check constants are added in the X
  '''
  # check whether constants are added in the X
  if not (np.sum(X[:,0])==X.shape[0]):
    print('Error: constants are not added in the regression')
    sys.exit(1)
  else:
    moorePenrosePseduoInverseX = np.dot(np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X))
    b = np.dot(moorePenrosePseduoInverseX, y)
    return b

def ResidualFromRegression(y, X):
  b = Regression(y, X):
  residual = y - np.dot(X, b)
  return residual
