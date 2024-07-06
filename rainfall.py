# Name:Leila Sarkamari
# Lab 2-rainfall-CIS 41B 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def print_return_value(func):
    '''
    A decorator that prints the return value of the function that it decorates
    '''
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        print("Number of data points plotted is:", ret)
        return ret
    return wrapper


class Rainfall:
    '''
    contains data from the input file and methods to analyze and plot the data
    '''
    def __init__(self, filename):
        #defualt filename is "sf_rainfall.csv"
        try:
            
            self.data = np.loadtxt(filename, delimiter=',')
            self.years = self.data[:-1, 0]
            
            self.monthly_rainfall = self.data[0:-1,1:]  # Exclude the last incomplete row and omit year col
            #highest yearly rainfall of all the years
            sorted_index = np.argsort(np.sum(self.monthly_rainfall, axis=1))
            
            max_index = sorted_index[-1]  # Get the index of the maximum sum after sorting
            #self.highest_yearly_rainfall =np.sum(self.monthly_rainfall[max_index])
            self.year_max_rainfall = self.years[max_index] 
            self.highest_yearly_rainfall = np.max(np.sum(self.monthly_rainfall, axis=1))
            
            #lowest yearly rainfall of all the years
            min_index = sorted_index[0]  # Get the index of the min sum after sorting
            #self.lowest_yearly_rainfall=np.sum(self.monthly_rainfall[min_index])
            self.year_min_rainfal = self.years[min_index]              
            self.lowest_yearly_rainfall = np.min(np.sum(self.monthly_rainfall, axis=1))
            # median yearly rainfall of all the years
            self.median_yearly_rainfall = np.median(np.sum(self.monthly_rainfall, axis=1))
            #print("Shape:",self.monthly_rainfall.shape)
           
            
                     
        except FileNotFoundError:
            raise FileNotFoundError("Error:",filename, " not found")
    def get_data(self):
        return self.data
    
    def get_years(self):
        return years
    
    def get_monthly_rainfall(self):
        return self.get_monthly_rainfall
    
    def get_highest_yearly_rainfall(self):
        
        return self.highest_yearly_rainfall
    
    def get_lowest_yearly_rainfall(self):
        return self.lowest_yearly_rainfall

    def get_median_yearly_rainfall(self):
        return self.median_yearly_rainfall
    
    def get_year_max_rainfall(self):
        '''
        calculate the highest year rainfall
        '''
       
        return int(self.year_max_rainfall)
    
    def get_year_min_rainfal(self):
        '''
        calculate the lowest year rainfall
        '''        
        return int(self.year_min_rainfal)
        

    @print_return_value
    def plot_monthly_rainfall_distribution(self):
        '''
        Plot the monthly rainfall distribution.
        '''
       
        Distr_rainfall = self.monthly_rainfall.copy()        
        Distr_rainfall.shape=(2088,) # copy into a 1D array of 174*12
        plt.figure(figsize=(10, 6))
        
        plt.hist(Distr_rainfall, bins=20 ,color='orange', edgecolor='black')
        plt.title('Distribution of Monthly Rainfall in San Francisco',color='blue')
        plt.xlabel('Rainfall (inches)',color='blue')
        plt.ylabel('Frequency',color='blue')
        plt.grid(True)
        plt.show()

        # Return the number of monthly rainfalls being plotted
        
        return len(Distr_rainfall)       
   

    @print_return_value
    def plot_average_monthly_rainfall(self):
        '''
        Plot the average rainfall for each month
        '''
        
        average_rainfall = np.mean(self.monthly_rainfall, axis=0) #average rainfall for each of the 12 months
        months = np.arange(1, 13)
        
        plt.bar(months, average_rainfall,  color='green')
        plt.xticks( months, "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())     
        plt.title('Average Monthly Rainfall',color='blue')
        plt.xlabel('Month',color='blue')
        plt.ylabel('Average Rainfall (inches)',color='blue')
        plt.show()
        return len(average_rainfall)

    @print_return_value
    def plot_yearly_rainfall(self, start_year, end_year):
        '''
        Plot the yearly rainfall for a range of years.Accept 2 input arguments:
        a start year and an end year. You can assume the start and end years
        will be within the valid range of 1850-2023, and that start year < end year.

        '''
        subset = (self.years >= start_year) & (self.years <= end_year)
        years = self.years[subset]
        yearly_rainfall = np.sum(self.monthly_rainfall[subset], axis=1)
        average_yearly_rainfall = np.mean(yearly_rainfall)
        
        plt.plot(years, yearly_rainfall, label='Yearly Rainfall', color='purple')
        plt.plot(years,[average_yearly_rainfall]*len(years), linestyle='--', label='Average Yearly Rainfall',color='blue')
        plt.title('Yearly Rainfall ({0}-{1})'.format(start_year, end_year),color='red')
        plt.xlabel('Year',color='blue')
        plt.ylabel('Rainfall (inches)',color='blue')
        plt.legend()
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.grid(True)
        plt.show()
        
        return len(years)

# Unit Testing

try:
    
    rainfall_data = Rainfall("sf_rainfall.csv")
    print("Highest yearly rainfall and year:", rainfall_data.get_highest_yearly_rainfall(), "in", int(rainfall_data.get_year_max_rainfall()))
    print("Lowest yearly rainfall and year:", rainfall_data.get_lowest_yearly_rainfall(), "in", int(rainfall_data.get_year_min_rainfal()))
    
    print("Median yearly rainfall:", rainfall_data.get_median_yearly_rainfall())
    
    rainfall_data.plot_monthly_rainfall_distribution()
    rainfall_data.plot_average_monthly_rainfall()
    rainfall_data.plot_yearly_rainfall(1850, 2023)
 #  rainfall_data.plot_yearly_rainfall(2000, 2013)
except FileNotFoundError as e:
    print(e.strerror,"not found. Default is sf_rainfall.csv")
    