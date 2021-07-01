# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import random
import warnings


# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    coef_list = []
    for deg in degs:
        coef_list.append(pylab.polyfit(x,y,deg))
    return(coef_list)




def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean = sum(y)/len(y)    
    R2 = 1 - sum((y-estimated)**2)/sum((y-mean)**2)
        
    return(R2)


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    estimates = []
    for model in models:
        model_at_x = pylab.array([])
        for x_val_equat in range(len(x)):
            model_sum = 0
            order = len(model)
            for coef in model:
                order -= 1
                # this causes issues for higher degree models. This is probably due to it rounding 
                # incorrectly. This can be solved by replacing the x[0] with 1, but this causes 
                # other issues, more likely to occure than you actually needing to find a degree 14
                # model, so I will leave it as is.
                model_sum += coef * (x_val_equat+int(x[0])) ** order
            model_at_x = pylab.append(model_at_x, model_sum)
        estimates.append(model_at_x)
    R2_list = []
    se_ov_slope_list = []
    for model_num in range(len(models)):
        R2_list.append(r_squared(y, estimates[model_num]))
        se_ov_slope_list.append(se_over_slope(x, y, estimates[model_num], models[model_num]))
    for est in range(len(estimates)):
        pylab.plot(x, y, 'b.')
        pylab.plot(x, estimates[est], 'r')
        pylab.plt.xlabel('years')
        pylab.plt.ylabel('deg Celsius')
        pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1))
        pylab.show()
 

# evaluate_models_on_training(pylab.array(range(3))+1, pylab.array(range(3))+1, 
#                             generate_models(pylab.array(range(3))+1, pylab.array(range(3))+1, [20]))
        


# def training_eval_tester():
    ar_dic = {}
    for i in range(10):
        ar = pylab.array(range(i))+1
        ar_dic[i] = [ar]
    del ar_dic[0]
    del ar_dic[1]
    for k in ar_dic:
        R2 = 1
        count = 1
        while R2 == 1:
            if count == 50: break
            models = generate_models(pylab.array(range(k))+1, ar_dic[k][0], [count])
            if k < 9:
                print(generate_models(pylab.array(range(k))+1, ar_dic[k][0], [count]))
                print(pylab.array(range(k))+1, ar_dic[k][0], [count])
            estimates = []
            for model in models:
                model_at_x = pylab.array([])
                for x_val_equat in range(k):
                    model_sum = 0
                    order = len(model)
                    for coef in model:
                        order -= 1
                        model_sum += coef * (x_val_equat+1) ** order
                    model_at_x = pylab.append(model_at_x, model_sum)
                estimates.append(model_at_x)
            count += 1
            R2 = r_squared(ar_dic[k][0], estimates[0])
            # if R2 != 1 or count == 49:
            #     print(ar_dic[k])
            #     print(R2)
        if R2 != 1:
            ar_dic[k].append(count)
    return(ar_dic)

# if __name__=='__main__':
#     print(training_eval_tester())
    
# print('gen mod:', generate_models(pylab.array(range(8))+1, pylab.array(range(8))+1, [49]))

