# Name:Leila Sarkamari
# Lab 2-CIS 41B 
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from rainfall import Rainfall

class MainWindow(tk.Tk):
    '''
    The main window is an object of the main window class,and it appears when the app first comes up.
    '''
    def __init__(self, rainfall_data):
        super().__init__()
        self.rainfall_data = rainfall_data
        self.title("Rainfall Analysis App")
        self.minyear=int(min(self.rainfall_data.years))
        self.maxyear=int(max(self.rainfall_data.years))
        explanation = "SF Rainfall "+str(self.minyear)+"-"+str(self.maxyear)
        self.explanation_label = tk.Label(self, text=explanation, fg="green")
        self.explanation_label.grid(row=0,column=2,sticky=tk.N)
        
        self.monthly_button = tk.Button(self, text="Monthly Average", command=self.show_monthly_average)
        self.monthly_button.grid(row=1,column=1,sticky=tk.W)
        self.distribution_button = tk.Button(self, text="Monthly Distribution", command=self.show_monthly_distribution)
        self.distribution_button.grid(row=1,column=2,sticky=tk.N)
        self.yearly_button = tk.Button(self, text="Yearly Total", command=self.yearly_range)
        self.yearly_button.grid(row=1,column=3,sticky=tk.E)
        
        self.statistics_label = tk.Label(self, text="Yearly Statistics:")
        self.statistics_label.grid(row=2,column=2)
        self.highest_label = tk.Label(self, text=f"Highest Yearly Rainfall: {rainfall_data.highest_yearly_rainfall:.2f} in {rainfall_data.get_year_max_rainfall()}")
        self.highest_label.grid(row=3,column=2)
        self.lowest_label = tk.Label(self, text=f"Lowest Yearly Rainfall: {rainfall_data.lowest_yearly_rainfall:.2f} in {rainfall_data.get_year_min_rainfal()}")
        self.lowest_label.grid(row=4,column=2)
        self.median_label = tk.Label(self, text=f"Median Yearly Rainfall: {rainfall_data.median_yearly_rainfall:.2f}")
        self.median_label.grid(row=5,column=2)
        
    def show_monthly_average(self):
        plot_window = PlotWindow(self)
        plot_window.plot(self.rainfall_data.plot_average_monthly_rainfall)

    def show_monthly_distribution(self):
        plot_window = PlotWindow(self)
        plot_window.plot(self.rainfall_data.plot_monthly_rainfall_distribution)


    def yearly_range(self):

        #self.grab_set()  # Disable other windows
        dialog = DialogWindow(self)        
        self.wait_window(dialog)
        range_years = dialog.get_range_years()
        #self.grab_release()  # Re-enable other windows

        if range_years:
            start_year, end_year = range_years
            if range_years:
                start_year, end_year = range_years
                #plot_window = PlotWindow(self)
                #plot_window.plot(lambda: self.rainfall_data.plot_yearly_rainfall(start_year, end_year))                
                #PlotWindow(self,self.rainfall_data.plot_yearly_rainfall(start_year, end_year))
                PlotWindow(lambda: self.rainfall_data.plot_yearly_rainfall(start_year, end_year))                
            

class PlotWindow(tk.Toplevel):
    '''
    The plot window is an object of the plot window class. The plot window is created by the main window
    '''
    def __init__(self, master):
        super().__init__(master)
        self.title("Rainfall Plot")
        self.plot_frame = tk.Frame(self)
        self.plot_frame.pack()
    
    def plot(self, plot_function):
        plot_function()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

class DialogWindow(tk.Toplevel):
    '''
    The dialog window is an object of the dialog window class. The window is created by the main window when the user selects the ‘Yearly Total’ button.
    '''
    def __init__(self, master):
        super().__init__(master)
        self.title("Yearly Range Input")
        self.prompt_label = tk.Label(self, text="Enter a range of years (e.g., 2000 2010):")
        self.prompt_label.pack()
        self.entry = tk.Entry(self)
        self.entry.pack()
        self.ok_button = tk.Button(self, text="OK", command=self.validate_input)
        self.ok_button.pack()
    def validate_input(self):
        input_years = self.entry.get()
        if not input_years:
            messagebox.showinfo("Empty Input", "Please enter two valid 4-digit years separated by space.")
            return None
    
        years = input_years.split()
        if len(years) != 2:
            messagebox.showinfo("Invalid Input", "Please enter two valid 4-digit years separated by space.")
            return None
    
        try:
            start_year = int(years[0])
            end_year = int(years[1])
            if start_year < min(self.master.rainfall_data.years) or end_year > max(self.master.rainfall_data.years) or start_year >= end_year:
                messagebox.showinfo("Invalid Range", f"The range entered is invalid. Using full range from {int(min(self.master.rainfall_data.years))} to {int(max(self.master.rainfall_data.years))}.")
                return int(min(self.master.rainfall_data.years)),int(max(self.master.rainfall_data.years))
            else:
                self.destroy()
                return start_year, end_year
        except ValueError:
            messagebox.showinfo("Invalid Input", "Please enter two valid 4-digit years separated by space.")

    def get_range_years(self):
        return self.validate_input()    

try:
    rainfall_data = Rainfall("sf_rainfall.csv")
    app = MainWindow(rainfall_data)
    app.mainloop()
except FileNotFoundError as e:
    messagebox.showerror("File Open Error", f"Unable to open file: {e.filename}.")
    app.quit()


