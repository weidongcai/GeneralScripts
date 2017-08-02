#!/home/wdcai/anaconda3/bin/python3.5

import sys
import numpy as np
import numpy.matlib

sys.path.append('/home/wdcai/Library/Python3.5/CommonModule')
from StatsModule import princomp

A = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
[coef,score,latent] = princomp(A)
print(coef)
print(score)
print(latent)
