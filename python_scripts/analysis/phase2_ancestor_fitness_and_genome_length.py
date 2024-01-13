"""
Analyze the Phase 2 total tasks and average length by depth.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""
__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import group_by, mask, rename, summarize, X
from pandas import read_csv
from pathlib import Path
from time import asctime, localtime, time
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))
output_folder = str(project_folder) + '/output_analysis'


phase2_ancestor_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase2_dataframe.csv'
    )

"""
Calculate group means by depth.
"""
ancestor_values = (
    phase2_ancestor_dataframe 
    >> group_by(
        X.environment, 
        X.trait, 
        X.ancestor_run_length,
        X.lineage
        )
    >> mask(X.time == 0)
    >> summarize(ancestor_value = X.ancestor_value_log10.mean())
    >> rename(depth = X.ancestor_run_length))

#print(ancestor_values)
ancestor_values_csv_name = 'ancestor_values_dataframe.csv'
ancestor_values_dataframe_location =  (
    output_folder 
    + '/' 
    + ancestor_values_csv_name
    )
ancestor_values.to_csv(ancestor_values_dataframe_location)


log_name= 'phase2_ancestor_fitness_and_genome_length_analysis_log.txt'
date_time_year = (
    '\nDate, time, and year: %s \n' % (asctime(localtime(time())))
    )
text = ancestor_values
filename = str(project_folder) + '/logs/' +  log_name
with open(filename, 'w+') as file:
    file.writelines([
        'Signator: J. Bundy', 
        str(date_time_year), ('\n'), 
        'The data_dict is:', ('\n'), 
        str(text)
        ])