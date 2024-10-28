import tkinter as tk
from tkinter import ttk, messagebox
import time
import numpy as np
from typing import List

from algorirthms import MyTuple, naive_without_filtration, dominated_points_filtration, ideal_point_algorithm


def dominated_points_filtration(X: List[tuple]) -> List[tuple]:
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


def naive_without_filtration(X: List[tuple]) -> List[tuple]:
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


def ideal_point_algorithm(X: List[tuple]) -> List[tuple]:
    P = []
    X = np.array(X)
    xmin = np.min(X, axis=0)
    d = [np.sum((xmin - X[j]) ** 2) for j in range(len(X))]
    sorted_indices = np.argsort(d)
    remaining_points = X[sorted_indices].tolist()
    while remaining_points:
        current_point = remaining_points.pop(0)
        P.append(tuple(current_point))
        remaining_points = [
            point for point in remaining_points
            if not all(np.array(current_point) <= np.array(point))
        ]
    return P


# Define the Tkinter GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Dominated Points Finder")

        # Input area for dataset configuration
        self.dataset_label = ttk.Label(root, text="Data Points (Python tuple format):")
        self.dataset_label.pack(pady=5)

        self.dataset_entry = ttk.Entry(root, width=50)
        self.dataset_entry.pack(pady=5)

        # Add buttons for each algorithm
        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.pack(pady=5)

        self.run_dominated = ttk.Button(self.buttons_frame, text="Dominated Points Filtration", command=self.run_dominated)
        self.run_dominated.grid(row=0, column=0, padx=5)

        self.run_naive = ttk.Button(self.buttons_frame, text="Naive Without Filtration", command=self.run_naive)
        self.run_naive.grid(row=0, column=1, padx=5)

        self.run_ideal = ttk.Button(self.buttons_frame, text="Ideal Point Algorithm", command=self.run_ideal)
        self.run_ideal.grid(row=0, column=2, padx=5)

        # Display results
        self.result_label = ttk.Label(root, text="Results:")
        self.result_label.pack(pady=5)

        self.result_text = tk.Text(root, height=10, width=60)
        self.result_text.pack(pady=5)

        # Benchmark button
        self.benchmark_button = ttk.Button(root, text="Benchmark Algorithms", command=self.benchmark)
        self.benchmark_button.pack(pady=10)

    def parse_input(self):
        raw_data = self.dataset_entry.get()
        try:
            # Use eval on the whole input string as a list of tuples
            points = eval(f"[{raw_data}]")
            
            # Check that all items are tuples with numeric elements
            if not all(isinstance(pt, tuple) and len(pt) == 2 and all(isinstance(x, (int, float)) for x in pt) for pt in points):
                raise ValueError
            
            return points  # Return as list of tuples
        
        except (SyntaxError, ValueError, TypeError):
            messagebox.showerror("Error", "Invalid data format. Use tuple format: (x1, y1), (x2, y2), ...")
            return None

    def display_results(self, results):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(map(str, results)))

    def run_dominated(self):
        points = self.parse_input()
        if points:
            results = dominated_points_filtration(points)
            self.display_results(results)

    def run_naive(self):
        points = self.parse_input()
        if points:
            results = naive_without_filtration(points)
            self.display_results(results)

    def run_ideal(self):
        points = self.parse_input()
        if points:
            results = ideal_point_algorithm(points)
            self.display_results(results)

    def benchmark(self):
        points = self.parse_input()
        if not points:
            return
        
        times = {}
        
        # Run each algorithm and measure time
        for algo_name, algo_func in [
            ("Dominated Points Filtration", dominated_points_filtration),
            ("Naive Without Filtration", naive_without_filtration),
            ("Ideal Point Algorithm", ideal_point_algorithm)
        ]:
            points_copy = points[:]
            start = time.time()
            algo_func(points_copy)
            elapsed = time.time() - start
            times[algo_name] = elapsed

        # Display benchmark results
        result_message = "Benchmark Results:\n" + "\n".join(f"{algo}: {time:.6f} seconds" for algo, time in times.items())
        self.display_results(result_message)


# Initialize the GUI
root = tk.Tk()
gui = GUI(root)
root.mainloop()