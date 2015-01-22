__author__ = 'yuki'
#coding UTF-8

import numpy as np


class GlobalInvariance(object):
    def __init__(self, orientations):
        self.orientations = orientations

    def compute_unit(self, input_layer, scale, feature, orientation):
        patch = input_layer.get_array(scale)[feature, :, :, orientation]
        return np.max(patch)

    def compute_layer(self, input_layer, output_layer):
        scales = output_layer.get_scales()
        layer_type = output_layer.get_layer_type()
        print "\n", layer_type
        for s in range(scales):
            print "Computing scale", s, "..."
            output_layer_unit = output_layer.get_array(s)
            features = output_layer.get_features(s)
            for f in range(features):
                for o in range(self.orientations):
                    output_layer_unit[f, 0, 0, o] = self.compute_unit(input_layer, s, f, o)
