import tkinter as tk
from tkinter import ttk

# Główne okno aplikacji
root = tk.Tk()
root.title("GUI_OW")
root.geometry("800x600")

# Górne przyciski
btn_load = tk.Button(root, text="Wczytaj dane z pliku", command=None)
btn_load.grid(row=0, column=0, padx=10, pady=10)

method_label = tk.Label(root, text="Metoda:")
method_label.grid(row=0, column=1, padx=5)

method_combobox = ttk.Combobox(root, values=["TOPSIS", "UTA_star", "RSN"], state="readonly")
method_combobox.set("TOPSIS")
method_combobox.grid(row=0, column=2, padx=5)

btn_rank = tk.Button(root, text="Stwórz ranking", command=None)
btn_rank.grid(row=0, column=3, padx=10, pady=10)

# Tabele
# Tabela "Alternatywy z kryteriami"
alt_frame = tk.LabelFrame(root, text="Alternatywy z kryteriami")
alt_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

data_table = ttk.Treeview(alt_frame, columns=(1, 2, 3), show="headings", height=5)
data_table.heading(1, text="1")
data_table.heading(2, text="2")
data_table.heading(3, text="3")
data_table.pack(fill="both", expand=True)

# Tabela "Klasy"
classes_frame = tk.LabelFrame(root, text="Klasy")
classes_frame.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

classes_table = ttk.Treeview(classes_frame, columns=(1, 2, 3), show="headings", height=5)
classes_table.heading(1, text="1")
classes_table.heading(2, text="2")
classes_table.heading(3, text="3")
classes_table.pack(fill="both", expand=True)

# Tabela "Stworzony ranking"
ranking_frame = tk.LabelFrame(root, text="Stworzony ranking")
ranking_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

ranking_table = ttk.Treeview(ranking_frame, columns=(1, 2), show="headings", height=5)
ranking_table.heading(1, text="1")
ranking_table.heading(2, text="2")
ranking_table.pack(fill="both", expand=True)

# Ustawienia siatki
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Uruchomienie aplikacji
root.mainloop()