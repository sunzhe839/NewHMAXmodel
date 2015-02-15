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
FEATURES = 8  # Number of features
TRAINING_IMAGES_FOLDER_NAME = "training_image"
FEATURES_FOLDER_NAME = "training_data"
CLASSIFIER_FOLDER_NAME = "classifier_data"
CLASSIFIER_FILE_NAME = "test_classifier"
IMAGES_FOLDER_NAME = "base_image"
TEMPORARY_FOLDER = "temp_folder"

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
        NormalS2 = NormalIntermediateFeature(PROTOTYPE_SIZE, INPUT_SIZE, C1_SCALES, FEATURES, ORIENTATIONS,
                                             FEATURES_FOLDER_NAME, mode)
        C2 = GlobalInvariance(ORIENTATIONS)
        NormalSVM = PredictionSVM(CLASSIFIER_FOLDER_NAME, CLASSIFIER_FILE_NAME)

        # make layer
        #print 'Input Layer'
        InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 0, 0, 0)
        InputLayer.set_image(image)
        #print '\nS1 Layer'
        s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 0, 11, InputLayer)
        #print "\nC1 Layer"
        c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 0, 10, s1Layer)
        #print "\nS2 Layer"
        ns2Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "normal_s2", FEATURES, PROTOTYPE_SIZE, c1Layer)
        #print "\nC2 Layer"
        c2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "c2", FEATURES, 0, ns2Layer)

        S1.compute_layer(InputLayer, s1Layer)
        C1.compute_layer(s1Layer, c1Layer)
        NormalS2.compute_s2(c1Layer, ns2Layer)
        C2.compute_layer(ns2Layer, c2Layer)

        vector = []
        for s in range(C1_SCALES):
            #features = c2Layer.get_features(s)
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
        NormalS2 = NormalIntermediateFeature(PROTOTYPE_SIZE, INPUT_SIZE, C1_SCALES, FEATURES, ORIENTATIONS,
                                             FEATURES_FOLDER_NAME, mode)
        C2 = GlobalInvariance(ORIENTATIONS)
        LearningSVM = TrainingSVM(CLASSIFIER_FOLDER_NAME, CLASSIFIER_FILE_NAME)

        print "training feature..."

        class_number = 1
        exi1 = path.isdir(TRAINING_IMAGES_FOLDER_NAME + "/" + str(class_number))
        while exi1:
            data_number = 1
            exi2 = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(class_number) + "/" + str(data_number) + ".jpg")
            while exi2:
                filename = str(class_number) + "_" + str(data_number) + "_" + str(INPUT_SIZE)
                exi = path.isdir(FEATURES_FOLDER_NAME + "/" + filename)
                if not exi:
                    image = Image.open(TRAINING_IMAGES_FOLDER_NAME + "/" + str(class_number) + "/" +
                                       str(data_number) + ".jpg")

                    #print 'Input Layer'
                    InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 1, 0, 0)
                    InputLayer.set_image(image)
                    #print '\nS1 Layer'
                    s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 1, 11, InputLayer)
                    #print "\nC1 Layer"
                    c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 1, 10, s1Layer)
                    #print "\nS2 Layer"
                    ls2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "learning_s2", FEATURES,
                                     PROTOTYPE_SIZE, c1Layer)

                    S1.compute_layer(InputLayer, s1Layer)
                    s1Layer.save_layer(TEMPORARY_FOLDER, filename)
                    C1.compute_layer(s1Layer, c1Layer)
                    c1Layer.save_layer(TEMPORARY_FOLDER, filename)
                    LearningS2.compute_s2(c1Layer, ls2Layer, filename)

                print "\nfinished image " + str(class_number) + "_" + str(data_number) + "\n"

                data_number += 1
                exi2 = path.isfile(TRAINING_IMAGES_FOLDER_NAME + "/" + str(class_number) + "/"
                                   + str(data_number) + ".jpg")
            class_number += 1
            exi1 = path.isdir(TRAINING_IMAGES_FOLDER_NAME + "/" + str(class_number))

        print "finished training feature"
        print "making classifier..."

        training_vector = []
        training_label = []
        label = np.genfromtxt(TRAINING_IMAGES_FOLDER_NAME + "/label.txt", comments='#', dtype='str')

        class_number = 1
        data_number = 1
        exi1 = path.isdir(TEMPORARY_FOLDER + "/" + str(class_number) + "_" + str(data_number) + "_" + str(INPUT_SIZE))
        while exi1:
            exi2 = path.isdir(TEMPORARY_FOLDER + "/" + str(class_number) + "_" + str(data_number) +
                              "_" + str(INPUT_SIZE))
            while exi2:
                #print 'Input Layer'
                InputLayer = Layer(INPUT_SIZE, SCALES, 1, "Input", 1, 0, 0)
                #print '\nS1 Layer'
                s1Layer = Layer(INPUT_SIZE, SCALES, ORIENTATIONS, "s1", 1, 11, InputLayer)
                #print "\nC1 Layer"
                c1Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "c1", 0, 10, s1Layer)
                #print "\nS2 Layer"
                ns2Layer = Layer(INPUT_SIZE, C1_SCALES, ORIENTATIONS, "normal_s2", FEATURES, PROTOTYPE_SIZE, c1Layer)
                #print "\nC2 Layer"
                c2Layer = Layer(PROTOTYPE_SIZE, C1_SCALES, ORIENTATIONS, "c2", FEATURES, 0, ns2Layer)

                c1Layer.set_layer(TEMPORARY_FOLDER, str(class_number) + "_" + str(data_number) + "_" + str(INPUT_SIZE))
                NormalS2.compute_s2(c1Layer, ns2Layer)
                C2.compute_layer(ns2Layer, c2Layer)

                vector = []
                for s in range(C1_SCALES):
                    #features = c2Layer.get_features(s)
                    for o in range(ORIENTATIONS):
                        vector.extend(c2Layer.get_array(s)[:, 0, 0, o])
                training_vector.append(vector)
                training_label.append(label[class_number - 1])

                print "\nfinished image " + str(class_number) + "_" + str(data_number) + "\n"

                data_number += 1
                exi2 = path.isdir(TEMPORARY_FOLDER + "/" + str(class_number) + "_" + str(data_number) +
                                  "_" + str(INPUT_SIZE))
            data_number = 1
            class_number += 1
            exi1 = path.isdir(TEMPORARY_FOLDER + "/" + str(class_number) + "_" + str(data_number) +
                              "_" + str(INPUT_SIZE))

        LearningSVM.training_feature(training_vector, training_label)

        print "finished making classifier"

        print "\n", time.time() - start
