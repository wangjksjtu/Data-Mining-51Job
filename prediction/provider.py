# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from sklearn.naive_bayes import GaussianNB

def salary_provider(preprocessing="None"):
    X_train, X_test, Y_train, Y_test = provider(is_regression=True)

    # Normalize the label [No sense!!]
    # salary_max, salary_min = np.max(Y_train), np.min(Y_train)
    # Y_train = (Y_train - salary_min) / float(salary_max - salary_min)
    # Y_test = (Y_test - salary_min) / float(salary_max - salary_min)
    if preprocessing == "normalize":
        normalizer = Normalizer()
        X_train = normalizer.fit_transform(X_train)
        X_test = normalizer.fit_transform(X_test)
    elif preprocessing == "minmax":
        minmaxscaler = MinMaxScaler()
        X_train = minmaxscaler.fit_transform(X_train)
        X_test = minmaxscaler.fit_transform(X_test)
    elif preprocessing == "standard":
        standardscale = StandardScaler()
        X_train = standardscale.fit_transform(X_train)
        X_test = standardscale.fit_transform(X_test)
    else:
        pass

    print Y_test
    print Y_train
    return X_train, X_test, Y_train, Y_test


def job_provider(preprocessing="None"):
    X_train, X_test, Y_train, Y_test = provider(is_regression=True)
    print (X_train.shape, Y_train.shape)

    if preprocessing == "normalize":
        normalizer = Normalizer()
        X_train = normalizer.fit_transform(X_train)
        X_test = normalizer.fit_transform(X_test)
    elif preprocessing == "minmax":
        minmaxscaler = MinMaxScaler()
        X_train = minmaxscaler.fit_transform(X_train)
        X_test = minmaxscaler.fit_transform(X_test)
    elif preprocessing == "standard":
        standardscale = StandardScaler()
        X_train = standardscale.fit_transform(X_train)
        X_test = standardscale.fit_transform(X_test)
    else:
        pass

    return X_train, X_test, Y_train, Y_test
    

def provider(filepath="../data/data.csv", 
             is_regression=False,
             salary_pred="high",
             all_data=False):
    # read data from the csv file 
    df =  pd.read_csv(filepath, header=0, encoding="gb2312")
    # print df.head(5)

    # preprocess the data [city, language, company, job, welfare]
    df_city = df.apply(lambda s: np.argmax(list(s[6:27])), axis=1)
    df_lan = df.apply(lambda s: np.argmax(list(s[174: 181])), axis=1)
    df_com = df.apply(lambda s: np.argmax(list(s[94: 104])), axis=1)
    df_job = df.apply(lambda s: np.argmax(list(s[241: 273])), axis=1)
    df_welfare = df.apply(lambda s: np.sum(list(s[104: 174])), axis=1)

    # merge the properties
    if is_regression:
        data = df.iloc[:,:4]
        if salary_pred == "high":
            labels = df.iloc[:,4]
        elif salary_pred == "low":
            labels = df.iloc[:,5]
        else:
            labels = df.iloc[:,4:6]
    else:
        data = df.iloc[:,:6]
    # print data.head(5)
    # print labels.head(5)

    data['city'] = df_city.values
    data['language'] = df_lan.values
    data['company'] = df_com.values
    if is_regression:
        data['job'] = df_job.values
    else:
        labels = df_job.values
    data['welfare'] = df_welfare.values
    print data.head(2)

    # split the data
    X_train, X_test, Y_train, Y_test = train_test_split(data.values, labels.values, test_size=0.2, random_state=42)
    print X_train.shape, X_test.shape
    print Y_train.shape, Y_test.shape
    if all_data:
        return data.values, labels.values
    return X_train, X_test, Y_train, Y_test


if __name__ == "__main__":
    X_train, X_test, Y_train, Y_test = salary_provider()
    # regression(X_train, X_test, Y_train, Y_test)