#!/home/wdcai/anaconda3/bin/python3.5 -tt

import sys
import os
import os.path
import numpy as np
import csv

def ElementOfListAInListB(listA, listB):
  listAInListB = []
  for i in range(len(listA)):
    if (listA[i] in listB):
      listAInListB.append(listA[i])
  return listAInListB

def ElementOfListANotInListB(listA, listB):
  listANotInListB = []
  for i in range(len(listA)):
    if not(listA[i] in listB):
      listANotInListB.append(listA[i])
  return listANotInListB

def ReadMovFile(filename):
  movArray = np.loadtxt(filename)
  return movArray

def ReadListFile(filename):
  try:
    f = open(filename, 'rU')
    if f:
      istrs = f.read()
      f.close()
      outputList = istrs.split()
      return outputList
  except ValueError:
    print("cannot open file")

def ReadCSVFileHeader(filename, isHeaderExist):
  output_list = []
  try:
    f = open(filename, 'rt')
    reader = csv.reader(f)
    if isHeaderExist:
      header = next(reader)
      output_list.append(header)
  except ValueError:
    print("cannot open file")
  return output_list[0]

def ReadCSVFileBody(filename, isHeaderExist):
  output_list = []
  try:
    f = open(filename, 'rt')
    reader = csv.reader(f)
    if isHeaderExist:
      next(reader)
    for row in reader:
      output_list.append(row)
    f.close()
    return output_list
  except ValueError:
    print("cannot open file")

def WriteList2File(inputList,filename):
  try:
    f = open(filename, 'w')
    if f:
      for iinput in inputList:
        istr = iinput + '\n'
        f.write(istr)
      f.close() 
  except ValueError:
    print("cannot open file")

def WriteListOfList2File(List,filename):
  try:
    f = open(filename, 'w')
    if f:
      for ilist in List:
        new_ilist = ",".join([str(x) for x in ilist])
        f.write(new_ilist)
        f.write(str('\n'))
      f.close() 
  except ValueError:
    print("cannot open file")

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

def ExtractBehavForSubj(inputSubjectListFname, inputBehavCsv, keyVar, outputFname):
  subjectList = ReadListFile(inputSubjectListFname)
  behavStats = ReadCSVFileBody(inputBehavCsv, 1)
  behavStatsHeader = ReadCSVFileHeader(inputBehavCsv, 1)
  print(keyVar)
  print(behavStatsHeader)
  if keyVar in behavStatsHeader:
    keyVarIdx = behavStatsHeader.index(keyVar)
  else:
    print('error: cannot find variable of interest')
    sys.exit(0)
  subjectListFromBehav = []
  for iBeh in behavStats:
    subjectListFromBehav.append(iBeh[0])
  outputList = []
  for isubj in subjectList:
    isubj_idx = subjectListFromBehav.index(isubj)
    isubj_beh = behavStats[isubj_idx]
    outputList.append(isubj_beh[keyVarIdx])
    print(isubj)
    print(isubj_beh[keyVarIdx])
  WriteList2File(outputList, outputFname)  
