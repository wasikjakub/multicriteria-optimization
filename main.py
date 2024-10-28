import tkinter as tk
from tkinter import ttk, messagebox

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Non-Dominated Points Finder")
        self.root.geometry("800x600")

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create frames for each tab
        self.criteria_tab = ttk.Frame(self.notebook)
        self.values_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.criteria_tab, text="Editor of Criteria")
        self.notebook.add(self.values_tab, text="Editor of Values")

        # Criteria editor setup
        self.setup_criteria_editor()
        # Values editor setup
        self.setup_values_editor()
        # Action controls setup
        self.setup_action_controls()

    def setup_criteria_editor(self):
        # Frame for Criteria Editor in criteria_tab
        criteria_frame = ttk.Frame(self.criteria_tab)
        criteria_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Treeview for Criteria List
        self.criteria_tree = ttk.Treeview(criteria_frame, columns=("Name", "Direction"), show="headings")
        self.criteria_tree.heading("Name", text="Name")
        self.criteria_tree.heading("Direction", text="Direction")
        self.criteria_tree.pack(side="left", fill="both", expand=True)

        # Sample criteria data
        for i in range(1, 9):
            self.criteria_tree.insert("", "end", values=(f"Criterion {i}", "Min" if i % 2 == 0 else "Max"))

        # Scrollbar for the treeview
        criteria_scroll = ttk.Scrollbar(criteria_frame, orient="vertical", command=self.criteria_tree.yview)
        self.criteria_tree.configure(yscroll=criteria_scroll.set)
        criteria_scroll.pack(side="right", fill="y")

        # Add/Delete buttons for Criteria
        button_frame = ttk.Frame(criteria_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Add").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete").pack(side="left", padx=5)

    def setup_values_editor(self):
        # Frame for Values Editor in values_tab
        values_frame = ttk.Frame(self.values_tab)
        values_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for Values List
        self.values_tree = ttk.Treeview(values_frame, columns=[f"Criterion {i}" for i in range(1, 9)], show="headings")
        for i in range(1, 9):
            self.values_tree.heading(f"Criterion {i}", text=f"Criterion {i}")
        self.values_tree.pack(side="left", fill="both", expand=True)

        # Sample values data
        for i in range(1, 12):
            self.values_tree.insert("", "end", values=[f"{i * 1.5:.2f}" for _ in range(8)])

        # Scrollbar for the treeview
        values_scroll = ttk.Scrollbar(values_frame, orient="vertical", command=self.values_tree.yview)
        self.values_tree.configure(yscroll=values_scroll.set)
        values_scroll.pack(side="right", fill="y")

        # Add/Delete buttons for Values
        button_frame = ttk.Frame(values_frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Add").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete").pack(side="left", padx=5)

    def setup_action_controls(self):
        # Bottom section for generation and actions
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=10)

        # Generation options
        ttk.Label(action_frame, text="Distribution:").grid(row=0, column=0, padx=5)
        distribution_combo = ttk.Combobox(action_frame, values=["Exponential", "Normal", "Uniform"])
        distribution_combo.grid(row=0, column=1, padx=5)

        ttk.Label(action_frame, text="Mean:").grid(row=0, column=2, padx=5)
        mean_entry = ttk.Entry(action_frame, width=10)
        mean_entry.grid(row=0, column=3, padx=5)

        ttk.Label(action_frame, text="Object Count:").grid(row=0, column=4, padx=5)
        count_entry = ttk.Entry(action_frame, width=10)
        count_entry.grid(row=0, column=5, padx=5)

        ttk.Button(action_frame, text="Generate").grid(row=0, column=6, padx=5)
        ttk.Button(action_frame, text="Sort").grid(row=0, column=7, padx=5)

        # Algorithm selection and action buttons
        ttk.Label(action_frame, text="Algorithm:").grid(row=1, column=0, padx=5)
        algorithm_combo = ttk.Combobox(action_frame, values=["Naive", "Dominated Points Filtration", "Ideal Point"])
        algorithm_combo.grid(row=1, column=1, padx=5)

        ttk.Button(action_frame, text="Render Animation").grid(row=1, column=2, padx=5)
        ttk.Button(action_frame, text="Stop").grid(row=1, column=3, padx=5)
        ttk.Button(action_frame, text="Benchmark").grid(row=1, column=4, padx=5)
        ttk.Button(action_frame, text="Solve").grid(row=1, column=5, padx=5)

# Initialize the GUI
root = tk.Tk()
gui = GUI(root)
root.mainloop()
