__author__ = 'yuki'
#coding UTF-8

import numpy as np
from MFilter import Filter

class LocalInvariance(Filter):
    def __init__(self, xyCount, oCount):
        self.xyCount = xyCount #size of filter
        self.oCount = oCount #number of orientation

    def ComputeUnit(self, Input_p1, Input_p2):
        return max(np.max(Input_p1), np.max(Input_p2))
