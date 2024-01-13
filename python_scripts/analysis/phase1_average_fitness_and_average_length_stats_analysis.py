"""
Analyze the Phase 1 total tasks and average length by depth.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply.reshape import spread
import pandas as pd
import numpy as np
import math
from math import sqrt as sqrt
from dfply import gather, group_by, mask, mutate, spread, summarize, X
from pandas import read_csv
from pathlib import Path
from time import asctime, localtime, time
from scipy import stats as stats
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))
output_folder = str(project_folder) + '/output_analysis'

ACH_phase1_average_fitness_and_average_length_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase1_average_fitness_and_average_length_dataframe.csv'
    )

ACH_phase1_ttest_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase1_ttest_dataframe.csv'
    )


"""
Number of replicates (i.e. populations- 101-110), per group.
"""
N = 10 


"""
Calculate group means by depth.
"""
group_means = (
    ACH_phase1_average_fitness_and_average_length_dataframe 
    >> group_by(X.trait, X.depth) 
    >> summarize(group_mean = X.evolved_population_value.mean(),
                 group_std = X.evolved_population_value.std()
                ))
var_group_dataframe = (
    ACH_phase1_average_fitness_and_average_length_dataframe 
    >> group_by(X.trait, X.depth) 
    >> mutate(group_mean = X.evolved_population_value.mean(),
              group_std = X.evolved_population_value.std()
              )
    >> mutate(group_deviations = (X.evolved_population_value - X.group_mean)
              )
    >> mutate(
        group_deviations_sqrd = (X.group_deviations**2)
        )
    >> mutate(
        sum_sqrd_deviations = (X.group_deviations_sqrd.sum())
        )
    >> mutate(
        group_var = (X.sum_sqrd_deviations / (N -1))
        )
    >> mutate(
        group_std_measured = (X.group_var**0.5)
        ))
var_group_dataframe_csv_name = 'phase1_var_group_dataframe.csv'
var_group_dataframe_location =  (
    output_folder 
    + '/' 
    + var_group_dataframe_csv_name
    )
var_group_dataframe.to_csv(var_group_dataframe_location)

var_summary_dataframe = (
    var_group_dataframe
    >> group_by(X.trait, X.depth) 
    >> summarize(group_mean = X.group_mean.mean(),
                 sum_sqrd_deviations = X.sum_sqrd_deviations.mean(),
                 group_var = X.group_var.mean(),
                 group_std = X.group_std_measured.mean()
                 ))
var_summary_dataframe_csv_name = 'phase1_var_summary_dataframe.csv'
var_summary_dataframe_location =  (
    output_folder 
    + '/' 
    + var_summary_dataframe_csv_name
    )
var_summary_dataframe.to_csv(var_summary_dataframe_location)

fitness_sd_500k =var_summary_dataframe.iloc[2]['group_std']

df = pd.DataFrame(columns=["trait", "source", "value"], data=[['','',float(0)]])
df.at[0] = ('fitness', '500k sd', var_summary_dataframe.iloc[2]['group_std'])
df.at[1] = ('fitness', '20k sd', var_summary_dataframe.iloc[0]['group_std'])
df.at[2] = ('fitness', 'N', N)
df.at[3] = ('fitness', 'df', (N-1))
df.at[4] = ('fitness', 'T', (
    (N - 1) * (var_summary_dataframe.iloc[2]['group_std'] 
    / var_summary_dataframe.iloc[0]['group_std'])
    ))
df.at[5] = ('fitness', 'alpha', .05)
df.at[6] = ('fitness', 'tails', 2)
df.at[7] = ('fitness', 'alpha/2', 0.025)
df.at[8] = ('fitness', '1 - alpha/2', (1 - (.05/2)))
df.at[9] = ('fitness', 'upper_crit', 19.023)  #critical value of chi^2 distribution given N-1 degrees of freedom (use link)
df.at[10] = ('fitness', 'lower_crit', 2.700)  #critical value of chi^2 distribution given N-1 degrees of freedom (use link)
df.at[11] = ('fitness', 'upper_bound', (
    sqrt(((N - 1) * (var_summary_dataframe.iloc[2]['group_std'] ** 2)) /  2.700)
    ))
df.at[12] = ('fitness', 'lower_bound', (
    sqrt(((N - 1) * (var_summary_dataframe.iloc[2]['group_std'] ** 2)) / 19.023)
    ))
df.at[13] = ('genome_length', '500k sd', 
    var_summary_dataframe.iloc[5]['group_std']
    )
df.at[14] = ('genome_length', '20k sd', 
    var_summary_dataframe.iloc[3]['group_std']
    )
df.at[15] = ('genome_length', 'N', N)
df.at[16] = ('genome_length', 'df', (N-1))
df.at[17] = ('genome_length', 'T', (
    (N - 1) * (var_summary_dataframe.iloc[5]['group_std'] 
    / var_summary_dataframe.iloc[3]['group_std'])
    ))
df.at[18] = ('genome_length', 'alpha', .05)
df.at[19] = ('genome_length', 'tails', 2)
df.at[20] = ('genome_length', 'alpha/2', 0.025)
df.at[21] = ('genome_length', '1 - alpha/2', (1 - (.05/2)))
df.at[22] = ('genome_length', 'upper_crit', 19.023)  #critical value of chi^2 distribution given N-1 degrees of freedom (use link)
df.at[23] = ('genome_length', 'lower_crit', 2.700)  #critical value of chi^2 distribution given N-1 degrees of freedom (use link)
df.at[24] = ('genome_length', 'upper_bound', (
    sqrt(((N - 1) * (var_summary_dataframe.iloc[5]['group_std'] ** 2)) 
    / 2.700 
    )))
df.at[25] = ('genome_length', 'lower_bound', (
    sqrt(((N - 1) * (var_summary_dataframe.iloc[5]['group_std'] ** 2)) 
    / 19.023 
    )))

chi_square_var_test_dataframe = df
chi_square_var_test_dataframe_csv_name = 'phase1_chi_square_var_test_dataframe.csv'
chi_square_var_test_dataframe_location =  (
    output_folder 
    + '/' 
    + chi_square_var_test_dataframe_csv_name
    )
chi_square_var_test_dataframe.to_csv(chi_square_var_test_dataframe_location)

t_test = (
    ACH_phase1_ttest_dataframe 
    >> mutate(difference = (X.deep_evolved_population_value_log10 - X.shallow_evolved_population_value_log10)
              )
    >> group_by(X.trait) 
    >> summarize(difference_mean = X.difference.mean(),
                 difference_std = X.difference.std())
    >> mutate(difference_sem = X.difference_std / (sqrt (N))
                )
    >> mutate(t = (X.difference_mean - 0) / X.difference_sem)
    >> mutate(t_lower = (X.t - (1.96 * X.difference_sem)),
              t_upper = (X.t + (1.96 * X.difference_sem))
              ))

fitness_t = t_test.iloc[0]['t']
genome_length_t = t_test.iloc[1]['t']

fitness_p_value = stats.t.sf(fitness_t, df = (N - 1)) * 2
if fitness_p_value < 0.0001:
    fitness_p_value_str = '****<0.0001'
elif fitness_p_value < 0.001:
    fitness_p_value_str = '***<0.001'
elif fitness_p_value < 0.01:
    fitness_p_value_str = '**<0.01'
elif fitness_p_value < 0.05:
    fitness_p_value_str = '*<0.05' % (fitness_p_value)   
else:
    fitness_p_value_str = str(round(fitness_p_value, 4)) 

genome_length_p_value = stats.t.sf(genome_length_t, df = (N - 1)) * 2
if genome_length_p_value < 0.0001:
    genome_length_p_value_str = '****<0.0001'
elif genome_length_p_value < 0.001:
    genome_length_p_value_str = '***<0.001'
elif genome_length_p_value < 0.01:
    genome_length_p_value_str = '**<0.01'
elif genome_length_p_value < 0.05:
    genome_length_p_value_str = '*<0.05' % (genome_length_p_value)   
else:
    genome_length_p_value_str = str(round(genome_length_p_value, 4))   
                
t_test['p_value'] = [fitness_p_value, genome_length_p_value]
t_test['p_value_str'] = [fitness_p_value_str, genome_length_p_value_str]


t_test_dataframe_csv_name = 'phase1_t_test_summary_dataframe.csv'
t_test_dataframe_location =  (
    output_folder 
    + '/' 
    + t_test_dataframe_csv_name 
    )
t_test.to_csv(t_test_dataframe_location)

log_name= 'phase1_average_fitness_and_average_length_stats_analysis_log.txt'  
date_time_year = (
    '\nDate, time, and year: %s \n' % (asctime(localtime(time()))) 
    )
text1 = group_means 
text2 = var_group_dataframe
text3 = var_summary_dataframe
filename = str(project_folder) + '/logs/' +  log_name
with open(filename, 'w+') as file:
    file.writelines([
        'Signator: J. Bundy', 
        str(date_time_year), ('\n'), 
        'The data is as follows:', ('\n'), 
        str(text1), ('\n'), ('\n'),
        str(text2), ('\n'), ('\n'),
        str(text3)
        ])
        