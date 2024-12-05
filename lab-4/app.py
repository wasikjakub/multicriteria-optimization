import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import openpyxl
from algorithms import RSM, Topsis, UtaStar  # Import the TOPSIS algorithm

class RankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Metody oparte o punkt odniesienia")
        self.master.geometry("800x600")
        
        self.data = None  # Store loaded data

        # Top Buttons
        btn_load = tk.Button(master, text="Wczytaj dane z pliku", command=self.load_file)
        btn_load.grid(row=0, column=0, padx=10, pady=10)

        method_label = tk.Label(master, text="Metoda:")
        method_label.grid(row=0, column=1, padx=5)

        self.method_combobox = ttk.Combobox(master, values=["TOPSIS", "UTA_star", "RSN"], state="readonly")
        self.method_combobox.set("TOPSIS")
        self.method_combobox.grid(row=0, column=2, padx=5)

        btn_rank = tk.Button(master, text="Stwórz ranking", command=self.create_ranking)
        btn_rank.grid(row=0, column=3, padx=10, pady=10)

        # "Alternatywy z kryteriami" Table
        alt_frame = tk.LabelFrame(master, text="Alternatywy z kryteriami")
        alt_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.columns = ("Nr alternatywy", "Nazwa alternatywy", "Kryterium 1", "Kryterium 2", "Kryterium 3")
        self.data_table = ttk.Treeview(alt_frame, columns=self.columns, show="headings")

        # Configure columns with dynamic width and stretch
        for col in self.columns:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, anchor="center", stretch=True, width=120)

        # Add Scrollbars
        scroll_y = ttk.Scrollbar(alt_frame, orient="vertical", command=self.data_table.yview)
        scroll_x = ttk.Scrollbar(alt_frame, orient="horizontal", command=self.data_table.xview)
        self.data_table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.data_table.pack(fill="both", expand=True)

        # Placeholder frames
        classes_frame = tk.LabelFrame(master, text="Klasy")
        classes_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.ranking_frame = tk.LabelFrame(master, text="Stworzony ranking")
        self.ranking_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Grid Configuration for Dynamic Resizing
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=1)

        alt_frame.grid_rowconfigure(0, weight=1)
        alt_frame.grid_columnconfigure(0, weight=1)

    def load_file(self):
        try:
            file_path = r"C:\Users\tomis\Desktop\OW\multicriteria-optimization\lab-4\data.xlsx"  # Predefined file path
            print(f"Loading file: {file_path}")
            self.data = np.round(pd.read_excel(file_path), decimals=2)

            # Clear the table before adding new data
            for row in self.data_table.get_children():
                self.data_table.delete(row)

            # Insert data into the table
            for _, row in self.data.iterrows():
                self.data_table.insert("", "end", values=row.tolist())
            print("Data displayed in the table.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {e}")

    def create_ranking(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded.")
            return

        method = self.method_combobox.get()
        if method == "TOPSIS":
            # Extract relevant data
            criteria_data = self.data[["Kryterium 1", "Kryterium 1.1", "Kryterium 2", "Kryterium 3"]].to_numpy()
            criteria_data = np.insert(criteria_data, 1, 0, axis=1)
            print(criteria_data)
            
            daneA = np.array([
                [1, 0, 55, 60, 70],
                [2, 0, 65, 75, 80],
                [3, 0, 50, 65, 60],
                [4, 0, 70, 85, 90],
                [5, 0, 60, 55, 65]
            ])
            print(daneA)
            
            max_min_criteria = np.array([
                [10, 15, 20],  # Minimalne wartości kryteriów
                [70, 85, 90]   # Maksymalne wartości kryteriów
            ])

            # Run TOPSIS algorithm
            topsis = Topsis(criteria_data, max_min_criteria)
            rankings = topsis.licz_topsis()
            print(rankings)

            # Display rankings in "Stworzony ranking" frame
            for widget in self.ranking_frame.winfo_children():
                widget.destroy()  # Clear previous content

            ranking_label = tk.Label(self.ranking_frame, text="Ranking:")
            ranking_label.pack()

            ranking_text = "\n".join(f"Alternatywa {int(rank[0])}: {np.round(rank[1], 2)}" for rank in rankings)
            ranking_display = tk.Label(self.ranking_frame, text=ranking_text)
            ranking_display.pack()
        else:
            print(f"Method {method} is not implemented yet.")

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = RankingApp(root)
    root.mainloop()
