#!/home/wdcai/anaconda3/bin/python3.5 -tt

import sys
import os
import os.path
import numpy as np
import scipy as sp
import scipy.signal as spsi
import statsmodels

def princomp(X):
  """
  X is a nxp matrix
  returns:
  coeff is a pxp matrix, each column containing coeffiicents for each principal component
  score is a nxp matrix, the representation of X in the pca sace
  latent contains the eigenvalues of the covariance matrix of A
  """
  X_demean = (X - np.mean(X.T, axis=1)).T
  [latent, coeff] = np.linalg.eig(np.cov(X_demean))
  score = np.dot(coeff.T, X_demean)
  return coeff, score, latent

def NormalizeData(X):
  '''
  X is a nxp matrix, n is number of samples, p is number of variables/features
  demean and divided by std
  '''
  normX = (X - np.mean(X, axis=0))/np.std(X, axis=0)
  return normX

def LinearDetrend(X):
  '''
  linear detrend X (nxk)
  input X is a nxp matrix
  '''
  detrendX = spsi.detrend(X, axis=0, type='linear')
  return detrendX

def Regression(y, X):
  '''
  multiple linear regression:
  y is a nxk matrix: n is number of sample, k is number of variables
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
  b = Regression(y, X)
  residual = y - np.dot(X, b)
  return residual
