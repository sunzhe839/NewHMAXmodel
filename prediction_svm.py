__author__ = 'yuki'
#coding UTF-8

from sklearn.externals import joblib


class PredictionSVM(object):
    def __init__(self, folder_name, file_name):
        self.folder_name = folder_name
        self.file_name = file_name

    def predict_class(self, data):
        clf = joblib.load(self.folder_name + "/" + self.file_name + ".pkl")

        print clf.predict(data)
