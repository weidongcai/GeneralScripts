#!/home/wdcai/anaconda2/bin/python -tt
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

sys.path.append('/home/wdcai/Library/Python/CommonModule')

def get1stEigenTS(X):
  """
  extract 1st eigenvariate TS from X
  X is a txn matrix, t is number of time point, n is number of voxel
  return Y is a tx1 vector
  """
  m,n = X.shape
  if m>n:
    u_,s,v = np.linalg.svd(np.dot(X.T, X))
    v = v.T # matlab & scipy svd difference v = v.T
    v = v[:,0]
    u = np.divide(np.dot(X,v), np.sqrt(s[0]))
  else:
    u,s,v_ = np.linalg.svd(np.dot(X, X.T))
    u = u[:,0]
    v = np.dot(X.T, np.divide(u, np.sqrt(s[0])))
  d = np.sign(np.sum(v))
  u = np.dot(u, d)
  v = np.dot(v, d)
  Y = np.dot(u, np.sqrt(np.divide(s[0],n)))
  return Y

def DecomposeLabeledROIs2IndividualROIs(labeledRoiFname, individualRoiPrefix, outputFolder):
  """
  This module reads in a nii file with rois with different labels (1 to N) and decompose them into individual rois with different files. 
  """
  labeledRoi_img = nib.load(labeledRoiFname)
  labeledRoi_img_data = labeledRoi_img.get_data()
  labeledRoi_intensity_unique = np.unique(labeledRoi_img_data)
  for i in range(len(labeledRoi_intensity_unique)-1):
    iRoi_img_data = np.zeros(labeledRoi_img_data.shape)
    iintensity = labeledRoi_intensity_unique[i+1]
    iRoi_img_data[np.where(labeledRoi_img_data == iintensity)] = 1
    if iintensity < 10:
      iRoi_label = '00' + str(int(iintensity))
    elif iintensity < 100:
      iRoi_label = '0' + str(int(iintensity))
    else:
      iRoi_label = str(int(iintensity))
    ioutput_fname = individualRoiPrefix + iRoi_label + '.nii.gz'
    print 'decomposing to ' + ioutput_fname
    iRoi_img = nib.Nifti1Image(iRoi_img_data, labeledRoi_img.affine, labeledRoi_img.header)
    iRoi_img.to_filename(ioutput_fname)

def MergeNiiROIsByModules(inputRoiList, inputModuleList, outputFname):
  """
  This module write multiple ROIs into one file and labels by their modules
  """
  img_template = nib.load(inputRoiList[0])
  img_header = img_template.header
  img_array = img_template.get_data()
  print img_array.shape
  for i in range(len(inputRoiList)):
    iRoiFname = inputRoiList[i]
    iRoiModule = int(inputModuleList[i])
    print iRoiFname
    print iRoiModule
    iRoiImg = nib.load(iRoiFname)
    iRoiImgArray = iRoiImg.get_data()
    iRoiImgArrayIdx = np.where(iRoiImgArray > 0)
    img_array[iRoiImgArrayIdx] = iRoiModule

  img_template.to_filename(outputFname)

def MergeNiiROIsNumberLabel(inputRoiList, outputFname):
  """
  This module merges a list or ROIs in one nii file. Each ROI is assigned with a different number as intensity
  """
  img_template = nib.load(inputRoiList[0])
  img_header = img_template.header
  img_array = img_template.get_data()
  print img_array.shape
  for i in range(len(inputRoiList)):
    iRoiFname = inputRoiList[i]
    iRoiIntensity = i+1
    iRoiImg = nib.load(iRoiFname)
    iRoiImgArray = iRoiImg.get_data()
    iRoiImgArrayIdx = np.where(iRoiImgArray > 0)
    img_array[iRoiImgArrayIdx] = iRoiIntensity
  img_template.to_filename(outputFname)

