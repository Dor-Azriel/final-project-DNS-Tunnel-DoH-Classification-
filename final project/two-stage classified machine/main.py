
import pandas as pd
from matplotlib.pyplot import clf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report, roc_curve
from sklearn.feature_selection import VarianceThreshold, mutual_info_classif, SelectKBest
from sklearn.neighbors import KNeighborsClassifier

from scapy.all import *
import pyshark
from tensorflow.keras.layers import Dense   # , Flatten, Conv1D, Dropout
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
import csv
import numpy as np






def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# ------------------------------------------------------------------------------------------------------------



    data = pd.read_csv(r'C:\Users\user\PycharmProjects\pythonFinalProject8\Firefox\all.csv',nrows=20000 )
   # print(data.head(5))
    data1 = pd.read_csv(r'C:\Users\user\PycharmProjects\pythonFinalProject8\Firefox\all.csv')
    data1 = data1[data1["DoH"] == True]
    data = data[data["DoH"] == False]
    data = data.append(data1)
# ________________________________________________________________________________________________________



    # --------------------------------------- data for test and train is ready


    # -----------------------------data doh ndoh is ready


    #print('------------------------------------------')
    x = data.drop(labels=['DoH', 'TimeStamp', 'SourceIP', 'DestinationIP', 'ResponseTimeTimeMedian',
                          'ResponseTimeTimeSkewFromMedian'], axis=1)

    y = data['DoH']



    data = data.drop(['SourceIP', 'DestinationIP', 'PacketTimeMode', 'TimeStamp'], 1)
    data = data.dropna()
    data = data.drop_duplicates()
    data.DoH = LabelEncoder().fit_transform(data.DoH)
    #print(data.head(5))
    #print('------------------------------------------')
    #print(data.groupby(data.DoH).size())

    x = data.drop('DoH', 1)
    y = data.DoH
    #print('------------------------------------------')
    #print(x.head())
    #print(y.head())
    #print('------------------------------------------')

    X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=42)

    mi = mutual_info_classif(X_train, y_train)
    select_feature = SelectKBest(mutual_info_classif, k=19).fit(X_train, y_train)
    X_train = select_feature.transform(X_train)
    X_test = select_feature.transform(X_test)




# --------------------------------------- Level two,data preparation
    data3 = pd.read_csv(r'C:\Users\user\PycharmProjects\pythonFinalProject8\data_2\l2-benign.csv')
    data3.insert(0, "M", 0, allow_duplicates=True)
    data3 = data3
    data4 = pd.read_csv(r'C:\Users\user\PycharmProjects\pythonFinalProject8\data_2\l2-malicious.csv', nrows=15000)

    print(data3.head())
    print(data3.info())
    print('!!!!!!!!!!!!!!!!!!')
    print(data4.head())
    print(data4.info())
    print('!!!!!!!!!!!!!!!!!!')

    data4.insert(0, "M", 1, allow_duplicates=True)

    data5 = pd.concat([data4, data3], ignore_index=True, sort=False)

    print(data5.head())
    print(data5.info())
    data5 = data5.drop(['SourceIP', 'DestinationIP', 'PacketTimeMode', 'TimeStamp', 'Label'], 1)
    data5 = data5.dropna()
    data5 = data5.drop_duplicates()

    # ------------------------------------------- level two, make data for train and test
    x2 = data5

    y2 = data5['M']

    print('#############################################')
    print(data.groupby(data5.M).size())
    data5.M = LabelEncoder().fit_transform(data5.M)

    data5 = data5.drop_duplicates()
    x2 = data5.drop('M', 1)
    y2 = data5.M

    X_train2, X_test2, y_train2, y_test2 = train_test_split(x2, y2, train_size=0.2, random_state=42)

    mi = mutual_info_classif(X_train2, y_train2)

    select_feature = SelectKBest(mutual_info_classif, k=19).fit(X_train2, y_train2)
    X_train2 = select_feature.transform(X_train2)
    X_test2 = select_feature.transform(X_test2)

# --------------------------------------- data  in level two for test and train is ready

    # first level :

    for i in [1, 5, 20]:
        print('#################################################################################')
        knn = KNeighborsClassifier(n_neighbors=i)
        y_pred_KNN = knn.fit(X_train, y_train).predict(X_test)
        print("accuracy_score :", accuracy_score(y_test, y_pred_KNN) * 100)
        print("classification_report:", classification_report(y_test, y_pred_KNN))
    print('')
    print('')
    print('')
    print('first level done  ')
    print('')
    print('')
    print('')

    # second level :

    for i in [1, 5, 20]:
        print('####################################################################################')
        knn2 = KNeighborsClassifier(n_neighbors=i)
        y_pred_KNN = knn2.fit(X_train2, y_train2).predict(X_test2)
        print("accuracy_score :", accuracy_score(y_test2, y_pred_KNN) * 100)
        print("classification_report:", classification_report(y_test2, y_pred_KNN))


    print('')
    print('')
    print('')
    print('second level done  ')


    #__________________________________________________________________ knn model finsh is run

    model = tf.keras.models.Sequential()
    model.add(Dense(len(y_train), input_shape=(19, )))
    model.add(Dense(len(y_train)//2, activation='relu'))
    model.add(Dense(len(y_train)//4, activation='relu'))
    model.add(Dense(len(y_train)//8, activation='relu'))
    model.add(Dense(len(y_train) // 4, activation='relu'))
    model.add(Dense(len(y_train) // 2, activation='relu'))
    model.add(Dense(len(y_train), activation='relu'))
    #model.compile(optimizer="adam", loss="mae", metrics=['accuracy'])
    #model.fit(X_train, y_train, batch_size=127, epochs=10)

    #prediction = model.predict(X_test)
    #print(prediction)

    #loss = tf.keras.losses.MAE(X_test, prediction)

    #plt.plot(prediction)

    #print(model.evaluate(X_test, y_test)[1])
    #plt.plot(tf.losses(X_test, y_test))

    #plt.show()
#___________________________ ANN MODEL NOT READY !!


#____________________  capture data done here

    #capture = sniff(count=5, filter="port 443")
    #capture.summary()
    #wrpcap("captured_data.pcap", capture)

    #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #data_cap1 = pd.read_csv(r'C:\Users\user\PycharmProjects\pythonFinalProject8\dnscat2\all.csv', nrows=20000)
    #print(data_cap1.head(5))



if __name__ == '__main__':
    print_hi('PyCharm')


