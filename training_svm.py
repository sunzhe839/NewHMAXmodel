__author__ = 'yuki'
#coding UTF-8

from sklearn.svm import LinearSVC
from sklearn.externals import joblib


class TrainingSVM(object):
    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name
        self.clf = LinearSVC(C=1.0)

    def training_feature(self, data_training, label_training):
        self.clf.fit(data_training, label_training)

        joblib.dump(self.clf, self.folder_name + "/" + self.file_name + ".pkl")
