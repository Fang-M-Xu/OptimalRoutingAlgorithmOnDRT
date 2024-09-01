# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:40:23 2023

@author: Fang Xu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


Jerusalem_grid = np.mat([[0, 0, 0, 0, 0, 0, 0, 0, 0, '100506', 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, '100505', 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, '100515', '100507', '100508'],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '100514', '100598'],
                         [0, 0, 0, 0, 0, '100524', '100526',
                             0, 0, 0, '100512', '100509'],
                         [0, 0, 0, 0, 0, '100523', '100525', '100530',
                          '100511', '100510', '100513', '100517'],
                         [0, 0, 0,  '100551', '100553', '100531',
                             '100528', '100527', 0, 0, 0, 0],
                         [0, 0, '100585', '100550', '100548', '100552', '100546',
                          '100547', '100529', '100520', '100519',  '100516'],
                         [0, 0, '100554', '100558', '100549', '100537', '100545',
                          '100439',  '100539', '100521', '100668',  '100522'],
                         [0, '100560', '100561', '100556', '100557', '100543',
                          '100541', '100540', '100544', '100538', '100518',   0],
                         ['100562', '100574', '100555', '101260', '100569', '100542',
                          '101258', '100577', '100576', '100533', '100534', 0],
                         [0, '100559', '100575', '100573', '100572',
                          '100570', '100582', '100793', '100532', 0, 0, 0],
                         [0, 0, 0, 0, '100799', '100571', '100586',
                             '100581', '100584', '100583', 0, 0],
                         [0, 0, '100566', '100669', '100667', '100587',
                          '100578', '100580', '100535', 0, 0, 0],
                         [0, 0, 0, '100565', '100564', '100563', '100579', '100536', 0, 0, 0, 0]])


x_aixs = []
y_aixs = []
x_grid = Jerusalem_grid.shape[0]
y_grid = Jerusalem_grid.shape[1]

for x in range(x_grid):
    for y in range(y_grid):
        if Jerusalem_grid[x, y] != '0':
            x_aixs.append(x_grid-x)
            y_aixs.append(y+1)


passenger_df = pd.read_csv('Data/Passenger_Request2.csv')
destinaiton = list(passenger_df['Destination'])
departure = list(passenger_df['Departure'])



destinaiton_x_aixs = []
destinaiton_y_aixs = []
for item in destinaiton:
    for x in range(x_grid):
        for y in range(y_grid):
            if Jerusalem_grid[x, y] == str(item):
                destinaiton_x_aixs.append(x_grid-x)
                destinaiton_y_aixs.append(y+1)


departure_x_aixs = []
departure_y_aixs = []
for item in departure:
    for x in range(x_grid):
        for y in range(y_grid):
            if Jerusalem_grid[x, y] == str(item):
                departure_x_aixs.append(x_grid-x)
                departure_y_aixs.append(y+1)


colors1 = '#00CED1'
colors2 = '#DC143C'
colors3 = '#000000'
plt.xlim(0, 15)
plt.ylim(0, 16)
plt.scatter(y_aixs, x_aixs, c=colors1)
plt.scatter(destinaiton_y_aixs, destinaiton_x_aixs, c=colors2)
plt.scatter(departure_y_aixs, departure_x_aixs, c=colors3)
plt.title("Matrix of 90 area of Jerusalem")
plt.show()


# use DBSCAN to group destination and departure place

# get parameter : eps
def getMinPts(data, k):
    cal_dist = []
    for i in range(data.shape[0]):
        dist = ((((data[i]) - data)**2).sum(axis=1)**0.5)
        print(dist)
        dist.sort()
        cal_dist.append(dist[k])
        print('cal_dist', cal_dist)
    return np.array(cal_dist)


# coordinate of Jerusalem
coordinate_Jerusalem = list(zip(y_aixs, x_aixs))
coordinate_Jerusalem_v2 = []
for item in coordinate_Jerusalem:
    item_list = list(item)
    coordinate_Jerusalem_v2.append(item_list)

coordinate_Jerusalem_v2 = np.array(coordinate_Jerusalem_v2)

cal_dist = getMinPts(coordinate_Jerusalem_v2, 3)
cal_dist.sort()
print('cal_dist=====', cal_dist)
plt.plot(np.arange(cal_dist.shape[0]), cal_dist[::-1])
eps = cal_dist[::-1][15]
print('eps=====', eps)
clusters = DBSCAN(eps=eps, min_samples=3).fit_predict(coordinate_Jerusalem_v2)
print('eps=====', eps)
# result
# for i, cluster in enumerate(clusters):
#print(f"point{i+1}belong to cluster {cluster}")

#plt.scatter(coordinate_Jerusalem_v2[:, 0], coordinate_Jerusalem_v2[:, 1], c=clusters)
# plt.show()


# coordinate of destinaiton red
coordinate_destinaiton = list(zip(destinaiton_y_aixs, destinaiton_x_aixs))
coordinate_destinaiton_v2 = []
for item in coordinate_destinaiton:
    item_list = list(item)
    coordinate_destinaiton_v2.append(item_list)

coordinate_destinaiton_v2 = np.array(coordinate_destinaiton_v2)
cal_dist = getMinPts(coordinate_destinaiton_v2, 2)
cal_dist.sort()
# plt.plot(np.arange(cal_dist.shape[0]),cal_dist[::-1])
eps = cal_dist[::-1][7]
# print(eps)
clusters_destinaiton = DBSCAN(
    eps=eps+1, min_samples=2).fit_predict(coordinate_destinaiton_v2)