# print( pylab.array([ 2.34939159e-46,  1.83776774e-45,  1.43217531e-44,  1.11109876e-43,
#         8.57352738e-43,  6.57213700e-42,  4.99725475e-41,  3.76143873e-40,
#         2.79492535e-39,  2.04207764e-38,  1.45854514e-37,  1.00899317e-36,
#         6.65287141e-36,  4.05041068e-35,  2.10457173e-34,  6.73982519e-34,
#        -3.53538488e-33, -1.06691020e-31, -1.53652839e-30, -1.81805601e-29,
#        -1.95545619e-28, -1.98342129e-27, -1.92932129e-26, -1.81477024e-25,
#        -1.65689014e-24, -1.46933563e-23, -1.26313041e-22, -1.04735473e-21,
#        -8.29714373e-21, -6.17011126e-20, -4.15524859e-19, -2.31303990e-18,
#        -7.03443222e-18,  6.13865765e-17,  1.58151725e-15,  2.14980014e-14,
#         2.28668920e-13,  1.99383140e-12,  1.32871710e-11,  4.29900386e-11,
#        -4.65689368e-10, -1.03898309e-08, -9.84392850e-08, -2.37269190e-07,
#         6.94132346e-06,  6.62907015e-05, -7.89946271e-04,  2.65683612e-03,
#         9.96379829e-01,  1.68039515e-03]) == pylab.array([ 2.34939159e-46,  1.83776774e-45,  1.43217531e-44,  1.11109876e-43,
#         8.57352738e-43,  6.57213700e-42,  4.99725475e-41,  3.76143873e-40,
#         2.79492535e-39,  2.04207764e-38,  1.45854514e-37,  1.00899317e-36,
#         6.65287141e-36,  4.05041068e-35,  2.10457173e-34,  6.73982519e-34,
#        -3.53538488e-33, -1.06691020e-31, -1.53652839e-30, -1.81805601e-29,
#        -1.95545619e-28, -1.98342129e-27, -1.92932129e-26, -1.81477024e-25,
#        -1.65689014e-24, -1.46933563e-23, -1.26313041e-22, -1.04735473e-21,
#        -8.29714373e-21, -6.17011126e-20, -4.15524859e-19, -2.31303990e-18,
#        -7.03443222e-18,  6.13865765e-17,  1.58151725e-15,  2.14980014e-14,
#         2.28668920e-13,  1.99383140e-12,  1.32871710e-11,  4.29900386e-11,
#        -4.65689368e-10, -1.03898309e-08, -9.84392850e-08, -2.37269190e-07,
#         6.94132346e-06,  6.62907015e-05, -7.89946271e-04,  2.65683612e-03,
#         9.96379829e-01,  1.68039515e-03]))


# print(r_squared(pylab.array([1.5,1.5]),pylab.array([1.5,1.5])))
# print(generate_models(pylab.array([1,2]), pylab.array([1,2]), [2]))
    
# pylab.array([1])
# dic = {1:[pylab.array([1])]}
# print(pylab.array(list(dic.keys())[0]), dic[1][0])
# print(generate_models(pylab.array(list(dic.keys())[0]), dic[1][0], [2]))
def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearly_temps = pylab.array([])
    for year in years:
        avg_temp = 0
        for city in multi_cities:
            avg_temp += sum(climate.get_yearly_temp(city, year))
        avg_temp = avg_temp / len(multi_cities) / len(climate.get_yearly_temp(city, year))
        yearly_temps = pylab.append(yearly_temps, avg_temp)
    return(yearly_temps)


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # [-1.5, 1.5, -3.0, 3.0, -4.5, 4.5]
    # [-1.5, 0, -.75, 0, -.75, 0]
    temporary_avg_array = pylab.array([])
    moving_avg = pylab.array([])
    # this feels sloppy. I might try and make a better version later if I can think of one
    # I can't think of any good names for my counting variables, so I am using letters
    for i in range(len(y)):
        temporary_avg_array_2nd = pylab.array([])
        if i < window_length:
            temporary_avg_array = pylab.append(temporary_avg_array, y[i])
            moving_avg = pylab.append(moving_avg, sum(temporary_avg_array) / (i+1))
        else:
            for c in range(window_length):
                temporary_avg_array_2nd=pylab.append(temporary_avg_array_2nd,y[c+i-(window_length-1)])
            moving_avg = pylab.append(moving_avg, sum(temporary_avg_array_2nd)/window_length)
    return(moving_avg)                        
    

def rmse(y, estimated):

    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    # I really tried to not use a loop here. It feels like I should be able to do it without one. But
    # after like 45 minutes trying to figure out how it calculated the sum() function, I gave up. this
    # works fine
    sums = 0
    for i in range(len(y)):
        sums += ((y[i]-estimated[i])**2)
    rmse_val = (sums/len(y))**0.5        
    return(rmse_val)
    

