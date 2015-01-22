__author__ = 'yuki'
#coding UTF-8

import numpy as np
import os.path as path
from PIL import Image
from layer import Layer
from gabor_filter import GaborFilter
from local_invariance import LocalInvariance
from learning_intermediate_feature import LearningIntermediateFeature
from normal_intermediate_feature import NormalIntermediateFeature
from global_invariance import GlobalInvariance
from training_svm import TrainingSVM
from prediction_svm import PredictionSVM
import time

INPUT_SIZE = 256  # Input image size
SCALES = 12  # Number of scales at InputLayer
C1_SCALES = SCALES - 1  # Number of scales at c1
ORIENTATIONS = 4  # Number of orientations
PROTOTYPE_SIZE = 4  # Prototype patch size
FEATURES = 20  # Number of features at largest scale
TRAINING_IMAGES_FOLDER_NAME = "training_image"
FEATURES_FOLDER_NAME = "training_data"
CLASSIFIER_FOLDER_NAME = "classifier_data"
CLASSIFIER_FILE_NAME = "test_classifier"
IMAGES_FOLDER_NAME = "base_image"

if __name__ == "__main__":
    print "Mode(\"l\" = learning mode, \"n\" = normal mode):"
    mode = raw_input()
    if mode == "n":
        print "Input file name:"
        input_image_name = raw_input()

        start = time.time()

        image = Image.open(IMAGES_FOLDER_NAME + "/" + input_image_name + ".jpg")

        S1 = GaborFilter(11, 0.3, 4.0, 1.0, ORIENTATIONS)
        C1 = LocalInvariance(10, ORIENTATIONS)
        NormalS2 = NormalIntermediateFeature(PROTOTYPE_SIZE, ORIENTATIONS, FEATURES_FOLDER_NAME)
        C2 = GlobalInvariance(ORIENTATIONS)
        NormalSVM = PredictionSVM(CLASSIFIER_FOLDER_NAME, CLASSIFIER_FILE_NAME)

        # make layer
        print 'Input Layer'
        InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 0)
        InputLayer.set_layer(image)
        print '\nS1 Layer'
        s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 0)
        print "\nC1 Layer"
        c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 0)
        print "\nS2 Layer"
        ns2Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "normal_s2", FEATURES)
        print "\nC2 Layer"
        c2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "c2", FEATURES)

        S1.compute_layer(InputLayer, s1Layer)
        C1.compute_layer(s1Layer, c1Layer)
        NormalS2.compute_s2(c1Layer, ns2Layer)
        C2.compute_layer(ns2Layer, c2Layer)

        vector = []
        for s in range(C1_SCALES):
            features = c2Layer.get_features(s)
            for o in range(ORIENTATIONS):
                vector.extend(c2Layer.get_array(s)[:, 0, 0, o])

        print "\n"
        NormalSVM.predict_class(vector)

        print "\n", time.time() - start

    elif mode == "l":
        start = time.time()

        S1 = GaborFilter(11, 0.3, 4.0, 1.0, ORIENTATIONS)
        C1 = LocalInvariance(10, ORIENTATIONS)
        LearningS2 = LearningIntermediateFeature(PROTOTYPE_SIZE, ORIENTATIONS, FEATURES_FOLDER_NAME)
        NormalS2 = NormalIntermediateFeature(PROTOTYPE_SIZE, ORIENTATIONS, FEATURES_FOLDER_NAME)
        C2 = GlobalInvariance(ORIENTATIONS)
        LearningSVM = TrainingSVM(CLASSIFIER_FOLDER_NAME, CLASSIFIER_FILE_NAME)

        print "training feature..."

        data_number = 1
        exi = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")
        while exi:
            image = Image.open(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")

            print 'Input Layer'
            InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 1)
            InputLayer.set_layer(image)
            print '\nS1 Layer'
            s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 1)
            print "\nC1 Layer"
            c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 1)
            print "\nS2 Layer"
            ls2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "learning_s2", FEATURES)

            S1.compute_layer(InputLayer, s1Layer)
            C1.compute_layer(s1Layer, c1Layer)
            LearningS2.compute_s2(c1Layer, ls2Layer, data_number)

            print "\nfinished image", data_number, "\n"

            data_number += 1
            exi = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")

        print "finished training feature"
        print "making classifier..."

        training_vector = []
        training_label = np.genfromtxt(TRAINING_IMAGES_FOLDER_NAME + "/label.txt", comments='#', dtype='str')

        data_number = 1
        exi = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")
        while exi:
            image = Image.open(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")

            print 'Input Layer'
            InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 0)
            InputLayer.set_layer(image)
            print '\nS1 Layer'
            s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 0)
            print "\nC1 Layer"
            c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 0)
            print "\nS2 Layer"
            ns2Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "normal_s2", FEATURES)
            print "\nC2 Layer"
            c2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "c2", FEATURES)

            S1.compute_layer(InputLayer, s1Layer)
            C1.compute_layer(s1Layer, c1Layer)
            NormalS2.compute_s2(c1Layer, ns2Layer)
            C2.compute_layer(ns2Layer, c2Layer)

            vector = []
            for s in range(C1_SCALES):
                features = c2Layer.get_features(s)
                for o in range(ORIENTATIONS):
                    vector.extend(c2Layer.get_array(s)[:, 0, 0, o])
            training_vector.append(vector)

            print "\nfinished image", data_number, "\n"

            data_number += 1
            exi = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(data_number) + ".jpg")

        LearningSVM.training_feature(training_vector, training_label)

        print "finished making classifier"

        print "\n", time.time() - start
