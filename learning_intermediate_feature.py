__author__ = 'yuki'
#coding UTF-8

import numpy as np
import os.path as path


class LearningIntermediateFeature(object):
    def __init__(self, filter_size, orientations, filename):
        self.filter_size = filter_size  # size of patch
        self.orientations = orientations  # number of orientation
        self.filename = filename

    def compute_s2(self, input_layer, output_layer, data_number):
        self.compute_layer(input_layer, output_layer)
        scales = output_layer.get_scales()
        save_data = []
        for s in range(scales):
            save_data.append(output_layer.get_array(s))
        np.savez(self.filename + "/" + str(data_number), save_data)

    def compute_layer(self, input_layer, output_layer):
        scales = output_layer.get_scales()
        layer_type = output_layer.get_layer_type()
        print "\n", layer_type
        for s in range(scales):
            print "Computing scale", s, "..."
            output_unit = output_layer.get_array(s)
            features = output_layer.get_features(s)
            size = input_layer.get_size(s)
            for f in range(features):
                x = np.random.randint(size - self.filter_size + 1)
                y = np.random.randint(size - self.filter_size + 1)
                for o in range(self.orientations):
                    for nx in range(self.filter_size):
                        for ny in range(self.filter_size):
                            output_unit[f, nx, ny, o] = input_layer.get_array(s)[0, x + nx, y + nx, o]
