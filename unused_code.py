# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 16:34:41 2021

@author: scout
"""
[6.111932525547663, 5.410262507640112, 6.030421044139480, 5.582323971063784, 5.590815196537217, 5.034763473603158, 6.248508178497177, 5.675263725351870, 5.982249304126632, 5.537621671909089, 6.033933156228509, 6.347143466163273, 5.387256485922278, 5.752836189735770, 6.011732939262028, 5.592257961095585, 5.6788817521223, 5.781089937304327, 5.718417857766408, 5.395580940200403, 5.173688692019366, 5.813422979017657, 5.191573321475987, 5.402331413951959, 6.786844210983085, 5.295287094733411, 5.606459762429633, 5.492109790810208, 6.145020282541521, 6.359102184800527, 5.499686635335061, 5.651682089431005, 5.796998330307141, 5.853122795803193, 5.254549207209780, 6.010270101745012, 5.532749383809286, 5.770303460533653, 5.041262497246844, 5.272866293889726, 5.085921173472264, 5.552642682373498, 5.800572059454674, 5.739142696516538, 5.551853823563220, 5.827956214216807, 5.908950839088547, 5.978990840187739, 6.569615394010557]
[6.1119325255476635, 5.4102625076401125, 6.0304210441394801, 5.5823239710637846, 5.5908151965372177, 5.0347634736031583, 6.2485081784971772, 5.6752637253518703, 5.9822493041266327, 5.5376216719090898, 6.0339331562285095, 6.3471434661632733, 5.3872564859222782, 5.7528361897357705, 6.0117329392620285, 5.5922579610955854, 5.67888175212234, 5.7810899373043272, 5.7184178577664087, 5.3955809402004036, 5.1736886920193665, 5.8134229790176573, 5.1915733214759872, 5.4023314139519591, 6.7868442109830855, 5.2952870947334114, 5.6064597624296333, 5.4921097908102086, 6.1450202825415214, 6.3591021848005278, 5.4996866353350615, 5.6516820894310058, 5.7969983303071411, 5.8531227958031931, 5.2545492072097808, 6.0102701017450126, 5.5327493838092865, 5.7703034605336532, 5.0412624972468443, 5.2728662938897264, 5.0859211734722649, 5.5526426823734987, 5.8005720594546748, 5.7391426965165389, 5.5518538235632207, 5.8279562142168073, 5.9089508390885479, 5.9789908401877394, 6.5696153940105573]

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
            
            
        std_dev = pylab.append(std_dev, ((sum(nat_daily_avg - nat_year_avg)**2)
                                         /(len(nat_daily_avg)-1))**0.5)
    return(std_dev)