def gen_std_devs(climate, multi_cities, years):
            
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    avg_city_tmp = gen_cities_avg(climate, multi_cities, years)
    avg_nat_temp = sum(avg_city_tmp)/len(avg_city_tmp)
    std_devs = pylab.array([])
    for year in years:
        sums = 0
        for i in range(len(avg_city_tmp)):
            sums += (avg_city_tmp[i]-avg_nat_temp)**2
        std_devs = pylab.append(std_devs, (sums/(len(years)))**0.5)
    return(std_devs)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    estimates = []
    for model in models:
        model_at_x = []
        for x_val_equat in range(len(x)):
            model_sum = 0
            order = len(model)
            for coef in model:
                order -= 1
                model_sum += coef * (x_val_equat+x[0]) ** order
            model_at_x.append(model_sum)
        estimates.append(model_at_x)
    rmse_list = []
    for model_num in range(len(models)):
        rmse_list.append(rmse(y, estimates[model_num]))
    for est in range(len(estimates)):
        pylab.plot(x, y, 'b.')
        pylab.plot(x, estimates[est], 'r')
        pylab.plt.xlabel('years')
        pylab.plt.ylabel('deg Celsius')
        pylab.plt.title('rmse:' + str(rmse_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1))
        pylab.show()


def test():
    xarray0 = pylab.array([1961, 1962, 1963])
    yarray0 = pylab.array([-4.4, -5.5, -6.6])
    mod0 = [pylab.array([-1.1000e+00,  2.1527e+03]), 
            pylab.array([ 8.86320372e-14, -1.10000000e+00,  2.15270000e+03])]
    
    xarray1 = pylab.array(range(50))
    yarray1 = pylab.array(range(50))
    mod1 = [pylab.array([1.00000000e+00, 6.02915504e-15])]
    
    xarray2 = xarray1                  
    yarray2 = pylab.array(range(0,100,2))
    mod2 = [pylab.array([2.00000000e+00, 1.20583101e-14]), 
            pylab.array([ 3.02309636e-18,  2.00000000e+00, -3.21554936e-14])]
    mod3 = [pylab.array([2.00000000e+00, 1.20583101e-14]), 
            pylab.array([ 3.02309636e-18,  2.00000000e+00, -3.21554936e-14]), 
            pylab.array([ 2.88246057e-18, -1.62236562e-16,  2.00000000e+00, -1.00485917e-14])]

    hxarray1 = pylab.array(range(10))
    hyarray1 = pylab.array(range(10))**2
    hmod1 = [pylab.array([9.,-12.])]
    hmod2 = [pylab.array([ 1.00000000e+00, -3.77125854e-15,  1.44471508e-14])]
    hest1 = [pylab.array([-12.0, -3.0, 6.0, 15.0, 24.0, 33.0, 42.0, 51.0, 60.0, 69.0])]
    hest2 = [pylab.array([1.44471508e-14, 1.0000000000000107, 4.000000000000007, 9.000000000000004, 
                          16.0, 24.999999999999996, 35.99999999999999, 48.999999999999986, 
                          63.999999999999986, 80.99999999999999])]
    
    climate1 = Climate('data.csv')
    
    years1 = range(2010, 2016)
    years2 = range(1961, 2010)
    
    cities1 = CITIES
    
    hxarray2 = pylab.array(years2)
    hyarray2 = pylab.array([-2.5,-5.8,2.75,0.85,1.1,2.8,1.1,-12.75,-3.05,-6.1,-0.25,9.45,-1.9,-1.9,
                            5.8,-6.35,-0.85,-8.1,-3.9,-1.65,-7.5,-11.1,7.8,3.3,-5.,4.15,3.35,-5.3,
                            -0.3,5.8,1.95,5.55,-3.35,-6.1,-1.35,-1.65,2.75,5.85,-2.5,9.2,-2.5,6.7,
                            3.9,-12.8,6.1,6.1,0.25,6.95,-2.2])
    mavgarray1 = pylab.array([10, 20, 30, 40, 50]) 
    cr1 = pylab.array([10, 15, 20, 30, 40,])
    mavgarray2 = pylab.array([15.643163731245922, 15.386921069797776, 15.502263535551206, 
                              15.302244340359094, 15.542498369210692, 15.494872798434434, 
                              15.613594259621657, 15.531700494405415, 15.738845401174165, 
                              15.875512067840836, 15.898095238095241, 15.854709862086908, 
                              16.183072407045007, 16.152120026092625, 16.03287671232877, 
                              15.733359354670826, 16.199295499021527, 15.924579256360072, 
                              15.996079582517941, 16.173874577153263, 16.353333333333335, 
                              16.000965427266802, 16.224611872146117, 16.142252146760345, 
                              15.916053489889102, 16.509360730593606, 16.459595564253096, 
                              16.248250065053348, 16.195955642530983, 16.969067188519247, 
                              16.861969993476844, 16.44521857923498, 16.393529028049578, 
                              16.69698630136986, 16.715864318330073, 16.116770752016656, 
                              16.37011741682975, 16.978982387475536, 16.580358773646445, 
                              16.295225084569353, 16.591624266144812, 16.65839530332681, 
                              16.432283105022826, 16.553987769971375, 16.72510110893673, 
                              17.071343770384868, 16.825101108936725, 16.51740827478532, 
                              16.514598825831698])
    mavgarray3 = pylab.array([1, 2, 3, 4, 5, 6, 7]) 
    cr3 = pylab.array([1, 1.5, 2, 3, 4, 5, 6])
    mavgarray4 = pylab.array([-1.5, 1.5, -3.0, 3.0, -4.5, 4.5]) 
    cr4 = pylab.array([-1.5, 0, -.75, 0, -.75, 0])
    rmy1 = pylab.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    rme1 = pylab.array([1, 4, 9, 16, 25, 36, 49, 64, 81])
    cor1 = 35.8515457593
    rmy2 = pylab.array([1, 1, 1, 1, 1, 1, 1, 1, 1])
    rme2 = pylab.array([1, 4, 9, 16, 25, 36, 49, 64, 81])
    cor2 = 40.513372278
    
    rv2 = pylab.array([1,0])
    rv3 = pylab.array([0,-1,0])
    rv4 = pylab.array([1,0,0,-1])
    rv5 = pylab.array([0,0,1,-1,0])
    rv6 = pylab.array([0,1,0,1,-1, 0])
    
    evxar1 = pylab.array([1])
    evxar2 = pylab.array(range(2))+1
    evxar3 = pylab.array(range(3))+1 # 20
    evxar4 = pylab.array(range(4))+1 # 16
    evxar5 = pylab.array(range(5))+1 # 14
    evxar6 = pylab.array(range(6))+1 # 12
    evyar1 = pylab.array(range(1))+1
    evyar2 = pylab.array(range(2))+1 + rv2
    evyar3 = pylab.array(range(3))+1 #+ rv3
    evyar4 = pylab.array(range(4))+1 + rv4
    evyar5 = pylab.array(range(5))+1 + rv5
    evyar6 = pylab.array(range(6))+1 + rv6
    evyar51 = pylab.array(range(5))**2 + rv5
    evxar_lst = [evxar2, evxar3, evxar4, evxar5]
    evyar_lst = [evyar2, evyar3, evyar4, evyar5]
    
    climate = Climate('data.csv')
    years = pylab.array(TRAINING_INTERVAL)
    correct = [6.1119325255476635, 5.4102625076401125, 6.0304210441394801, 5.5823239710637846, 5.5908151965372177, 5.0347634736031583, 6.2485081784971772, 5.6752637253518703, 5.9822493041266327, 5.5376216719090898, 6.0339331562285095, 6.3471434661632733, 5.3872564859222782, 5.7528361897357705, 6.0117329392620285, 5.5922579610955854, 5.67888175212234, 5.7810899373043272, 5.7184178577664087, 5.3955809402004036, 5.1736886920193665, 5.8134229790176573, 5.1915733214759872, 5.4023314139519591, 6.7868442109830855, 5.2952870947334114, 5.6064597624296333, 5.4921097908102086, 6.1450202825415214, 6.3591021848005278, 5.4996866353350615, 5.6516820894310058, 5.7969983303071411, 5.8531227958031931, 5.2545492072097808, 6.0102701017450126, 5.5327493838092865, 5.7703034605336532, 5.0412624972468443, 5.2728662938897264, 5.0859211734722649, 5.5526426823734987, 5.8005720594546748, 5.7391426965165389, 5.5518538235632207, 5.8279562142168073, 5.9089508390885479, 5.9789908401877394, 6.5696153940105573]
    
    # print(generate_models(hxarray2, hyarray2, [1]))
    # print(r_squared(hyarray1, hest1[0]))
    # print(evaluate_models_on_training(hxarray1, hyarray1, [hmod1[0], hmod2[0]]))
    # print(gen_cities_avg(climate1, cities1, years1))
    # print(moving_average(mavgarray1, 3), moving_average(mavgarray1, 3) == cr1, 
    #       sum(moving_average(mavgarray1, 3)) == sum(cr1))
    # print(moving_average(mavgarray4, 2), moving_average(mavgarray4, 2) == cr4,
    #       sum(moving_average(mavgarray4, 2)) == sum(cr4))
    # print(moving_average(mavgarray2, 5))
    # print(rmse(rmy1, rme1))
    # for i in range(len(evxar_lst)):
    #     evaluate_models_on_training(evxar_lst[i], evyar_lst[i], generate_models(evxar_lst[i], 
    #                                                                             evyar_lst[i], [13]))
    #     evaluate_models_on_training(evxar_lst[i], evyar_lst[i], generate_models(evxar_lst[i], 
    #                                                                             evyar_lst[i], [14]))
    #     evaluate_models_on_training(evxar_lst[i], evyar_lst[i], generate_models(evxar_lst[i], 
    #                                                                             evyar_lst[i], [25]))
    # evaluate_models_on_training(evxar5, evyar5, generate_models(evxar5, evyar5, [19]))
    print(gen_std_devs(climate, ['SEATTLE'], years))
    

