#!/home/wdcai/anaconda3/bin/python3.5 -tt
##################################
# Weidong Cai, 1/17/2017
##################################

import sys
import os
import numpy as np
import numpy.matlib
import scipy as sp
import scipy.io as spio
import nibabel as nib
import matplotlib.pyplot as plt 

sys.path.append('/home/wdcai/Library/Python3.5/CommonModule')

def CorrelationIcaMaps(sourceIcFname, targetIcFname, maskFname):
  """
  This module finds the IC that has the highest correlation 
  """
  img_src = nib.load(sourceIcFname)
  data_src = img_src.get_data()
  img_tgt = nib.load(targetIcFname)
  data_tgt = img_tgt.get_data()
  img_msk = nib.load(maskFname)
  data_mask = img_msk.get_data()
  idx_mask = np.nonzero(data_mask)

  tgt2src_cc = np.zeros(data_tgt.shape[3], data_src.shape[3])
  for it in data_tgt.shape[3]:
    idata_tgt = data_tgt[:,:,:,it]
    idata_tgt_vec = idata_tgt(idx_mask)
    for ic in data_src.shape[3]:
      print('computing correlation: target ' + it + ' source ' + ic)
      idata_src = data_src[:,:,:,ic]
      idata_src_vec = idata_src[idx_mask]
      tgt2src_cc[it, ic] = np.corrcoef(idata_tgt_vec, idata_src_vec)[0, 1]

  return tgt2src_cc
