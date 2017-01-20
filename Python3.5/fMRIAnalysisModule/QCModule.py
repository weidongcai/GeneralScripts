#!/home/wdcai/anaconda3/bin/python3.5 -tt

import nibabel as nib
import sys
import os
import os.path
import numpy as np
import scipy as sp
import scipy.io as spion
import scipy.ndimage
import nilearn
import nilearn.image
from nilearn import plotting
import matplotlib.pyplot as plt

class StatsCoV(object):
  """define a class for coefficient of variation statisticas
  """
  def __init__(self, mean_mean=0, std_mean=0, mean_std=0, std_std=0, mean_CoV=0, std_CoV=0):
    """ initialize class variables 'mean' and 'std'
    """
    self.mean_mean = mean_mean
    self.std_mean = std_mean
    self.mean_std = mean_std
    self.std_std = std_std
    self.mean_CoV = mean_CoV
    self.std_CoV = std_CoV  


def CoefficientOfVariation4D(inputFilename, maskFilename):
  """ compute voxelwise coefficient of variation on 4D fMRI data
  """

  img = nib.load(inputFilename)
  img_data = img.get_data()
  img_mask = nib.load(maskFilename)
  img_mask_data = img_mask.get_data()
  img_mask_idx = np.nonzero(img_mask_data)
  #mean_img = np.zeros(img_mask_data.shape)
  img_data_nanmean = np.nanmean(img_data, axis=3)
  img_data_nanstd = np.nanstd(img_data, axis=3)
  img_data_cv = np.divide(img_data_nanstd, img_data_nanmean)

  ### if need to save nanmean or nanstd images ###
  #img_nanmean = nib.Nifti1Image(img_data_nanmean, img.affine, img.header)
  #img_nanmean.to_filename('test_nanmean.nii.gz')
  #img_nanstd = nib.Nifti1Image(img_data_nanstd, img.affine, img.header)
  #img_nanstd.to_filename('test_nanstd.nii.gz')
  ###

  stats = StatsCoV(np.nanmean(img_data_nanmean[img_mask_idx]), np.nanstd(img_data_nanmean[img_mask_idx]), np.nanmean(img_data_nanstd[img_mask_idx]), np.nanstd(img_data_nanstd[img_mask_idx]), np.nanmean(img_data_cv[img_mask_idx]), np.nanstd(img_data_cv[img_mask_idx]))
  return(stats)
  