def ExtractNiiROITsFromfMRI(subjectList, subjectDataList, roiList, roiDataList, outputPath, outputPostfix):
  """
  This module extracts ROI mean time series from 4D fMRI data
  ROIs are nii files
  """
  if not os.path.exists(outputPath):
    os.mkdir(outputPath)
  
  for i in range(len(subjectList)):
    isubj = subjectList[i]
    isubj_data = subjectDataList[i]
    print isubj
    isubj_data_nii = isubj_data + '.nii'
    isubj_data_nii_gz = isubj_data_nii + '.gz'
    if os.path.isfile(isubj_data_nii_gz):
      isubj_data_fname = isubj_data_nii_gz
    elif os.path.isfile(isubj_data_nii):
      isubj_data_fname = isubj_data_nii
    else:
      print('error: cannot find ' + isubj_data)
      sys.exit(1)
    isubj_img = nib.load(isubj_data_fname)
    isubj_img_data = isubj_img.get_data()

    ts_nanmean_orig = [] # create empty list for time series output
    ts_eigen1_orig = []

    ioutputFname = outputPath + '/' + isubj + '_' + outputPostfix + '.mat' # output file

    for j in range(len(roiList)):
      jroi = roiList[j]
      print('extracting ' + jroi)
      jroi_data = roiDataList[j]
      if jroi_data[-4:] == '.nii':
        jroi_data_nii = jroi_data
        jroi_data_nii_gz = jroi_data_nii + '.gz'
      elif jroi_data[-7:] == '.nii.gz':
        jroi_data_nii_gz = jroi_data
        jroi_data_nii = jroi_data[:-3]
      else:
        jroi_data_nii = jroi_data + '.nii'
        jroi_data_nii_gz = jroi_data_nii + '.gz'
      if os.path.isfile(jroi_data_nii_gz):
        jroi_data_fname = jroi_data_nii_gz
      elif os.path.isfile(jroi_data_nii):
        jroi_data_fname = jroi_data_nii
      else:
        print 'error: cannot find ' + jroi_data
        sys.exit(1)
      jroi_img = nib.load(jroi_data_fname)
      jroi_img_data = jroi_img.get_data()
      jroi_img_data_nonzero = np.nonzero(jroi_img_data)

      isubj_in_jroi_2D = np.zeros((len(jroi_img_data_nonzero[0]), isubj_img_data.shape[3]))
      isubj_in_jroi_nanmean = np.zeros((isubj_img_data.shape[3],1))
      isubj_in_jroi_Eigen1Variate = np.zeros(isubj_in_jroi_nanmean.shape)
      for k in range(isubj_img_data.shape[3]):
        isubj_img_data_in_k_vol = isubj_img_data[:,:,:,k]
        isubj_in_jroi_2D[:,k] = isubj_img_data_in_k_vol[jroi_img_data_nonzero]
        isubj_in_jroi_nanmean[k] = np.nanmean(isubj_img_data_in_k_vol[jroi_img_data_nonzero])
      isubj_in_jroi_Eigen1Variate = get1stEigenTS(isubj_in_jroi_2D.T)
      ############################
      # data plotting script for testing purpose
      # print isubj_in_jroi_nanmean[0]
      # plt.plot(isubj_in_jroi_nanmean)
      # plt.show()
      # sys.exit(1)
      ############################

      ts_nanmean_orig.append(isubj_in_jroi_nanmean)
      ts_eigen1_orig.append(isubj_in_jroi_Eigen1Variate)

    spio.savemat(ioutputFname, mdict={'ts_nanmean_orig':ts_nanmean_orig, 'ts_eigen1_orig':ts_eigen1_orig,'subject_id': isubj, 'roi_name':roiList})

