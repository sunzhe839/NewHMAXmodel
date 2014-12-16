__author__ = 'yuki'
#coding UTF-8

import numpy as np
from MFilter import Filter

class IntermediateFeature(Filter):
    def __init__(self, xyCount, oCount, mode):
        self.xyCount = xyCount #size of filter
        self.oCount = oCount #number of orientation
        self.mode = mode

    def ComputeS2(self, input, output):
        if self.mode == "learning":
            self.ComputeLayer()
            scale = output.get_scale()
            save_data = []
            for s in range(scale):
                save_data.append(output.get_array(s))
            #ファイルの有無を調べる
            data_number = ""
            np.savez('training_data/' + data_number, x = save_data)

        elif self.mode == "normal":
            #ファイルの有無を調べる
            data_number = ""
            self.prototype = np.load('training_data/' + data_number)
            self.ComputeLayer()


    def ConputeUnit(self, input, scale, x, y, orientation):
        patch = input.get_array(scale)[x:x + self.xyCount, y:y + self.xyCount, orientation]
        if self.mode == "learning":
            return patch
        elif self.mode == "normal":
            p_patch = self.prototype
            alpha = (self.xyCount/4)**2.0
            res = np.exp(-(p_patch - patch) * 1.0 / 2 * alpha)
            return res
