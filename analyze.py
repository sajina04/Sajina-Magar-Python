# Sajina Magar,
# Student number: 32090360
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class employee_app:
    def __init__(self):
        self.window_main = tk.Tk()
        self.window_main.title("Sajina magar , Student ID:32090360")
        self.window_main.geometry("1200x650")

        self.dataset_loaded = None
        self.summary_data = {}

        self.setup_layout()
        self.window_main.mainloop()

    def setup_layout(self):
        container_outer = tk.Frame(self.window_main, bg="black", padx=5, pady=5)
        container_outer.pack(fill='both', expand=True)

        container_main = tk.Frame(container_outer, bg="#7fcdcd")
        container_main.pack(fill='both', expand=True)

        tk.Label(container_main, text="Data Visualization of Nurse Attrition", font=('Arial', 22, 'bold'),pady=5, bg="#badc57", fg="black").pack(fill='x')

        self.build_controls(container_main)

    def build_controls(self, parent_frame):
        section_controls = ttk.Frame(parent_frame, padding=20)
        section_controls.pack(expand=True)

        ttk.Label(section_controls, text="Employee Tools", font=("Arial", 13, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Button(section_controls, text="Load csv", width=25, command=self.load_file).grid(
            row=1, column=0, pady=10, ipadx=5, ipady=7)

        self.button_process = ttk.Button(section_controls, text="Process data", width=25, command=self.process_file)
        self.button_process.grid(row=2, column=0, pady=10, ipadx=5, ipady=7)
        self.button_process['state'] = 'disabled'

        self.button_visuals = ttk.Button(section_controls, text="Show charts", width=25, command=self.show_charts)
        self.button_visuals.grid(row=3, column=0, pady=10, ipadx=5, ipady=7)
        self.button_visuals['state'] = 'disabled'

        self.button_export = ttk.Button(section_controls, text="Export the data", width=25, command=self.export_data)
        self.button_export.grid(row=4, column=0, pady=10, ipadx=5, ipady=7)
        self.button_export['state'] = 'disabled'



