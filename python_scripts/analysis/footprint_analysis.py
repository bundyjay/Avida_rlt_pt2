"""
Analyze the fitness differences between shallow and deep populations.

Saves 'footprint_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""
__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import group_by, mask, mutate, spread, summarize, X
from pandas import concat, merge, read_csv 
from pathlib import Path
from time import asctime, localtime, time
from scipy import stats as stats
from sys import path

import pandas as pd
pd.set_option('max_columns', None)

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))

footprint_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'footprint_dataframe.csv'
    )

"""
Calculate group means by depth.
Start with shallow_overlapping (A) values.
"""
footprint_values = (
    footprint_dataframe
    >> mask(X.depth == 20000, 
            X.trait == 'fitness', 
            X.environment == 'overlapping')
    >> group_by(X.lineage)
    >> summarize(A_shallow_overlapping = X.evolved_log10_difference.mean())
    )

deep_overlapping = (
    footprint_dataframe
    >> mask(X.depth == 500000, 
            X.trait == 'fitness', 
            X.environment == 'overlapping')
    >> group_by(X.lineage)
    >> summarize(B_deep_overlapping = X.evolved_log10_difference.mean())
    )

shallow_orthogonal = (
    footprint_dataframe
    >> mask(X.depth == 20000, 
            X.trait == 'fitness', 
            X.environment == 'orthogonal')
    >> group_by(X.lineage)
    >> summarize(C_shallow_orthogonal= X.evolved_log10_difference.mean())
    )

deep_orthogonal = (
    footprint_dataframe
    >> mask(X.depth == 500000, 
            X.trait == 'fitness', 
            X.environment == 'orthogonal')
    >> group_by(X.lineage)
    >> summarize(D_deep_orthogonal= X.evolved_log10_difference.mean())
    )

footprint_values['B_deep_overlapping'] = (
    deep_overlapping['B_deep_overlapping'].values
    )
footprint_values['C_shallow_orthogonal'] = (
    shallow_orthogonal['C_shallow_orthogonal'].values
    )
footprint_values['D_deep_orthogonal'] = (
    deep_orthogonal['D_deep_orthogonal'].values
    )

footprint_values = (
    footprint_values
    >> mutate (X_overlapping_minus_orthogonal = (
        (X.A_shallow_overlapping - X.B_deep_overlapping) 
        - 
        (X.C_shallow_orthogonal - X.D_deep_orthogonal)
        ))
    >> mutate (Y_relative_overlapping_minus_orthogonal = (
        (X.A_shallow_overlapping / X.B_deep_overlapping) 
        -
        (X.C_shallow_orthogonal / X.D_deep_orthogonal)
        )))



mean_overlapping_minus_orthogonal = footprint_values['X_overlapping_minus_orthogonal'].mean()
mean_relative_overlapping_minus_orthogonal = footprint_values['Y_relative_overlapping_minus_orthogonal'].mean()

T_overlapping_minus_orthogonal = stats.ttest_1samp(footprint_values['X_overlapping_minus_orthogonal'].values, 0, axis=0)
T_relative_overlapping_minus_orthogonal = stats.ttest_1samp(footprint_values['Y_relative_overlapping_minus_orthogonal'].values, 0, axis=0)

Wilcoxon_overlapping_minus_orthogonal= stats.wilcoxon(footprint_values['X_overlapping_minus_orthogonal'].values, y=None)
Wilcoxon_overlapping_minus_orthogonal= str(Wilcoxon_overlapping_minus_orthogonal)
Wilcoxon_relative_overlapping_minus_orthogonal= stats.wilcoxon(footprint_values['Y_relative_overlapping_minus_orthogonal'].values, y=None)
Wilcoxon_relative_overlapping_minus_orthogonal = str(Wilcoxon_relative_overlapping_minus_orthogonal)

log_name= 'footprint_analysis_log.txt'
date_time_year = (
    '\nDate, time, and year: %s \n' % (asctime(localtime(time())))
    )
filename = str(project_folder) + '/logs/' +  log_name
with open(filename, 'w+') as file:
    file.writelines([
        'Signator: J. Bundy', 
        str(date_time_year), ('\n'), 
        'The data_dict is:', ('\n'), 
        repr(footprint_values), ('\n'), ('\n'),
        'mean_X_overlapping_minus_orthogonal: ', str(mean_overlapping_minus_orthogonal), ('\n'), 
        'mean_Y_relative_overlapping_minus_orthogonal: ', str(mean_relative_overlapping_minus_orthogonal), ('\n'), ('\n'),
        'X_T_overlapping_minus_orthogonal: ', str(T_overlapping_minus_orthogonal),('\n'),
        'Y_T_relative_overlapping_minus_orthogonal: ', str(T_relative_overlapping_minus_orthogonal), ('\n'), ('\n'),
        'X_Wilcoxon_overlapping_minus_orthogonal: ', Wilcoxon_overlapping_minus_orthogonal, ('\n'), 
        'Y_Wilcoxon_relative_overlapping_minus_orthogonal: ', Wilcoxon_relative_overlapping_minus_orthogonal
        ])