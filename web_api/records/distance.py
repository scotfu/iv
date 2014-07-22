#! /usr/bin/python
#coding=utf-8
import sys
import math
import random

#read data from a file, return a list of points
def read_data(file_name):
    data = []
    file_handler = open(file_name)
    for line in file_handler:
        data.append(map(float, line[:-1].split(',')))
    file_handler.close()    
    return data

    
#start with no weight, all the dimensions are the same
def binary_euclidean_distance(pointA, pointB):
    result = XOR(pointA, pointB)
    distance = reduce(lambda x,y: x + y, result, 0)
    root_of_distance = math.sqrt(distance)
    return root_of_distance

def XOR(pointA, pointB):
    result = ''
    if len(pointA) != len(pointB):
        raise ValueError('the two points should have the same degree of dimension')
    for pos in range(len(pointA)):
        result = result + chr(pointA[pos] ^ pointB[pos])
    return result
    

#watch out: float flaw 
def euclidean_distance(pointA, pointB):
    if len(pointA) != len(pointB):
        raise ValueError('the two points should have the same degree of dimension')

    dimension = len(pointA)
    distance = 0.0
    for i in range(dimension):
        distance += math.pow(pointA[i] - pointB[i], 2)
    root_of_distance = math.sqrt(distance)
    return root_of_distance

#watch out: float flaw 
def squared_euclidean_distance(pointA, pointB):
    if len(pointA) != len(pointB):
        raise ValueError('the two points should have the same degree of dimension')

    dimension = len(pointA)
    distance = 0.0
    for i in range(dimension):
        distance += math.pow(pointA[i] - pointB[i], 2)

    return distance
    
    
def assignment(points, centroids):
    '''
    assgin points to k clusters, the first step of k-means iteration
    Randomly pick k points as centroids then assgin points to the nearest centroid
    '''
    k = len(centroids)
    num_of_points = len(points)
    cluster_matrix = [[0 for i in range(num_of_points)] for j in range(k)]

    for i in range(len(points)):
        distance = float('inf')
        assign_to = None
        for j in range(len(centroids)):
            e_distance = squared_euclidean_distance(points[i], centroids[j])
            if e_distance <= distance:
                distance = e_distance
                assign_to = j
        cluster_matrix[assign_to][i] = 1
        
    return cluster_matrix


def update_centroids(points, cluster_matrix):
    new_centroids = []
    dimension = len(points[0])
    for cluster in cluster_matrix:
        coordinate = [0 for i in range(dimension)]
        for position in range(len(cluster)):
            if cluster[position] == 1:
               coordinate = map(sum, zip(coordinate, points[position]))
        count = float(cluster.count(1))
        mean = map(lambda x:x/count, coordinate)
        new_centroids.append(mean)    
    return new_centroids

def KMeans(points,centroids):
    #import pprint
    #centroids = random.sample(points, k)
    cluster_matrix = assignment(points, centroids)
    #cluster_matrix
    centroids = update_centroids(points, cluster_matrix)
    return cluster_matrix,centroids
    #plot(points, cluster_matrix, centroids)

def plot(points,cluster_matrix,centroids):
    import numpy as np
    import pylab as pl

    fig = pl.figure(0)
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.9)
    colors = ['#4EACC5', '#FF9C34', '#4E9A06','black']

    # We want to have the same colors for the same cluster from the
    # MiniBatchKMeans and the KMeans algorithm. Let's pair the cluster centers per
    # closest one.

    # KMeans
    #ax = fig.add_subplot(1,3,1)
    ax = pl.axes([0., 0., 1., 1.])

    for k, col in zip(range(len(cluster_matrix)), colors):
        my_members = k
        cluster_center = centroids[k]
        cluster_points =[ points[i] for i in range(len(cluster_matrix[k])) if cluster_matrix[k][i]==1 ]
        ax.plot(*zip(*cluster_points), marker='.',  markerfacecolor=col, ls='')
        
#        ax.plot(X[my_members, 0], X[my_members, 1], 'w',
 #           markerfacecolor=col, marker='.')
        ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)
        ax.set_title('KMeans')
        ax.set_xticks(())
        ax.set_yticks(())
    
    pl.show()
    
if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
    except IndexError:
        raise Exception('File name is needed')

    points = read_data(file_name)

    pointA = points[10]
    pointB = points[1]
#    print euclidean_distance(pointA, pointB)

    #verify the distance using numpy
    import numpy
    A = numpy.array((pointA[0], pointA[1]))
    B = numpy.array((pointB[0], pointB[1]))
    dist = numpy.linalg.norm(A-B)
#    print dist
    KMeans(points, 4)
