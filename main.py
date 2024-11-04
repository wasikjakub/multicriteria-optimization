import tkinter as tk
from tkinter import ttk, messagebox
import time
import numpy as np
from typing import List
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from algorirthms import MyTuple, naive_without_filtration, dominated_points_filtration, ideal_point_algorithm, naive_without_filtration_max, dominated_points_filtration_max, ideal_point_algorithm_max


# Define the Tkinter GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Dominated Points Finder")
        
        # Initialize the points list
        self.points = []
        self.output_points = []
        self.criterion = None

        # Input area for dataset configuration
        self.dataset_label = ttk.Label(root, text="Enter Data Points (Python tuple format):")
        self.dataset_label.pack(pady=5)
        self.dataset_entry = ttk.Entry(root, width=50)
        self.dataset_entry.pack(pady=5)
        
        # Button to show input data as a table
        self.show_input_button = ttk.Button(root, text="Show input data as a table", command=self.show_input)
        self.show_input_button.pack(pady=5)
        
        self.separator = ttk.Separator(root, orient="horizontal")
        self.separator.pack(fill="x", pady=10)
        
        # Frame for generating random points
        self.random_frame = ttk.Frame(root)
        self.random_frame.pack(pady=10)

        self.criteria_label = ttk.Label(self.random_frame, text="Criterion num:")
        self.criteria_label.grid(row=0, column=0, padx=5)
        self.criteria_entry = ttk.Entry(self.random_frame, width=10)
        self.criteria_entry.grid(row=0, column=1, padx=5)
        
        self.num_points_label = ttk.Label(self.random_frame, text="Points num:")
        self.num_points_label.grid(row=0, column=2, padx=5)
        self.num_points_entry = ttk.Entry(self.random_frame, width=10)
        self.num_points_entry.grid(row=0, column=3, padx=5)
        
        self.distribution_label = ttk.Label(self.random_frame, text="Distribution:")
        self.distribution_label.grid(row=0, column=4, padx=5)
        self.distribution_var = tk.StringVar(value="Gaussian")
        self.distribution_menu = ttk.Combobox(self.random_frame, textvariable=self.distribution_var, values=["Gaussian", "Exponential", "Poisson"], width=10)
        self.distribution_menu.grid(row=0, column=5, padx=5)
        
        self.mean_label = ttk.Label(self.random_frame, text="Mean:")
        self.mean_label.grid(row=1, column=0, padx=5)
        self.mean_entry = ttk.Entry(self.random_frame, width=10)
        self.mean_entry.grid(row=1, column=1, padx=5)

        self.stdev_label = ttk.Label(self.random_frame, text="Stdev:")
        self.stdev_label.grid(row=1, column=2, padx=5)
        self.stdev_entry = ttk.Entry(self.random_frame, width=10)
        self.stdev_entry.grid(row=1, column=3, padx=5)
        
        self.generate_button = ttk.Button(self.random_frame, text="Generate Points", command=self.generate_points)
        self.generate_button.grid(row=1, column=5, padx=5)

        # Table area for displaying tuples
        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(pady=10, fill="x")
        
        # Display initial table with any points
        self.display_table()
        
        # Frame for adding points
        self.add_frame = ttk.Frame(root)
        self.add_frame.pack(pady=5)

        self.add_entry = ttk.Entry(self.add_frame, width=20)
        self.add_entry.grid(row=0, column=0, padx=5)
        self.add_button = ttk.Button(self.add_frame, text="Add Point", command=self.add_point)
        self.add_button.grid(row=0, column=1, padx=5)

        # Frame for updating points
        self.update_frame = ttk.Frame(root)
        self.update_frame.pack(pady=5)

        self.update_entry = ttk.Entry(self.update_frame, width=20)
        self.update_entry.grid(row=0, column=0, padx=5)
        self.update_button = ttk.Button(self.update_frame, text="Update Selected Point", command=self.update_point)
        self.update_button.grid(row=0, column=1, padx=5)
        
        # Button for deleting points
        self.delete_button = ttk.Button(self.update_frame, text="Delete Selected Point", command=self.delete_point)
        self.delete_button.grid(row=0, column=2, padx=5)

        # Horizontal separator between update section and algorithm buttons
        self.separator = ttk.Separator(root, orient="horizontal")
        self.separator.pack(fill="x", pady=10)
        
        # Frame for algorithm buttons
        self.buttons_frame = ttk.Frame(root)
        self.buttons_frame.pack(pady=5)
        
        # Radio button variable to choose criterion mode
        self.criterion = tk.StringVar(value='min')

        # Add radio buttons for min and max criteria
        self.min_button = ttk.Radiobutton(self.buttons_frame, text="Min criterion", value='min', variable=self.criterion)
        self.min_button.grid(row=0, column=0, padx=5)
        self.min_button.invoke()  # Set default to min
        self.max_button = ttk.Radiobutton(self.buttons_frame, text="Max criterion", value='max', variable=self.criterion)
        self.max_button.grid(row=0, column=1, padx=5)

        # Rename the buttons to avoid name conflict with methods
        self.run_naive_button = ttk.Button(self.buttons_frame, text="Algorytm bez filtracji", command=self.run_naive)
        self.run_naive_button.grid(row=1, column=0, padx=5)
        self.run_dominated_button = ttk.Button(self.buttons_frame, text="Algorytm z filtracją punktów zdominowanych", command=self.run_dominated)
        self.run_dominated_button.grid(row=1, column=1, padx=5)
        self.run_ideal_button = ttk.Button(self.buttons_frame, text="Algorytm oparty o punkt idealny", command=self.run_ideal)
        self.run_ideal_button.grid(row=1, column=2, padx=5)
        
        # Display results
        self.result_label = ttk.Label(root, text="Results:")
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(root, height=5, width=60)
        self.result_text.pack(pady=5)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)  # Set padding for the frame

        # Benchmark button
        benchmark_button = ttk.Button(button_frame, text="Benchmark algorithms", command=self.benchmark)
        benchmark_button.pack(side="left", padx=10)

        # Plot button
        plot_button = ttk.Button(button_frame, text="Plot", command=self.plot_button_action)
        plot_button.pack(side="right", padx=10)
        
    def run_dominated(self):
        if self.criterion.get() == 'min':
            start = time.time()
            results, comparisons = dominated_points_filtration(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
        else:
            start = time.time()
            results, comparisons = dominated_points_filtration_max(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
    
    def run_naive(self):
        if self.criterion.get() == 'min':
            start = time.time()
            results, comparisons = naive_without_filtration(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
        else:
            start = time.time()
            results, comparisons = naive_without_filtration_max(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
    
    def run_ideal(self):
        if self.criterion.get() == 'min':
            start = time.time()
            results, comparisons = ideal_point_algorithm(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
        else:
            start = time.time()
            results, comparisons = ideal_point_algorithm_max(self.points)
            elapsed_time = (time.time() - start) * 1000
            self.display_results(results)
            self.output_points = results
            return elapsed_time, comparisons
            
    def display_results(self, results):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(map(str, results)))
    
    def generate_points(self):
        try:
            self.points = []
            num_criteria = int(self.criteria_entry.get())
            dist_type = self.distribution_var.get()
            num_points = int(self.num_points_entry.get())
            
            if num_criteria < 2 or num_criteria > 10:
                raise ValueError("Number of criteria should be between 2 and 10.")
            
            points = []
            if dist_type == "Gaussian":
                mean = float(self.mean_entry.get())
                stdev = float(self.stdev_entry.get())
                points = [tuple(np.round((np.random.normal(mean, stdev, num_criteria)), 2)) for _ in range(num_points)]
            elif dist_type == "Exponential":
                mean = float(self.mean_entry.get())
                points = [tuple(np.round(np.random.exponential(mean, num_criteria), 2)) for _ in range(num_points)]
            elif dist_type == "Poisson":
                mean = float(self.mean_entry.get())
                points = [tuple(np.round(np.random.poisson(mean, num_criteria), 2)) for _ in range(num_points)]
            
            self.points.extend(points)  # Update points list
            self.display_table()  # Refresh the table with new points
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    
    def display_table(self):
        # Clear previous table if it exists
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Determine the number of columns based on the tuple size, defaulting to 2 if empty
        num_columns = len(self.points[0]) if self.points else 2
        columns = ["Index"] + [f"Criterion {i + 1}" for i in range(num_columns)]

        # Create Treeview widget
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.heading("Index", text="Index")
        self.tree.column("Index", anchor="center", width=50)

        # Configure each coordinate column and bind header clicks to sort function
        for i, col in enumerate(columns[1:], start=1):
            self.tree.heading(col, text=col, command=lambda _col=col, idx=i: self.sort_column(idx))
            self.tree.column(col, anchor="center", width=100)

        # Populate Treeview with current points
        for idx, point in enumerate(self.points):
            tag = 'g' if idx % 2 else 'b'
            self.tree.insert("", "end", values=(idx + 1, *point), tags=tag)

        # Configure alternating row colors
        self.tree.tag_configure('g', background='#78de98')
        self.tree.tag_configure('b', background='#3297a8')

        # Pack Treeview to display table
        self.tree.pack(fill="x")

    def sort_column(self, col_index):
        # Toggle sorting direction for each criterion independently
        if not hasattr(self, "sort_orders"):
            self.sort_orders = {}

        # Set or toggle the sorting order for the chosen column
        self.sort_orders[col_index] = not self.sort_orders.get(col_index, False)

        # Sort points based only on the selected criterion
        self.points.sort(key=lambda x: x[col_index - 1], reverse=self.sort_orders[col_index])

        # Refresh the table to reflect the sorted data
        self.display_table()

    def parse_input(self):
        raw_data = self.dataset_entry.get()
        try:
            # Parse input string into a list of tuples
            points = eval(f"[{raw_data}]")
            if not all(isinstance(pt, tuple) and all(isinstance(x, (int, float)) for x in pt) for pt in points):
                raise ValueError
            return points
        except (SyntaxError, ValueError, TypeError):
            messagebox.showerror("Error", "Invalid data format. Use tuple format.")
            return None

    def show_input(self):
        # Parse input, update points, and display them in the table
        points = self.parse_input()
        if points:
            self.points = points  # Update internal data
            self.display_table()  # Refresh table with new data

    def add_point(self):
        try:
            new_point = eval(f"({self.add_entry.get()})")
            if isinstance(new_point, tuple) and all(isinstance(x, (int, float)) for x in new_point):
                self.points.append(new_point)  # Update internal data
                self.display_table()  # Refresh table to show added point
                self.add_entry.delete(0, tk.END)
            else:
                raise ValueError
        except (SyntaxError, ValueError, TypeError):
            messagebox.showerror("Error", "Invalid point format. Use tuple format.")

    def update_point(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No row selected.")
            return

        try:
            updated_point = eval(f"({self.update_entry.get()})")
            if isinstance(updated_point, tuple) and all(isinstance(x, (int, float)) for x in updated_point):
                item_id = selected_item[0]
                index = int(self.tree.item(item_id, 'values')[0]) - 1
                self.points[index] = updated_point  # Update internal data list
                self.display_table()  # Refresh table to show updated point
                self.update_entry.delete(0, tk.END)
            else:
                raise ValueError
        except (SyntaxError, ValueError, TypeError):
            messagebox.showerror("Error", "Invalid point format for update.")

    def delete_point(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No row selected.")
            return

        item_id = selected_item[0]
        index = int(self.tree.item(item_id, 'values')[0]) - 1
        del self.points[index]  # Remove point from internal list
        self.display_table()  # Refresh table to show deletion
    
    def benchmark(self):
        # Run each algorithm and store results
        benchmarks = [
            ("Algorytm bez filtracji", *self.run_naive()),
            ("Algorytm z filtracją punktów zdominowanych", *self.run_dominated()),
            ("Algorytm oparty o punkt idealny", *self.run_ideal())
        ]

        # Create a new window for displaying the benchmark results
        benchmark_window = tk.Toplevel(self.root)
        benchmark_window.title("Benchmark Results")

        # Set up the Treeview widget
        columns = ("Algorithm", "Execution Time (ms)", "Number of Comparisons")
        tree = ttk.Treeview(benchmark_window, columns=columns, show="headings")
        tree.heading("Algorithm", text="Algorithm")
        tree.heading("Execution Time (ms)", text="Execution Time (ms)")
        tree.heading("Number of Comparisons", text="Number of Comparisons")
        
        # Insert benchmark data into the Treeview
        for algo_name, exec_time, comparisons in benchmarks:
            tree.insert("", "end", values=(algo_name, f"{exec_time:.2f}", comparisons))
        
        # Pack and display the Treeview
        tree.pack(padx=10, pady=10, fill="both", expand=True)

    def plot_button_action(self):
        # Wrapper function that calls plot_points with the correct arguments
        self.plot_points(self.points, self.output_points)
                
    def plot_points(self, input_points, output_points):
        '''
        Plots input and output points in 2D or 3D.
        Different colors are used for each distinct group in output points.

        Parameters:
            input_points (List[Tuple[float, ...]]): List of tuples representing input points.
            output_points (List[Tuple[float, ...]]): List of tuples representing output points.
        '''
        # Helper function to convert MyTuple to a tuple
        def to_tuple(point):
            if isinstance(point, MyTuple):
                return point.data  # Access the `data` attribute which contains the tuple
            return point

        # Convert MyTuple instances to tuples
        input_points = [to_tuple(point) for point in input_points]
        output_points = [to_tuple(point) for point in output_points]  # Treat output_points as a flat list

        # Check dimensionality of points
        is_3d = len(input_points[0]) == 3  # Assume points are consistent in dimensions

        # Set up plot
        fig = plt.figure()
        if is_3d:
            ax = fig.add_subplot(111, projection='3d')
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")
            ax.set_zlabel("Z-axis")
        else:
            ax = fig.add_subplot(111)
            ax.set_xlabel("X-axis")
            ax.set_ylabel("Y-axis")

        # Plot input points in blue
        if is_3d:
            ax.scatter([p[0] for p in input_points], [p[1] for p in input_points], [p[2] for p in input_points], 
                    color='blue', label='Input Points', alpha=0.6)
        else:
            ax.scatter([p[0] for p in input_points], [p[1] for p in input_points], 
                    color='blue', label='Input Points', alpha=0.6)

        # Plot output points in a different color
        if is_3d:
            ax.scatter([p[0] for p in output_points], [p[1] for p in output_points], [p[2] for p in output_points], 
                    color='red', label='Output Points', alpha=0.6)
        else:
            ax.scatter([p[0] for p in output_points], [p[1] for p in output_points], 
                    color='red', label='Output Points', alpha=0.6)

        # Add legend and show plot
        plt.legend()
        plt.show()






# Initialize the GUI
root = tk.Tk()
gui = GUI(root)
root.mainloop()