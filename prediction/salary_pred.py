from provider import salary_provider
import time

from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import ElasticNet
from sklearn.neural_network import MLPRegressor
from sklearn import metrics

def train():
    X_train, X_test, Y_train, Y_test = salary_provider()
    ada = AdaBoostRegressor()
    rf = RandomForestRegressor()
    bagging = BaggingRegressor()
    grad = GradientBoostingRegressor()
    svr = SVR()
    bayes_ridge = BayesianRidge()
    elastic_net = ElasticNet()
    mlp = MLPRegressor(hidden_layer_sizes=(64, 128, 64), max_iter=1000)

    regressors = [ada, rf, bagging, grad, svr, bayes_ridge, elastic_net, mlp]
    regressor_names = ["AdaBoost", "Random Forest", "Bagging",
                       "Gradient Boost", "SVR", "Bayesian Ridge",
                       "Elastic Net", "MLPRegressor"]

    #regressors = [mlp]
    #regressor_names = ["MLP"]

    for regressor, regressor_name in zip(regressors, regressor_names):
        intime = time.time()
        regressor.fit(X_train, Y_train)
        Y_pred = regressor.predict(X_test)        
        print X_train.shape, Y_train.shape
        print "-----------------------------------"
        print time.time() - intime
        print "For Regressor : ", regressor_name
        print "Mean Absolute Error : ", metrics.mean_absolute_error(Y_test, Y_pred)
        # print "Median Absolute Error : ",metrics.median_absolute_error(Y_test, Y_pred)
        # print "Mean Squared Error : ",metrics.mean_squared_error(Y_test, Y_pred)
        print "R2 Score : ", metrics.r2_score(Y_test, Y_pred)
        print "---------------------------------\n"

        for i in range(5):
            print Y_pred[i], Y_test[i], X_test[i]

if __name__ == "__main__":
    train()