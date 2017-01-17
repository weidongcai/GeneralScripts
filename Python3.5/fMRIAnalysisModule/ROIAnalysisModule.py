#!/home/wdcai/anaconda/bin/python3.5 -tt
##################################
# Weidong Cai, 1/17/2017
##################################

import sys
import os
import numpy as np
import scipy as sp
import scipy.io as spio

import nibabel as nib
import nilearn
from nilearn.masking import apply_mask

import matplotlib.pyplot as plt 

def ExtractNiiROITsFromfMRI(subjectList, subjectDataList, roiList, roiDataList, outputPath):
  ##################################
  # This script extracts ROI mean time series from 4D fMRI data
  # ROIs are nii files
  ##################################
  if not os.path.exists(outputPath):
    os.mkdir(outputPath)
  
  for i in range(len(subjectList)):
    isubj = subjectList[i]
    isubj_data = subjectDataList[i]
    print(isubj)
    isubj_data_nii = isubj_data + '.nii'
    isubj_data_nii_gz = isubj_data_nii + '.gz'
    if os.path.isfile(isubj_data_nii_gz):
      isubj_data_fname = isubj_data_nii_gz
    elif os.path.isfile(isubj_data_nii):
      isubj_data_fname = isubj_data_nii
    else:
      print('error: cannot find ' + isubj_data)
      sys.exit(1)

    ts_nanmean_orig = [] # create empty list for time series output

    ioutputFname = outputPath + '/' + isubj + '_data.mat' # output file

    for j in range(len(roiList)):
      jroi = roiList[j]
      print('extracting ' + jroi)
      jroi_data = roiDataList[j]
      jroi_data_nii = jroi_data + '.nii'
      jroi_data_nii_gz = jroi_data_nii + '.gz'
      if os.path.isfile(jroi_data_nii_gz):
        jroi_data_fname = jroi_data_nii_gz
      elif os.path.isfile(jroi_data_nii):
        jroi_data_fname = jroi_data_nii
      else:
        print('error: cannot find ' + jroi_data)
        sys.exit(1)
      isubj_in_jroi = apply_mask(isubj_data_fname, jroi_data_fname)
      isubj_in_jroi_nanmean = np.nanmean(isubj_in_jroi, axis=1) 
      
      ############################
      # data plotting script for testing purpose
      # plt.plot(isubj_in_jroi_nanmean)
      # plt.show()
      # sys.exit(1)
      ############################

      ts_nanmean_orig.append(isubj_in_jroi_nanmean)

    spio.savemat(ioutputFname, mdict={'ts_nanmean_orig':ts_nanmean_orig, 'subject_id': isubj, 'roi_name':roiList})
    #sys.exit(1)

