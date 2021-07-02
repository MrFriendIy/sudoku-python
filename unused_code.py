# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 16:34:41 2021

@author: scout
"""
    daily_temps = pylab.array([])
    all_cities_yearly = {}
    for year in years:
        city_temp_yearly = []
        for city in multi_cities:
            daily_temps = climate.get_yearly_temp(city, year)
            city_and_temp = (city, daily_temps)
            city_temp_yearly.append(city_and_temp)
        all_cities_yearly[year] = city_temp_yearly
    avg_daily_tmp_yearly = {}
    for year in all_cities_yearly:
        for city in all_cities_yearly[year]:
            
            
        # key: years. values: array of average daily temps
    avg_daily_tmp_yearly = {}
    for year in years:
        daily_tmp = pylab.array([])
        for city in multi_cities:
            city_temps = climate.get_yearly_temp(city, year)
            # this feels a little sloppy. might improve if I think of a better way
            if len(daily_tmp) != len(city_temps):
                for i in range(len(city_temps)):
                    daily_tmp = pylab.append(daily_tmp, 0)
            daily_tmp += city_temps
        daily_tmp /= len(multi_cities)
        avg_daily_tmp_yearly[year] =  daily_tmp
    std_devs = pylab.array([])
    mean_temp = gen_cities_avg(climate, multi_cities, years)
    count = 0
    for year in avg_daily_tmp_yearly:
        sums = 0
        for i in range(len(avg_daily_tmp_yearly[year])):
            sums += (avg_daily_tmp_yearly[year][i] - mean_temp[count])**2
        std_devs = pylab.append(std_devs, (sums/(len(years)))**0.5)
        count += 1
    return(std_devs)

    avg_city_tmp = gen_cities_avg(climate, multi_cities, years)
    avg_nat_temp = sum(avg_city_tmp)/len(avg_city_tmp)
    std_devs = pylab.array([])
    for year in years:
        sums = 0
        for i in range(len(avg_city_tmp)):
            sums += (avg_city_tmp[i]-avg_nat_temp)**2
        std_devs = pylab.append(std_devs, (sums/(len(years)))**0.5)
    return(std_devs)

        if len(models[est])-1 > 4:
            pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1)
                            + 'standard error to slope:' + se_ov_slope_list[est])
        elif len(models[est])-1 == 1:
            pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1) 
                            + '\n' + 'linear' + 'standard error to slope:' + se_ov_slope_list[est])
        elif len(models[est])-1 == 2:
            pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1) 
                            + '\n' + 'quadratic' + 'standard error to slope:' + se_ov_slope_list[est])
        elif len(models[est])-1 == 3:
            pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1) 
                            + '\n' + 'cubic' + 'standard error to slope:' + se_ov_slope_list[est])    
        elif len(models[est])-1 == 4:
            pylab.plt.title('R^2:' + str(R2_list[est]) + '\n' + 'Degree:' + str(len(models[est])-1) 
                            + '\n' + 'quartic' + 'standard error to slope:' + se_ov_slope_list[est])