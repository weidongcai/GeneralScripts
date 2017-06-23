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

  tgt2src_cc = np.zeros((data_tgt.shape[3], data_src.shape[3]))
  for it in range(data_tgt.shape[3]):
    idata_tgt = data_tgt[:,:,:,it]
    idata_tgt_vec = idata_tgt[idx_mask]
    for ic in range(data_src.shape[3]):
      idata_src = data_src[:,:,:,ic]
      idata_src_vec = idata_src[idx_mask]
      tgt2src_cc[it, ic] = np.corrcoef(idata_tgt_vec, idata_src_vec)[0, 1]

  return tgt2src_cc

def ThreshNii(inputFname, outputFname, maskFname, threshType, threshValue):
  """
  This module thresholds input nifti file and output thresholded mask
  """
  img_input = nib.load(inputFname)
  data_input = img_input.get_data()
  img_mask = nib.load(maskFname)
  data_mask = img_mask.get_data()
  idx_mask = np.where(data_mask > 0)
  data_input_in_mask = data_input[idx_mask]
  if (threshType == 'intensity'):
    thresh_idx = np.where(data_input_in_mask > threshValue)
  elif (threshType == 'percent'):
    data_input_in_mask_sort = np.sort(data_input_in_mask)[::-1]
    data_input_in_mask_len = len(data_input_in_mask)
    perc_len = np.floor(data_input_in_mask_len * threshValue).astype(int)
    threshValueInIntensity = data_input_in_mask_sort[perc_len]
    thresh_idx = np.where(data_input > threshValueInIntensity)
  data_output = np.zeros(data_input.shape)
  data_output[thresh_idx] = 1
  img_output = nib.Nifti1Image(data_output, img_input.affine, img_input.header)
  nib.save(img_output, outputFname)
  print(outputFname + ' saved')