def ExtractNiiROITsFromfMRIMultiSess(subjectList, sessionList, sessDataList, roiList, roiDataList, outputPath, outputPostfix):
  """
  This module extracts ROI mean time series from 4D fMRI data
  each subject has multiple sessions
  ROIs are nii files
  """
  if not os.path.exists(outputPath):
    os.mkdir(outputPath)
  
  for i in range(len(subjectList)):
    isubj = subjectList[i]
    ises = sessionList[i]
    isubj_data = sessDataList[i]
    print isubj
    print ises
    isubj_data_nii = isubj_data + '.nii'
    isubj_data_nii_gz = isubj_data_nii + '.gz'
    if os.path.isfile(isubj_data_nii_gz):
      isubj_data_fname = isubj_data_nii_gz
    elif os.path.isfile(isubj_data_nii):
      isubj_data_fname = isubj_data_nii
    else:
      print 'error: cannot find ' + isubj_data
      sys.exit(1)
    isubj_img = nib.load(isubj_data_fname)
    isubj_img_data = isubj_img.get_data()

    ts_nanmean_orig = [] # create empty list for time series output
    ts_eigen1_orig = []

    ioutputFname = outputPath + '/' + isubj + '_' + ises + '_' + outputPostfix + '.mat' # output file

    for j in range(len(roiList)):
      jroi = roiList[j]
      print('extracting ' + jroi)
      jroi_data = roiDataList[j]
      if jroi_data[-4:] == '.nii':
        jroi_data_nii = jroi_data
        jroi_data_nii_gz = jroi_data_nii + '.gz'
      elif jroi_data[-7:] == '.nii.gz':
        jroi_data_nii_gz = jroi_data
        jroi_data_nii = jroi_data[:-3]
      else:
        jroi_data_nii = jroi_data + '.nii'
        jroi_data_nii_gz = jroi_data_nii + '.gz'
      if os.path.isfile(jroi_data_nii_gz):
        jroi_data_fname = jroi_data_nii_gz
      elif os.path.isfile(jroi_data_nii):
        jroi_data_fname = jroi_data_nii
      else:
        print 'error: cannot find ' + jroi_data
        sys.exit(1)
      jroi_img = nib.load(jroi_data_fname)
      jroi_img_data = jroi_img.get_data()
      jroi_img_data_nonzero = np.nonzero(jroi_img_data)

      isubj_in_jroi_2D = np.zeros((len(jroi_img_data_nonzero[0]), isubj_img_data.shape[3]))
      isubj_in_jroi_nanmean = np.zeros((isubj_img_data.shape[3],1))
      isubj_in_jroi_Eigen1Variate = np.zeros(isubj_in_jroi_nanmean.shape)
      for k in range(isubj_img_data.shape[3]):
        isubj_img_data_in_k_vol = isubj_img_data[:,:,:,k]
        isubj_in_jroi_2D[:,k] = isubj_img_data_in_k_vol[jroi_img_data_nonzero]
        isubj_in_jroi_nanmean[k] = np.nanmean(isubj_img_data_in_k_vol[jroi_img_data_nonzero])
      isubj_in_jroi_Eigen1Variate = get1stEigenTS(isubj_in_jroi_2D.T)
      ############################
      # data plotting script for testing purpose
      # print isubj_in_jroi_nanmean[0]
      # plt.plot(isubj_in_jroi_nanmean)
      # plt.show()
      # sys.exit(1)
      ############################

      ts_nanmean_orig.append(isubj_in_jroi_nanmean)
      ts_eigen1_orig.append(isubj_in_jroi_Eigen1Variate)

    spio.savemat(ioutputFname, mdict={'ts_nanmean_orig':ts_nanmean_orig, 'ts_eigen1_orig':ts_eigen1_orig,'subject_id': isubj, 'roi_name':roiList})

def ExtractROIValueFromMRI(dataFname, roiFname):
  """
  This module extracts ROI mean from 3D MRI data
  ROIs are nii or img files
  """
 
  roi_img = nib.load(roiFname)
  roi_img_data = roi_img.get_data()
  roi_img_idx = np.nonzero(roi_img_data)

  data_img = nib.load(dataFname)
  data_img_data = data_img.get_data()
  data_img_roi_mean = np.nanmean(data_img_data[roi_img_idx])
  
  return data_img_roi_mean 

def ExtractNumberLabeledROIValueFromMRI(dataFname, roiFname):
  """
  This module extracts number labeled ROI means from 3D MRI data
  Each ROI file containing multiple integer values for different regions
  """
 
  roi_img = nib.load(roiFname)
  roi_img_data = roi_img.get_data()
  roi_labels = np.unique(roi_img_data)
  roi_labels_nonzero = np.trim_zeros(roi_labels)
  
  data_img = nib.load(dataFname)
  data_img_data = data_img.get_data()
  
  data_img_rois_mean = np.zeros((len(roi_labels_nonzero), 1))

  for i in range(len(roi_labels_nonzero)):
    iroi_label = roi_labels_nonzero[i]
    iroi_img_idx = np.where(roi_img_data==iroi_label)
    data_img_rois_mean[i] = np.nanmean(data_img_data[iroi_img_idx])
  
  return data_img_rois_mean 
