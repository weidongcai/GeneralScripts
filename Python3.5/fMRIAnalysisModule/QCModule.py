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
  """
  define a class for coefficient of variation statisticas
  spatial mean of temporal mean of 4D data
  spatial std of temporal mean of 4D data
  spatial mean of temporal std of 4D data
  spatial std of temporal std of 4D data
  spatial mean of temporal CoV of 4D data
  spatial std of temporal CoV of 4D data
  spatial max of temporal Cov of 4D data
  spatial min of temporal Cov of 4D data
  """
  def __init__(self, smean_tmean=0, sstd_tmean=0, smean_tstd=0, sstd_tstd=0, smean_tCoV=0, sstd_tCoV=0, smax_tCoV=0, smin_tCoV=0):
    """ 
    initialize class variables 'mean' and 'std'
        
    """
    self.smean_tmean = smean_tmean
    self.sstd_tmean = sstd_tmean
    self.smean_tstd = smean_tstd
    self.sstd_tstd = sstd_tstd
    self.smean_tCoV = smean_tCoV
    self.sstd_tCoV = sstd_tCoV
    self.smax_tCoV = smax_tCoV
    self.smin_tCoV = smin_tCoV

class StatsVoxInData(object):
  """
  define a class for couting number of voxels in Data
  number of nonzero voxels in Data within Mask
  number of nonzero voxels in Mask
  ratio of nonzero vxoels in Data within Mask relative to number of nonzero voxels within Mask
  """
  def __init__(self, n_voxel_in_data=0, n_voxel_in_mask=0, ratio_n_voxel_in_data_to_mask=0):
    """
    initialize varialbes
    """
    self.n_voxel_in_data = n_voxel_in_data
    self.n_voxel_in_mask = n_voxel_in_mask
    self.ratio_n_voxel_in_data_to_mask = ratio_n_voxel_in_data_to_mask


def CoefficientOfVariation4D(inputFilename, maskFilename):
  """ 
  compute voxelwise coefficient of variation on 4D fMRI data
  """

  img = nib.load(inputFilename)
  img_data = img.get_data()
  img_mask = nib.load(maskFilename)
  img_mask_data = img_mask.get_data()
  img_mask_idx = np.nonzero(img_mask_data)
  img_data_nanmean = np.nanmean(img_data, axis=3)
  img_data_nanstd = np.nanstd(img_data, axis=3)
  img_data_cv = np.divide(img_data_nanstd, img_data_nanmean)

  ### if need to save nanmean or nanstd images ###
  #img_nanmean = nib.Nifti1Image(img_data_nanmean, img.affine, img.header)
  #img_nanmean.to_filename('test_nanmean.nii.gz')
  #img_nanstd = nib.Nifti1Image(img_data_nanstd, img.affine, img.header)
  #img_nanstd.to_filename('test_nanstd.nii.gz')
  ###

  stats = StatsCoV(np.nanmean(img_data_nanmean[img_mask_idx]), np.nanstd(img_data_nanmean[img_mask_idx]), np.nanmean(img_data_nanstd[img_mask_idx]), np.nanstd(img_data_nanstd[img_mask_idx]), np.nanmean(img_data_cv[img_mask_idx]), np.nanstd(img_data_cv[img_mask_idx]), np.amax(img_data_cv[img_mask_idx]), np.amin(img_data_cv[img_mask_idx]))
  return(stats)

def ComputeNumOfVoxelinData(inputFilename, maskFilename):
  cmd_nVoxelInMask = 'fslstats ' + maskFilename + ' -V'
  cmd_nVoxelInData = 'fslstats ' + inputFilename + ' -k ' + maskFilename + ' -V'
  nVoxelInMask = os.popen(cmd_nVoxelInMask).read().rstrip().split()[1]
  nVoxelInData = os.popen(cmd_nVoxelInData).read().rstrip().split()[1]
  stats = StatsVoxInData(nVoxelInData, nVoxelInMask, float(nVoxelInData)/float(nVoxelInMask))
  return(stats)
