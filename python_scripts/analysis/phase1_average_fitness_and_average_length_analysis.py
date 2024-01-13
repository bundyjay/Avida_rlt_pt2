"""
Analyze the Phase 1 total tasks and average length by depth.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import group_by, summarize, X
from pandas import read_csv
from pathlib import Path
from time import asctime, localtime, time
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))

ACH_phase1_average_fitness_and_average_length_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase1_average_fitness_and_average_length_dataframe.csv'
    )


"""
Calculate group means by depth.
"""
group_means = (
    ACH_phase1_average_fitness_and_average_length_dataframe 
    >> group_by(X.trait, X.depth) 
    >> summarize(
        group_mean = X.evolved_population_value.mean(),
        group_std = X.evolved_population_value.std(),
        raw_mean = X.raw_evolved_population_value.mean(),
        raw_std = X.raw_evolved_population_value.std(),
                ))

log_name= 'phase1_average_fitness_and_average_length_analysis_log.txt'  
date_time_year = (
    '\nDate, time, and year: %s \n' % (asctime(localtime(time()))) 
    )
text = group_means
filename = str(project_folder) + '/logs/' +  log_name
with open(filename, 'w+') as file:
    file.writelines([
        'Signator: J. Bundy', 
        str(date_time_year), ('\n'), 
        'The data is as follows:', ('\n'), 
        str(text)
        ])
        