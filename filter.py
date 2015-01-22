__author__ = 'yuki'
#coding UTF-8


class Filter(object):
    def __init__(self):
        pass

    def compute_layer(self, input_layer, output_layer):
        scales = output_layer.get_scales()
        layer_type = output_layer.get_layer_type()
        step = output_layer.get_step()
        if layer_type != "normal_s2":
            print "\n", layer_type
        for s in range(scales):
            print "Computing scale", s, "..."
            output_unit = output_layer.get_array(s)
            features = output_layer.get_features(s)
            size = input_layer.get_size(s)
            for f in range(features):
                for o in range(self.orientations):
                    o_x = 0
                    for x in range(0, size - self.filter_size + 1, step):
                        o_y = 0
                        for y in range(0, size - self.filter_size + 1, step):
                            output_unit[f, o_x, o_y, o] = self.compute_unit(input_layer, s, f, x, y, o)
                            o_y += 1
                        o_x += 1
