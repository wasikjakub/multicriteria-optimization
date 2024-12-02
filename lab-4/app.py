import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import openpyxl

def load_file():
    try:
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Excel Files", "*.xls *.xlsx"), ("All Files", "*.*")]
        )
        if file_path:
            print(f"File selected: {file_path}")
            data = pd.read_excel(file_path)

            for row in data_table.get_children():
                data_table.delete(row)

            for _, row in data.iterrows():
                data_table.insert("", "end", values=row.tolist())
            print("Data displayed in the table.")
        else:
            print("No file selected.")
    except Exception as e:
        print(f"Error loading file: {e}")

# Placeholder for additional functionalities
def create_ranking():
    print("Create ranking functionality is not implemented yet.")

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

btn_rank = tk.Button(root, text="Stwórz ranking", command=create_ranking)  # Placeholder command
btn_rank.grid(row=0, column=3, padx=10, pady=10)

# "Alternatywy z kryteriami" Table
alt_frame = tk.LabelFrame(root, text="Alternatywy z kryteriami")
alt_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

columns = ("Nr alternatywy", "Nazwa alternatywy", "Kryterium 1", "Kryterium 2", "Kryterium 3")
data_table = ttk.Treeview(alt_frame, columns=columns, show="headings")

for col in columns:
    data_table.heading(col, text=col)
    data_table.column(col, anchor="center")

data_table.pack(fill="both", expand=True)

# Placeholder frames and functionalities
classes_frame = tk.LabelFrame(root, text="Klasy")
classes_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

ranking_frame = tk.LabelFrame(root, text="Stworzony ranking")
ranking_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

# Grid Configuration for Dynamic Resizing
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)

alt_frame.grid_rowconfigure(0, weight=1)
alt_frame.grid_columnconfigure(0, weight=1)

# Run the Application
root.mainloop()