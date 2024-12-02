from typing import List
import numpy as np
from copy import deepcopy
    
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
           

def dominated_points_filtration(X: list):
    X_copy = deepcopy([MyTuple(*element) if not isinstance(element, MyTuple) else element for element in X])
    num_compares = 0
    P = [] 
    i = 0
    
    while i < len(X_copy):
        Y = X_copy[i]
        j = i + 1
        while j < len(X_copy):
            if Y <= X_copy[j]:
                X_copy.pop(j)
            elif X_copy[j] <= Y:
                X_copy.pop(i)
                if i > j:
                    Y = X_copy[j]
                else:
                    Y = X_copy[j - 1]
                    j -= 1
            num_compares += 1
            j += 1
        P.append(Y)
    
        num_compares += len(X_copy)
        X_copy = [point for point in X_copy if not (Y <= point)]
        if len(X_copy) == 1:
            P.append(X_copy[0])
            break
        i += 1
    return P, num_compares


def naive_without_filtration(X: list):
    X_copy = deepcopy([MyTuple(*element) if not isinstance(element, MyTuple) else element for element in X])
    num_compares = 0
    P = []
    i = 0
    
    while i < len(X_copy):
        Y = X_copy[i]
        fl = 0
        j = i + 1
        while j < len(X_copy):
            if Y <= X_copy[j]:
                del X_copy[j] 
            elif X_copy[j] <= Y and X_copy[j] <= Y:
                Y = X_copy[j]
                fl = 1
                del X_copy[i]
            else:
                j += 1
            num_compares += 1
        if Y not in P:
            P.append(Y)
        
        if fl == 0:
            del X_copy[i]
        else:
            i += 1
    return P, num_compares


def ideal_point_algorithm(X: list):
    X_copy = deepcopy(X)
    num_compares = 0
    P = []
    X_copy = np.array(X_copy)  
    
    xmin = np.min(X_copy, axis=0)  
    d = [np.sum((xmin - X_copy[j]) ** 2) for j in range(len(X_copy))]  
    sorted_indices = np.argsort(d)  
    remaining_points = X_copy[sorted_indices].tolist()  
    while remaining_points:
        current_point = remaining_points.pop(0)      
        P.append(current_point)   
        num_compares += len(remaining_points)    
        remaining_points = [
            point for point in remaining_points 
            if not all(np.array(current_point) <= np.array(point))
        ]
    return tuple(map(tuple, P)), num_compares


def dominated_points_filtration_max(X: list):
    X_copy = deepcopy([MyTuple(*element) if not isinstance(element, MyTuple) else element for element in X])
    num_compares = 0
    P = [] 
    i = 0
    
    while i < len(X_copy):
        Y = X_copy[i]
        j = i + 1
        while j < len(X_copy):
            if Y >= X_copy[j]:
                X_copy.pop(j) 
            elif X_copy[j] >= Y:
                X_copy.pop(i)
                if i > j:
                    Y = X_copy[j]
                else:
                    Y = X_copy[j - 1]
                    j -= 1
            num_compares += 1
            j += 1
        P.append(Y)
    
        num_compares += len(X_copy)
        X_copy = [point for point in X_copy if not (Y >= point)]
        if len(X_copy) == 1:
            P.append(X_copy[0])
            break
        i += 1
    return P, num_compares


def naive_without_filtration_max(X: list):
    X_copy = deepcopy([MyTuple(*element) if not isinstance(element, MyTuple) else element for element in X])
    num_compares = 0
    P = []
    i = 0
    
    while i < len(X_copy):
        Y = X_copy[i]
        fl = 0
        j = i + 1
        while j < len(X_copy):
            if Y >= X_copy[j]:
                del X_copy[j] 
            elif X_copy[j] >= Y:
                Y = X_copy[j]
                fl = 1
                del X_copy[i]
            else:
                j += 1
            num_compares += 1
        if Y not in P:
            P.append(Y)
        
        if fl == 0:
            del X_copy[i]
        else:
            i += 1
    return P, num_compares


def ideal_point_algorithm_max(X: list):
    X_copy = deepcopy(X)
    num_compares = 0
    P = []
    X_copy = np.array(X_copy)  
    
    xmax = np.max(X_copy, axis=0)  
    d = [np.sum((xmax - X_copy[j]) ** 2) for j in range(len(X_copy))]  
    sorted_indices = np.argsort(d)  
    remaining_points = X_copy[sorted_indices].tolist()  
    while remaining_points:
        current_point = remaining_points.pop(0)      
        P.append(current_point)      
        num_compares += len(remaining_points)  
        remaining_points = [
            point for point in remaining_points 
            if not all(np.array(current_point) >= np.array(point))
        ]
    return tuple(map(tuple, P)), num_compares