print('clusters_destinaiton=====', clusters_destinaiton)
print('coordinate_destinaiton_v2====', coordinate_destinaiton_v2)
# result
# for i, cluster in enumerate(clusters_destinaiton):
#print(f"point{i+1}belong to cluster {cluster}")
plt.xlim(0, 15)
plt.ylim(0, 15)
# plt.axes().set_facecolor("gray")
plt.scatter(coordinate_destinaiton_v2[:, 0],
            coordinate_destinaiton_v2[:, 1], c=clusters_destinaiton)
plt.show()

# get the center of cluster
destinaiton_cluster_center = []
clusters_destinaiton_set = set(clusters_destinaiton)
for i in clusters_destinaiton_set:
    destinaiton_cluster_center.append(
        np.mean(coordinate_destinaiton_v2[clusters_destinaiton == i], axis=0))

# calculate center of destinaiton cluster
destinaiton_cluster_center_x = []
destinaiton_cluster_center_y = []
destinaiton_cluster_center_x_v2 = []
destinaiton_cluster_center_y_v2 = []

for item in destinaiton_cluster_center:
    destinaiton_cluster_center_x.append(item[0])
    destinaiton_cluster_center_y.append(item[1])

for item in destinaiton_cluster_center_x:
    destinaiton_cluster_center_x_v2.append(round(item))

for item in destinaiton_cluster_center_y:
    destinaiton_cluster_center_y_v2.append(round(item))

destinaiton_cluster_center = list(
    zip(destinaiton_cluster_center_x_v2, destinaiton_cluster_center_y_v2))
destinaiton_cluster_center_v2 = []
for item in destinaiton_cluster_center:
    item_list = list(item)
    destinaiton_cluster_center_v2.append(item_list)

destinaiton_cluster_center_v2 = np.array(destinaiton_cluster_center_v2)

plt.xlim(0, 15)
plt.ylim(0, 15)
plt.scatter(coordinate_destinaiton_v2[:, 0],
            coordinate_destinaiton_v2[:, 1], c=clusters_destinaiton)
plt.scatter(destinaiton_cluster_center_v2[:, 0],
            destinaiton_cluster_center_v2[:, 1], marker='x', c='r')
plt.title("Center place of destinaiton group")
plt.show()


# coordinate of departure black
coordinate_departure = list(zip(departure_y_aixs, departure_x_aixs))
coordinate_departure_v2 = []
for item in coordinate_departure:
    item_list = list(item)
    coordinate_departure_v2.append(item_list)

coordinate_departure_v2 = np.array(coordinate_departure_v2)

cal_dist = getMinPts(coordinate_departure_v2, 3)
cal_dist.sort()
# plt.plot(np.arange(cal_dist.shape[0]),cal_dist[::-1])
eps = cal_dist[::-1][6]

clusters_departure = DBSCAN(
    eps=eps, min_samples=2).fit_predict(coordinate_departure_v2)
# result
# for i, cluster in enumerate(clusters_departure):
#print(f"point{i+1}belong to cluster {cluster}")
# plt.xlim(0,15)
# plt.ylim(0,15)
# plt.axes().set_facecolor("gray")
#plt.scatter(coordinate_departure_v2[:, 0], coordinate_departure_v2[:, 1], c=clusters_departure)
# plt.show()



# group the passenger departure place based on the destination group:intersection of two cluster
departure_array = np.array(departure)
count = 0
for num in clusters_destinaiton_set:
    singleGroupOnDestination = departure_array[clusters_destinaiton == num]
    singleGroupOnDeparture = departure_array[clusters_departure == num]
    intersectSingleGroup = np.intersect1d(
        singleGroupOnDestination, singleGroupOnDeparture, False)
    exclusiveSingleGroup = np.setxor1d(
        singleGroupOnDestination, singleGroupOnDeparture, False)
    for item in intersectSingleGroup:
        index = np.where(departure_array == item)
        clusters_departure[index] = count
    count = count+1
    for item in exclusiveSingleGroup:
        index = np.where(departure_array == item)
        clusters_departure[index] = count

# get the center of cluster
departure_cluster_center = []
clusters_departure_set = set(clusters_departure)
for i in clusters_departure_set:
    departure_cluster_center.append(
        np.mean(coordinate_departure_v2[clusters_departure == i], axis=0))
# calculate center of departure cluster
departure_cluster_center_x = []
departure_cluster_center_y = []

departure_cluster_center_x_v2 = []
departure_cluster_center_y_v2 = []

for item in departure_cluster_center:
    departure_cluster_center_x.append(round(item[0]))
    departure_cluster_center_y.append(round(item[1]))

for item in departure_cluster_center_x:
    departure_cluster_center_x_v2.append(round(item))

for item in departure_cluster_center_y:
    departure_cluster_center_y_v2.append(round(item))


departure_cluster_center = list(
    zip(departure_cluster_center_x_v2, departure_cluster_center_y_v2))
departure_cluster_center_v2 = []
for item in departure_cluster_center:
    item_list = list(item)
    departure_cluster_center_v2.append(item_list)

departure_cluster_center_v2 = np.array(departure_cluster_center_v2)


plt.xlim(0, 15)
plt.ylim(0, 15)
plt.scatter(coordinate_departure_v2[:, 0],
            coordinate_departure_v2[:, 1], c=clusters_departure)
plt.scatter(departure_cluster_center_v2[:, 0],
            departure_cluster_center_v2[:, 1], marker='x', c='r')
plt.title("Center place of departure group")
plt.show()
