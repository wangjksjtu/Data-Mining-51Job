from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import Perceptron
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import metrics
from provider import job_provider
from sklearn import cross_validation
from sklearn.multiclass import OneVsRestClassifier
import time

def train():
    X_train, X_test, Y_train, Y_test = job_provider()
    svm = SVC()
    perceptron = Perceptron()
    gnb = GaussianNB()
    knn = KNeighborsClassifier()
    rf = RandomForestClassifier()
    xg = XGBClassifier()
    mlp = MLPClassifier()

    classifiers =  [svm, perceptron, gnb, knn, rf, xg, mlp]
    classifier_names = ["SVM", "LP", "GNB", "KNN", "RF", "XGB", "MLP"]
    for classifier, classifier_name in zip(classifiers, classifier_names):

        print "-----------------------------------"
        print classifier
        intime = time.time()
        classifier.fit(X_train, Y_train)
        Y_pred = classifier.predict(X_test)
        print time.time() - intime
        print "Accuracy for ", classifier_name, " : ", metrics.accuracy_score(Y_test, Y_pred)
        print "-----------------------------------\n"
            
if __name__ == "__main__":
    train()