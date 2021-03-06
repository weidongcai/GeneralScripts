#!/usr/bin/python -tt

import sys
import os
import os.path
import numpy as np
import csv

def ReadListFile(filename):
  try:
    f = open(filename, 'rU')
    if f:
      istrs = f.read()
      f.close()
      outputList = istrs.split()
      return outputList
  except Exception, e:
    print str(e)

def ReadCSVFile(filename,header):
  output_list = []
  try:
    f = open(filename, 'rt')
    reader = csv.reader(f)
    if header:
      header = reader.next()
    for row in reader:
      output_list.append(row)
    f.close()
    return output_list
  except Exception, e:
    print str(e)

def WriteList2File(inputList,filename):
  try:
    f = open(filename, 'w')
    if f:
      for iinput in inputList:
        istr = iinput + '\n'
        f.write(istr)
      f.close() 
  except Exception, e:
    print str(e)

def WriteListOfList2File(List,filename):
  try:
    f = open(filename, 'w')
    if f:
      for ilist in List:
        new_ilist = ",".join([str(x) for x in ilist])
        f.write(new_ilist)
        f.write(str('\n'))
      f.close() 
  except Exception, e:
    print str(e)

def MovScreen(List):
  tran_thr = 3
  rot_thr = 3
  s2s_thr = 0.25
  if (float(List[2])<tran_thr) & (float(List[3])<tran_thr) & (float(List[4])<tran_thr) & (float(List[5])<rot_thr) & (float(List[6])<rot_thr) & (float(List[7])<rot_thr) & (float(List[10])<s2s_thr):
    passflg = 1
  else:
    passflg = 0
  return passflg

def FindFilesWithExtension(path, ext):
  outputList = [f for f in os.listdir(path) if f.endswith(ext)]
  return outputList
