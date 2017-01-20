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
  def __init__(self, mean=0, std=0):
    """ initialize class variables 'mean' and 'std'
    """
    self.mean = mean
    self.std = std  


def CoefficientOfVariation4D(inputFilename, maskFilename):
  """ compute voxelwise coefficient of variation on 4D fMRI data
  """
  img = nib.load(inputFilename)
  img_data = img.get_data()
  img_mask = nib.load(maskFilename)
  img_mask_data = img_mask.get_data()
  img_mask_idx = np.nonzero(img_mask_data)
  mean_img = np.zeros(img_mask_data.shape)
  img_data_nanmean = np.nanmean(img_data, axis=3)
  img_data_nanstd = np.nanstd(img_data, axis=3)
  img_data_cv = np.divide(img_data_nanstd, img_data_nanmean)
  print(img_data_cv.shape)

  ### if need to save nanmean or nanstd images ###
  #img_nanmean = nib.Nifti1Image(img_data_nanmean, img.affine, img.header)
  #img_nanmean.to_filename('test_nanmean.nii.gz')
  #img_nanstd = nib.Nifti1Image(img_data_nanstd, img.affine, img.header)
  #img_nanstd.to_filename('test_nanstd.nii.gz')
  ###

  stats = StatsCoV(np.nanmean(img_data_cv), np.nanstd(img_data_cv))
  return(stats)
  
