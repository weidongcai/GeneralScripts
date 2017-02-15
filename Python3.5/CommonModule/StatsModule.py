#!/home/wdcai/anaconda3/bin/python3.5 -tt

import sys
import os
import os.path
import numpy as np
import numpy.matlib
import scipy as sp
import scipy.signal as spsi
import statsmodels

def princomp(X):
  """
  X is a nxp matrix
  X_cov is the covariance matrix of X
  returns:
  coeff is a pxp matrix, which is,each column containing coeffiicents for each principal component
  score is a pxn matrix, the representation of X in the pca sace
  latent is a 1xp vector, containing the eigenvalues of the covariance matrix of A
  """
  X_demean = (X - np.matlib.repmat(np.mean(X, axis=0), X.shape[0], 1)).T
  X_cov = np.cov(X_demean)
  latent,coeff = np.linalg.eig(X_cov)
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
