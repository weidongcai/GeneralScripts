#!/home/wdcai/anaconda3/bin/python3.5 -tt

import nibabel as nib
import sys
import os
import os.path
import numpy as np
import scipy as sp
import scipy.ndimage
import scipy.signal as spsi
import csv
import nilearn
import nilearn.image

sys.path.append('/home/wdcai/Library/Python/ModulesFromColleagues')
from filtutils import get_filt_coeffs

def BPFilter(X,TR,fl,fh):
  '''
  X is a nxk matrix, n is number of sample, k is number of variables
  '''
  fs = 1/TR
  fc = 0.5*(fh+fl)
  order = int(np.floor(fs*2/fc))
  b = get_filt_coeffs(np.zeros((1,X.shape[0])),fs,fl,fh,filtorder=order)
  a = 1
  filterX = spsi.filtfilt(b,a,X,axis=0)
  return filterX

def Smoothing(inputfilename, fwhm, outputfilename):
### smoothing script from JK ###
  img_file = inputfilename
  img = nib.load(img_file)
  print('Done: load ' + inputfilename)
  zooms = np.array(img.header.get_zooms())
  kernel_width = fwhm
  kernel_sigma = (kernel_width/zooms[:3])/(2 * np.sqrt(2*np.log(2)))
  kernel_sigma = tuple(kernel_sigma) + (0,) # don't smooth over time dim

  #data = np.asarray(img.dataobj) #proxy object to avoid caching (this is for stricter memory management on Sherlock)
  data = img.get_data() # this is fine for our servers
  print('Done: set smooth kernel')
  data = sp.ndimage.filters.gaussian_filter(data, sigma=kernel_sigma, mode='constant', cval=0.)
  print('Done: smoothing')
  nib.save(img, outputfilename)

def SmoothingNilearn(inputfilename, fwhm, outputfilename):
### use smoothing function from nilearn ###
  img = nib.load(inputfilename)
  print('Done: load ' + inputfilename)
  img_smooth = nilearn.image.smooth_img(img, fwhm)
  img_smooth.to_filename(outputfilename)
