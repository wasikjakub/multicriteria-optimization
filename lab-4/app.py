import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd

def load_file():
    try:
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Excel Files", "*.xls *.xlsx"),  # Correct format for file extensions
                       ("All Files", "*.*")]  # Catch-all for all files
        )
        if file_path:
            print(f"File selected: {file_path}")
            data = pd.read_excel(file_path)
            print("Data loaded successfully.")
            
            # Clear the data table
            for row in data_table.get_children():
                data_table.delete(row)
            
            # Populate the "Alternatywy z kryteriami" table with data
            for index, row in data.iterrows():
                # Assuming the data contains columns corresponding to the headings
                data_table.insert("", "end", values=row.tolist())
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error: {e}")

# Main Application Window
root = tk.Tk()
root.title("Metody oparte o punkt odniesienia")
root.geometry("800x600")

# Top Buttons
btn_load = tk.Button(root, text="Wczytaj dane z pliku", command=load_file)
btn_load.grid(row=0, column=0, padx=10, pady=10)

method_label = tk.Label(root, text="Metoda:")
method_label.grid(row=0, column=1, padx=5)

method_combobox = ttk.Combobox(root, values=["TOPSIS", "UTA_star", "RSN"], state="readonly")
method_combobox.set("TOPSIS")
method_combobox.grid(row=0, column=2, padx=5)

btn_rank = tk.Button(root, text="Stwórz ranking", command=None)  # Placeholder command
btn_rank.grid(row=0, column=3, padx=10, pady=10)

# "Alternatywy z kryteriami" Table
alt_frame = tk.LabelFrame(root, text="Alternatywy z kryteriami")
alt_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

data_table = ttk.Treeview(alt_frame, columns=("A", "B", "C", "D"), show="headings")
data_table.heading("A", text="Nr alternatywy")
data_table.heading("B", text="Nazwa alternatywy")
data_table.heading("C", text="Kryterium 1")
data_table.heading("D", text="Kryterium 2")
data_table.pack(fill="both", expand=True)

# "Klasy" Table
classes_frame = tk.LabelFrame(root, text="Klasy")
classes_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

classes_table = ttk.Treeview(classes_frame, columns=("A", "B", "C", "D"), show="headings")
classes_table.heading("A", text="Nr klasy")
classes_table.heading("B", text="x")
classes_table.heading("C", text="y")
classes_table.heading("D", text="z")
classes_table.pack(fill="both", expand=True)

# "Stworzony ranking" Table
ranking_frame = tk.LabelFrame(root, text="Stworzony ranking")
ranking_frame.grid(row=2, column=0, columnspan=4, padx=100, pady=100, sticky="nsew")

ranking_table = ttk.Treeview(ranking_frame, columns=(1, 2), show="headings", height=5)
ranking_table.heading(1, text="1")
ranking_table.heading(2, text="2")
ranking_table.pack(fill="both", expand=True)

# Grid Configuration for Dynamic Resizing
root.grid_rowconfigure(1, weight=1)  # Allow row 1 to expand vertically
root.grid_rowconfigure(2, weight=1)  # Allow row 2 to expand vertically
root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
root.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally
root.grid_columnconfigure(2, weight=1)  # Allow column 2 to expand horizontally
root.grid_columnconfigure(3, weight=1)  # Allow column 3 to expand horizontally

alt_frame.grid_rowconfigure(0, weight=1)  # Ensure the Treeview inside expands
alt_frame.grid_columnconfigure(0, weight=1)

classes_frame.grid_rowconfigure(0, weight=1)  # Ensure the Treeview inside expands
classes_frame.grid_columnconfigure(0, weight=1)

ranking_frame.grid_rowconfigure(0, weight=1)  # Ensure the Treeview inside expands
ranking_frame.grid_columnconfigure(0, weight=1)

# Run the Application
root.mainloop()