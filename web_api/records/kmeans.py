print(__doc__)

import time
import sys
import csv

import numpy as np
import pylab as pl

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.datasets.samples_generator import make_blobs

##############################################################################
# Generate sample data
np.random.seed(0)

file_name = sys.argv[1]
T=[]
t_data = open(file_name)
for data in t_data:
    T.append(list(data[:-1].split(',')))

X =np.asarray(T)

batch_size = 45
centers = [[1, 1], [-1, -1], [1, -1]]
n_clusters = len(centers)
#X, labels_true = make_blobs(n_samples=3000, centers=centers, cluster_std=0.7)
#print type(X[:10])
#print my_data[:10]


##############################################################################
# Compute clustering with Means

k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
t0 = time.time()
print X[0]
k_means.fit(X)

print 'result is ',X[0,0]
t_batch = time.time() - t0
k_means_labels = k_means.labels_

k_means_cluster_centers = k_means.cluster_centers_
k_means_labels_unique = np.unique(k_means_labels)


##############################################################################
# Plot result

fig = pl.figure(0)
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
colors = ['#4EACC5', '#FF9C34', '#4E9A06']

# We want to have the same colors for the same cluster from the
# MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
# closest one.

distance = euclidean_distances(k_means_cluster_centers,
                               squared=True)
order = distance.argmin(axis=1)

# KMeans
#ax = fig.add_subplot(1,3,1)
ax = pl.axes([0., 0., 1., 1.])
print type(k_means_labels)
for k, col in zip(range(n_clusters), colors):
    my_members = k_means_labels == k

    cluster_center = k_means_cluster_centers[k]
    
    ax.plot(X[my_members, 0], X[my_members, 1], 'w',
            markerfacecolor=col, marker='.')
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)
    ax.set_title('KMeans')
    ax.set_xticks(())
    ax.set_yticks(())
    pl.text(-3.5, 1.8,  'train time: %.2fs\ninertia: %f' % (
        t_batch, k_means.inertia_))
    
    
pl.show()