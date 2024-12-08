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

        self.method_combobox = ttk.Combobox(master, values=["TOPSIS", "UTA_star", "RSM"], state="readonly")
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

        # Replace this part in the __init__ method where the ranking_frame is created
        self.ranking_canvas = tk.Canvas(master)
        self.ranking_scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.ranking_canvas.yview)
        self.ranking_frame = tk.Frame(self.ranking_canvas)

        self.ranking_canvas.create_window((0, 0), window=self.ranking_frame, anchor="nw")
        self.ranking_canvas.configure(yscrollcommand=self.ranking_scrollbar.set)

        self.ranking_scrollbar.grid(row=2, column=3, sticky="ns")
        self.ranking_canvas.grid(row=2, column=2, sticky="nsew")

        self.ranking_frame.bind("<Configure>", lambda e: self.ranking_canvas.configure(scrollregion=self.ranking_canvas.bbox("all")))

        # Add a placeholder label for the ranking box
        ranking_label = tk.Label(self.ranking_frame, text="Stworzony Ranking:", font=("Arial", 12, "bold"))
        ranking_label.pack(pady=5)

        placeholder_label = tk.Label(self.ranking_frame, text="Brak danych do wyświetlenia.", justify="left", fg="gray")
        placeholder_label.pack(pady=5)


        # Add to __init__
        self.classes_data = {
            "Fu_ref": np.array([
                [15, 5, 5],
                [20, 10, 10],
                [10, 40, 50],
                [30, 20, 0],
                [15, 15, 15]
            ]),
            "max_min_criteria": np.array([
                [10, 15, 20],
                [70, 85, 90]
            ]),
            "pref": np.array([10, 25, 0]),
            "pref_two": np.array([25, 40, 10]) 
        }

        self.classes_entries = {}

        # Add fields for Fu_ref
        fu_ref_label = tk.Label(classes_frame, text="Fu_ref:")
        fu_ref_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        for i, row in enumerate(self.classes_data["Fu_ref"]):
            self.classes_entries[f"Fu_ref_row_{i}"] = []
            for j, value in enumerate(row):
                entry = ttk.Entry(classes_frame, width=10)
                entry.insert(0, str(value))
                entry.grid(row=i + 1, column=j, padx=5, pady=5)
                self.classes_entries[f"Fu_ref_row_{i}"].append(entry)

        # Add fields for max_min_criteria
        max_min_label = tk.Label(classes_frame, text="Min/Max Criteria:")
        max_min_label.grid(row=len(self.classes_data["Fu_ref"]) + 2, column=0, padx=5, pady=5, sticky="w")

        for i, row in enumerate(self.classes_data["max_min_criteria"]):
            self.classes_entries[f"max_min_row_{i}"] = []
            for j, value in enumerate(row):
                entry = ttk.Entry(classes_frame, width=10)
                entry.insert(0, str(value))
                entry.grid(row=len(self.classes_data["Fu_ref"]) + 3 + i, column=j, padx=5, pady=5)
                self.classes_entries[f"max_min_row_{i}"].append(entry)
                
        # Add fields for pref
        pref_label = tk.Label(classes_frame, text="Pref:")
        pref_label.grid(row=len(self.classes_data["Fu_ref"]) + 5, column=0, padx=5, pady=5, sticky="w")

        self.classes_entries["pref"] = []
        for i, value in enumerate(self.classes_data["pref"]):
            entry = ttk.Entry(classes_frame, width=10)
            entry.insert(0, str(value))
            entry.grid(row=len(self.classes_data["Fu_ref"]) + 6, column=i, padx=5, pady=5)
            self.classes_entries["pref"].append(entry)

        # Add fields for pref_two
        pref_two_label = tk.Label(classes_frame, text="Pref Two:")
        pref_two_label.grid(row=len(self.classes_data["Fu_ref"]) + 7, column=0, padx=5, pady=5, sticky="w")

        self.classes_entries["pref_two"] = []
        for i, value in enumerate(self.classes_data["pref_two"]):
            entry = ttk.Entry(classes_frame, width=10)
            entry.insert(0, str(value))
            entry.grid(row=len(self.classes_data["Fu_ref"]) + 8, column=i, padx=5, pady=5)
            self.classes_entries["pref_two"].append(entry)


        # Grid Configuration for Dynamic Resizing
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=1)

        alt_frame.grid_rowconfigure(0, weight=1)
        alt_frame.grid_columnconfigure(0, weight=1)

    def get_classes_data(self):
    # Extract Fu_ref values
        Fu_ref = []
        for i in range(len(self.classes_data["Fu_ref"])):
            row = [float(entry.get()) for entry in self.classes_entries[f"Fu_ref_row_{i}"]]
            Fu_ref.append(row)
        Fu_ref = np.array(Fu_ref)

        # Extract max_min_criteria values
        max_min_criteria = []
        for i in range(len(self.classes_data["max_min_criteria"])):
            row = [float(entry.get()) for entry in self.classes_entries[f"max_min_row_{i}"]]
            max_min_criteria.append(row)
        max_min_criteria = np.array(max_min_criteria)
        
        pref = np.array([float(entry.get()) for entry in self.classes_entries["pref"]])
        pref_two = np.array([float(entry.get()) for entry in self.classes_entries["pref_two"]])

        return Fu_ref, max_min_criteria, pref, pref_two

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

        # Extract Fu_ref and max_min_criteria from GUI
        Fu_ref, max_min_criteria, pref, pref_two = self.get_classes_data()

        if method == "TOPSIS":
            # Extract relevant data
            criteria_data = self.data[["Nr alternatywy", "Kryterium 1", "Kryterium 2", "Kryterium 3"]].to_numpy()
            criteria_data = np.insert(criteria_data, 1, 0, axis=1)

            # Run TOPSIS algorithm with user-provided max_min_criteria
            topsis = Topsis(criteria_data, max_min_criteria)
            rankings = topsis.licz_topsis()
            rankings = rankings[rankings[:, 1].argsort()[::-1]]

            # Display rankings in the "Ranking" box
            for widget in self.ranking_frame.winfo_children():
                widget.destroy()  # Clear previous content

            ranking_label = tk.Label(self.ranking_frame, text="Stworzony Ranking:", font=("Arial", 12, "bold"))
            ranking_label.pack(pady=5)

            ranking_text = "\n".join(f"Alternatywa {int(rank[0])}: {np.round(rank[1], 2)}" for rank in rankings)
            ranking_display = tk.Label(self.ranking_frame, text=ranking_text, justify="left")
            ranking_display.pack(pady=5)

        elif method == "UTA_star":
            Fu = self.data[["Kryterium 1", "Kryterium 2", "Kryterium 3"]].to_numpy()

            # Run UTA* algorithm with user-provided Fu_ref
            utastar = UtaStar(Fu, Fu_ref)
            U, _, ranking = utastar.UTASTAR()

            # Display rankings in the "Stworzony Ranking" frame
            for widget in self.ranking_frame.winfo_children():
                widget.destroy()  # Clear previous content

            ranking_label = tk.Label(self.ranking_frame, text="Stworzony Ranking:", font=("Arial", 12, "bold"))
            ranking_label.pack(pady=5)

            rankings = []
            for i in range(len(U)):
                rankings.append((U[i], ranking[i]))
            rankings.sort(key=lambda x: x[1])

            ranking_text = "\n".join(f"Alternatywa {int(rank[1])}: {np.round(rank[0], 2)}" for rank in rankings)
            ranking_display = tk.Label(self.ranking_frame, text=ranking_text, justify="left")
            ranking_display.pack(pady=5)

        elif method == "RSM":
            data = self.data[["Kryterium 1", "Kryterium 2", "Kryterium 3"]].to_numpy()
            
            rsm = RSM(data, pref, pref_two)
            rankings = np.unique(rsm.determine_sets(), axis=0)
            
            for widget in self.ranking_frame.winfo_children():
                widget.destroy()  # Clear previous content

            ranking_label = tk.Label(self.ranking_frame, text="Stworzony Ranking:", font=("Arial", 12, "bold"))
            ranking_label.pack(pady=5)
            
            ranking_text = "\n".join(f"Alternatywa: {str(rank)}" for _, rank in enumerate(rankings))
            ranking_display = tk.Label(self.ranking_frame, text=ranking_text, justify="left")
            ranking_display.pack(pady=5)
            
        else:
            print(f"Method {method} is not implemented yet.")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = RankingApp(root)
    root.mainloop()
