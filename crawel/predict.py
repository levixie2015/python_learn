# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

def load_historydata():
    if not os.path.isfile(os.getcwd()+"ssq.pkl"):
        ori_data = np.loadtxt('data2.csv', skiprows=1,delimiter=',',usecols=(0,1,2, 3, 4, 5, 6), unpack=False)
        pickle.dump(ori_data, open("ssq.pkl", "wb"))
        return ori_data
    else:
        ori_data = pickle.load(open("ssq.pkl", "rb"))
        return ori_data

def load_tsnedata(ori_data):
    if not os.path.isfile(os.getcwd()+"ssq_tsne.pkl"):
        tsne = TSNE(n_components=3, random_state=0)
        tsne_data = tsne.fit_transform(ori_data)
        pickle.dump(tsne_data, open("ssq_tsne.pkl", "wb"))
        return tsne_data
    else:
        tsne_data = pickle.load(open("ssq_tsne.pkl", "rb"))
        return tsne_data

def show_oridata(show_date):
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(show_date[:, 0], show_date[:, 1], show_date[:, 2], edgecolor='k', s=40)
    plt.show()

if __name__ == '__main__':
    ori_data = load_historydata()
    np.random.shuffle(ori_data)
    tsne_data = load_tsnedata(ori_data)
    show_oridata(tsne_data)

    X_data = ori_data[:, 0].reshape(-1, 1)
    Y_data = ori_data[:, 1:]
    print("X_data[0]: ", X_data[0])
    print("Y_data[0]: ", Y_data[0])

    # Split the data into training/testing sets
    split_len = int(len(X_data) * 0.8)
    X_train = X_data[:split_len]
    X_test = X_data[split_len:]
    print("X_train")
    print(X_train)

    # Split the targets into training/testing sets
    y_train = Y_data[:split_len]
    y_test = Y_data[split_len:]
    print("y_train")
    print(y_train)

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(X_train, y_train)

    # Make predictions using the testing set
    #y_pred = regr.predict(X_train).round()
    y_pred = regr.predict(X_test).round()
    print("y_pred")
    print(y_pred)

    print("y_pred distinct")
    y_pred_cache = list()
    for line in y_pred:
        line = list(line)
        if line not in y_pred_cache:
            y_pred_cache.append(line)
    for line in y_pred_cache:
        print(line)

    # 预测的准确度
    print("Prediction accurate: {0}%".format(np.mean(X_test==y_pred) * 100))