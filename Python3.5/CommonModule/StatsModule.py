#!/home/wdcai/anaconda3/bin/python3.5 -tt

import sys
import os
import os.path
import numpy as np
import statsmodels

def Regression(y, X):
  moorePenrosePseduoInverseX = np.dot(np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X))
  b = np.dot(moorePenrosePseduoInverseX, y)
  return b
