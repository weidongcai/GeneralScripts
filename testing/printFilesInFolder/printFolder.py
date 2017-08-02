#!/usr/bin/python -tt

import os
import sys

sys.path.append('/home/wdcai/Library/Python/CommonModule')
from SysModule import ListAllFilesInFolder

def main():
  args = sys.argv[1:]
  if not args:
    print 'error: no folder was given'
    sys.exit(1)
  else:
    folderName = sys.argv[1]
    fileList = ListAllFilesInFolder(folderName)
    for ifile in fileList:
      print ifile

if __name__ == '__main__':
  main()
