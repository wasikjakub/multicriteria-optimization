from typing import List
import numpy as np
    
def dominated_points_filtration(X: list) -> list:
    P = [] 
    i = 0
    while i < len(X):
        Y = X[i]
        j = i + 1
        while j < len(X):
            if Y[0] <= X[j][0] and Y[1] <= X[j][1]:
                X.pop(j) 
            elif X[j][0] <= Y[0] and X[j][1] <= Y[1]:
                X.pop(i)
                Y = X[j]
            else:
                j += 1
        P.append(Y)
    
        X = [point for point in X if not (Y[0] <= point[0] and Y[1] <= point[1])]
        if len(X) == 1:
            P.append(X[0])
            break
        i += 1
    return P


def naive_without_filtration(X: list) -> list:
    P = []
    i = 0
    while i < len(X):
        Y = X[i]
        fl = 0
        j = i + 1
        while j < len(X):
            if Y[0] <= X[j][0] and Y[1] <= X[j][1]:
                del X[j] 
            elif X[j][0] <= Y[0] and X[j][1] <= Y[1]:
                Y = X[j]
                fl = 1
                del X[i]
            else:
                j += 1
        if Y not in P:
            P.append(Y)
        if fl == 0:
            del X[i]
        else:
            i += 1
    return P


def ideal_point_algorithm(X: list) -> list:
    P = []
    X = np.array(X)
    xmin = np.min(X, axis=0)
    d = [np.sum((xmin - X[j]) ** 2) for j in range(len(X))]
    sorted_indices = np.argsort(d)
    remaining_points = X[sorted_indices].tolist()
    
    while remaining_points:
        current_point = remaining_points.pop(0)
        P.append(current_point)
        remaining_points = [
            point for point in remaining_points 
            if not all(np.array(current_point) <= np.array(point))
        ] 
    return P