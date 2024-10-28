from typing import List
import numpy as np

class MyTuple:
    def __init__(self, *args):
        self.data = tuple(args)

    def __lt__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return all(x < y for x, y in zip(self.data, other.data))
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return all(x <= y for x, y in zip(self.data, other.data))
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return all(x > y for x, y in zip(self.data, other.data))
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return all(x >= y for x, y in zip(self.data, other.data))
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return all(x == y for x, y in zip(self.data, other.data))
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, MyTuple) and len(self.data) == len(other.data):
            return any(x != y for x, y in zip(self.data, other.data))
        return NotImplemented
    
    def __repr__(self) -> str:
        return f"{self.data}"
    
    
def dominated_points_filtration(X):
    P = [] 
    i = 0
    while i < len(X):
        Y = X[i]
        j = i + 1
        while j < len(X):
            if Y <= X[j]:
                X.pop(j) 
            elif X[j] <= Y:
                X.pop(i)
                Y = X[j]
            else:
                j += 1
        P.append(Y)
    
        X = [point for point in X if not (Y <= point)]
        if len(X) == 1:
            P.append(X[0])
            break
        i += 1
    return P


def naive_without_filtration(X: List[int]) -> List[int]:
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