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
    

    
def assignment(points, k):
    '''
    assgin points to k clusters, the first step of k-means iteration
    Randomly pick k points as centroids then assgin points to the nearest centroid
    '''
    num_of_points = len(points)
    cluster_matrix = [[0 for i in range(num_of_points)] for j in range(k)]
    
    random.shuffle(points) # shuffle the points randomly
    centroids = points[:k] # then pick the first k points as centroids
    print centroids
    for i in range(len(points[k:])):
        distance = float('inf')
        assign_to = None
        for j in range(len(centroids)):
            e_distance = squared_euclidean_distance(points[i+k], centroids[j])
            if e_distance <= distance:
                distance = e_distance
                assign_to = j
        cluster_matrix[assign_to][i+k] = 1
        
    return cluster_matrix
    
if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
    except IndexError:
        raise Exception('File name is needed')

    data = read_data(file_name)
    print data[1]
    pointA = data[10]
    pointB = data[1]
    print euclidean_distance(pointA, pointB)

    #verify the distance using numpy
    import numpy
    A = numpy.array((pointA[0], pointA[1]))
    B = numpy.array((pointB[0], pointB[1]))
    dist = numpy.linalg.norm(A-B)
    print dist

    import pprint
    print assignment(data, 3)

