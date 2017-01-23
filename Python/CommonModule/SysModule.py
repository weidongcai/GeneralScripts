#!/user/bin/python -tt

import sys
import os

def ListAllFilesInFolder(folder):
  fileList = []
  for r,d,f in os.walk(folder):
    if not len(f)==0:
      for ifile in f:
        fileList.append(os.path.join(r,ifile))
  return sorted(fileList)
