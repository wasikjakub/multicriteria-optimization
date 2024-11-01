import tkinter as tk
from tkinter import ttk, messagebox
import time
import numpy as np
from typing import List

from algorirthms import naive_without_filtration, dominated_points_filtration, ideal_point_algorithm


# Define the Tkinter GUI
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Dominated Points Finder")
        
        # Initialize the points list
        self.points = []

        # Input area for dataset configuration
        self.dataset_label = ttk.Label(root, text="Data Points (Python tuple format):")
        self.dataset_label.pack(pady=5)
        self.dataset_entry = ttk.Entry(root, width=50)
        self.dataset_entry.pack(pady=5)
        
        # Button to show input data as a table
        self.show_input_button = ttk.Button(root, text="Show input data as a table", command=self.show_input)
        self.show_input_button.pack(pady=5)

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
        self.run_dominated = ttk.Button(self.buttons_frame, text="Dominated Points Filtration", command=self.run_dominated)
        self.run_dominated.grid(row=1, column=0, padx=5)
        self.run_naive = ttk.Button(self.buttons_frame, text="Naive Without Filtration", command=self.run_naive)
        self.run_naive.grid(row=1, column=1, padx=5)
        self.run_ideal = ttk.Button(self.buttons_frame, text="Ideal Point Algorithm", command=self.run_ideal)
        self.run_ideal.grid(row=1, column=2, padx=5)
        
        # Display results
        self.result_label = ttk.Label(root, text="Results:")
        self.result_label.pack(pady=5)
        self.result_text = tk.Text(root, height=5, width=60)
        self.result_text.pack(pady=5)
        
        # Benchmark button
        self.benchmark_button = ttk.Button(root, text="Benchmark Algorithms", command=self.benchmark)
        self.benchmark_button.pack(pady=10)

    def run_dominated(self):
        results = dominated_points_filtration(self.points)
        self.display_results(results)
    
    def run_naive(self):
        results = naive_without_filtration(self.points)
        self.display_results(results)
    
    def run_ideal(self):
        results = ideal_point_algorithm(self.points)
        self.display_results(results)
            
    def display_results(self, results):
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "\n".join(map(str, results)))
    
    def display_table(self):
        # Clear previous table if it exists
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        # Determine the number of columns based on the tuple size, defaulting to 2 if empty
        num_columns = len(self.points[0]) if self.points else 2
        columns = ["Index"] + [f"Criterium {i + 1}" for i in range(num_columns)]

        # Create Treeview widget
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        self.tree.heading("Index", text="Index")
        self.tree.column("Index", anchor="center", width=50)

        # Configure each coordinate column
        for i, col in enumerate(columns[1:], start=1):
            self.tree.heading(col, text=col)
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
        times = {}
        
        # Run each algorithm and measure time
        for algo_name, algo_func in [
            ("Dominated Points Filtration", dominated_points_filtration),
            ("Naive Without Filtration", naive_without_filtration),
            ("Ideal Point Algorithm", ideal_point_algorithm)
        ]:
            points_copy = self.points[:]  # Use the updated points list
            start = time.time()
            algo_func(points_copy)
            elapsed = time.time() - start
            times[algo_name] = elapsed

        result_message = "Benchmark Results:\n" + "\n".join(f"{algo}: {time:.6f} seconds" for algo, time in times.items())
        self.display_results(result_message)



# Initialize the GUI
root = tk.Tk()
gui = GUI(root)
root.mainloop()