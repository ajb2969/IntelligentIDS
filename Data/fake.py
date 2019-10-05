"""
https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py
"""

import csv
import random
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
import matplotlib.pyplot as plt

np.random.seed(42)

def process():
    df = pd.read_csv("fake.csv")
    data = scale(df)
    #print(data)

    n_samples, n_features = data.shape
    #n_digits = len(np.unique(df[0]))
    #labels = df[0]

    print("n_samples %d, \t n_features %d"
          % (n_samples, n_features))

    return data


def kmeans(estimator, name, data):
    estimator.fit(data)


def createcsv():
    rows = []

    for i in range(100):
        duration = random.randint(0,60)
        flags = random.randint(0,10)
        protocol_temp = random.randint(0,6) #number
        switcher = switch()
        protocol = switcher.get(protocol_temp) #string
        src = random.randint(1024,9999)
        dest = random.randint(1024,9999)
        payload = random.randint(0, 9999999)
        packetid = random.randint(0, 9999)
        rows.append([duration, flags, protocol_temp, src, dest, payload, packetid])


    with open('fake.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['duration', 'flags', 'protocol', 'src', 'dest', 'payload', 'packet_id'])
        for row in rows:
            writer.writerow(row)
    csvFile.close()

def switch():
    switcher = {
        1: "upd",
        2: "tcp",
        3: "dns",
        4: "http",
        5: "https",
        6: "tls",
    }
    return switcher


def main():
    """
    uncomment createcsv() if you need to create the csv file
    """

    #createcsv()
    data = process()
    kmeans(KMeans(init='k-means++', n_clusters=2, n_init=10),
                  name="k-means++", data=data)

    kmeans(KMeans(init='random', n_clusters=2, n_init=10),
                  name="random", data=data)

    # in this case the seeding of the centers is deterministic, hence we run the
    # kmeans algorithm only once with n_init=1
    pca = PCA(n_components=2).fit(data)
    kmeans(KMeans(init=pca.components_, n_clusters=2, n_init=1),
                  name="PCA-based",
                  data=data)

    reduced_data = PCA(n_components=2).fit_transform(data)
    km = KMeans(init='k-means++', n_clusters=2, n_init=10)
    km.fit(reduced_data)
    #print('first half', reduced_data[:, 0])
    #print('second half', reduced_data[:, 1])

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02  # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = km.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = km.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the fake dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()

if __name__ == '__main__':
    main()
