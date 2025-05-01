import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class employee_app:
    def __init__(self):
        self.window_main = tk.Tk()
        self.window_main.title("Sajina magar , Student ID:3010029")
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

    def load_file(self):
        try:
            self.dataset_loaded = pd.read_csv('nurse_attrition (1).csv')
            messagebox.showinfo("Data","Data loaded successfully")
            self.button_process['state'] = 'normal'
        except Exception as error:
            messagebox.showerror("Error", f"couldn’t load file:\n{error}")

    def process_file(self):
        if self.dataset_loaded is None:
            messagebox.showerror("oops", "load the file first")
            return

        df = self.dataset_loaded

        self.summary_data = {
            'total': len(df),
            'dept_names': df['Department'].unique().tolist(),
            'dept_count': df['Department'].value_counts().to_dict(),
            'gender_count': df['Gender'].value_counts().to_dict(),
            'age_stats': {
                'min': df['Age'].min(),
                'max': df['Age'].max(),
                'avg': round(df['Age'].mean(), 1)
            },
            'distance_stats': {
                'min': df['DistanceFromHome'].min(),
                'max': df['DistanceFromHome'].max(),
                'avg': round(df['DistanceFromHome'].mean(), 1)
            },
            'rate_stats': {
                'min': df['HourlyRate'].min(),
                'max': df['HourlyRate'].max(),
                'avg': round(df['HourlyRate'].mean(), 1)
            },
            'marriage_status': df['MaritalStatus'].value_counts(normalize=True).mul(100).round(1).to_dict(),
            'balance_score': round(df['WorkLifeBalance'].mean(), 1),
            'attrition_yes': df['Attrition'].value_counts().get('Yes', 0)
        }

        self.button_visuals['state'] = 'normal'
        self.button_export['state'] = 'normal'
        self.show_summary()

    def show_summary(self):
        window_summary = tk.Toplevel(self.window_main)
        window_summary.title("summary")

        text_summary = tk.Text(window_summary, wrap='word')
        text_summary.pack(fill='both', expand=True)

        s = self.summary_data
        summary_text = f"""summary:
total employees: {s['total']}

departments: {', '.join(s['dept_names'])}
department counts:
"""
        for dept, count in s['dept_count'].items():
            summary_text += f"- {dept}: {count}\n"

        summary_text += f"""
gender:
- male: {s['gender_count'].get('Male', 0)}
- female: {s['gender_count'].get('Female', 0)}

age:
- min: {s['age_stats']['min']}
- max: {s['age_stats']['max']}
- avg: {s['age_stats']['avg']}

distance from home:
- min: {s['distance_stats']['min']}
- max: {s['distance_stats']['max']}
- avg: {s['distance_stats']['avg']}

hourly rate:
- min: {s['rate_stats']['min']}
- max: {s['rate_stats']['max']}
- avg: {s['rate_stats']['avg']}

marital status (%):
"""
        for status, percent in s['marriage_status'].items():
            summary_text = summary_text + f"- {status}: {percent}%\n"

        summary_text = summary_text + f"\n Work-life balance (avg): {s['balance_score']}/4 \n Gone: {s['attrition_yes']}"
        text_summary.insert('end', summary_text)
        text_summary.config(state='disabled')

    def show_charts(self):
        if self.dataset_loaded is None:
            messagebox.showerror("Error"," Load file first")
            return

        chart_menu = tk.Toplevel(self.window_main)
        chart_menu.title("charts")

        ttk.Button(chart_menu, text="Pie chart of Department", command=self.plot_dept_chart).pack(fill='x', pady=5)
        ttk.Button(chart_menu, text="Marriage Bar Graph", command=self.plot_marriage_chart).pack(fill='x', pady=5)
        ttk.Button(chart_menu, text="Dashboard", command=self.plot_dashboard).pack(fill='x', pady=5)

    def plot_dept_chart(self):
        chart_window = self.create_chart_window("Department chart")
        fig, axis = plt.subplots(figsize=(8, 6))
        self.dataset_loaded['Department'].value_counts().plot.pie(autopct='%1.1f%%', ax=axis)
        axis.set_ylabel('')
        FigureCanvasTkAgg(fig, chart_window).get_tk_widget().pack()

    def plot_marriage_chart(self):
        chart_window = self.create_chart_window("Marital status chart")
        fig, axis = plt.subplots(figsize=(8, 6))
        self.dataset_loaded['MaritalStatus'].value_counts().plot.bar(ax=axis, color='skyblue')
        axis.set_xlabel('status')
        axis.set_ylabel('count')
        axis.tick_params(axis='x', rotation=45)
        FigureCanvasTkAgg(fig, chart_window).get_tk_widget().pack()

    def plot_dashboard(self):
        if self.dataset_loaded is None or not self.summary_data:
            messagebox.showerror("Error","process the data first")
            return

        dashboard_window = self.create_chart_window("Dashboard")
        fig = plt.Figure(figsize=(12, 6))

        axis1 = fig.add_subplot(2, 2, 1)
        self.dataset_loaded['Department'].value_counts().plot.pie(autopct='%1.1f%%', ax=axis1)
        axis1.set_title("departments")
        axis1.set_ylabel('')

        axis2 = fig.add_subplot(2, 2, 2)
        self.dataset_loaded['MaritalStatus'].value_counts().plot.bar(ax=axis2, color='lightgreen')
        axis2.set_title("marital status")
        axis2.tick_params(axis='x', rotation=45)

        axis3 = fig.add_subplot(2, 1, 2)
        axis3.axis('off')
        s = self.summary_data
        info_text = f"""
Total: {s['total']}
Department Name : {', '.join(s['dept_names'])}
Average age: {s['age_stats']['avg']}
Attrition: {s['attrition_yes']}
Average rate: ${s['rate_stats']['avg']}
Balance: {s['balance_score']}/4
"""
        axis3.text(0, 0.8, info_text.strip(), fontsize=12, verticalalignment='top')

        chart_canvas = FigureCanvasTkAgg(fig, dashboard_window)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill='both', expand=True)

    def create_chart_window(self, title_text):
        new_window = tk.Toplevel(self.window_main)
        new_window.title(title_text)
        return new_window

    def export_data(self):
        try:
            self.dataset_loaded.to_csv("processed_employee_data.csv", index=False)
            messagebox.showinfo("done", "file exported successfully")
        except Exception as error:
            messagebox.showerror("fail", f"couldn’t export:\n{error}")

run = employee_app()