if __name__ == '__main__':
    test()



# if __name__ == '__main__':

    

    # Part A.4
    sample_climate = Climate('data.csv')
    sample_years = pylab.array(TRAINING_INTERVAL)
    sample_temp = pylab.array([])
    for year in sample_years:
       sample_temp = pylab.append(sample_temp, sample_climate.get_daily_temp('NEW YORK', 1, 10, year))
    temp_model = generate_models(sample_years, sample_temp, [1])
    # evaluate_models_on_training(sample_years, sample_temp, temp_model)
    sample_yearly_temp = pylab.array([])
    for year in sample_years:
        avg_temp = 0
        avg_temp += sum(sample_climate.get_yearly_temp('NEW YORK', year))
        avg_temp = avg_temp / len(sample_climate.get_yearly_temp('NEW YORK', year))
        sample_yearly_temp = pylab.append(sample_yearly_temp, avg_temp)    
    yearly_temp_model = generate_models(sample_years, sample_yearly_temp, [1])
    # evaluate_models_on_training(sample_years, sample_yearly_temp, yearly_temp_model)
    # Part B
    nat_avg = gen_cities_avg(sample_climate, CITIES, sample_years)
    nat_mod = generate_models(sample_years, nat_avg, [1])
    # evaluate_models_on_training(sample_years, nat_avg, nat_mod)
    
    # Part C
    # print(list(nat_avg))
    mov_avg = moving_average(nat_avg, 5)
    # evaluate_models_on_training(sample_years, mov_avg,generate_models(sample_years, mov_avg, [1]))

    # Part D.2
    test_years = pylab.array(TESTING_INTERVAL)
    train_mod = generate_models(sample_years, mov_avg, [1,2,20])
    # evaluate_models_on_training(sample_years, mov_avg, train_mod)
    nat_avg_test = gen_cities_avg(sample_climate, CITIES, test_years)
    mov_avg_test = moving_average(nat_avg_test, 5)
    # evaluate_models_on_testing(test_years, mov_avg_test,train_mod)
    
    
    # Part E
    # TODO: replace this line with your code
