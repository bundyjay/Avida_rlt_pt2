"""
Sort the Phase 1 dataframe.

function:: def sort_csv(csv_name: str, sorted_name: str) -> str
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

import csv
from decimal import Decimal
from dfply import arrange, select, X
from pathlib import Path
from pandas import read_csv
import sys
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
operations_folder = module_path.parent
scripts_folder = operations_folder.parent
project_folder = scripts_folder.parent
sys.path.insert(0, str(scripts_folder))
sys.path.insert(0, str(operations_folder))


def sort_csv(
    csv_name='phase1_corr_fitness_genome_length_raw.csv', 
    sorted_name='phase1_corr_fitness_genome_length_dataframe.csv'
    ):

    '''
    Sort the csv.

    :param str csv_name: Name the input csv.
    :param str sorted_name: Name the sorted csv. (dataframe)
    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Read unsorted: csv location
              Saved sorted: csv location'
    :rtype: str
    '''

    analysis_directory = str(project_folder) + '/output_analysis'
    csv = read_csv(
        analysis_directory 
            + '/raw/' 
            + csv_name, 
        dtype={'ancestor_seed': str}
        )

    csv_trajectory_phase1_dataframe = (
        csv 
        >> arrange(
            X.ancestor_seed, 
            X.time
            ))
    csv_trajectory_phase1_dataframe.to_csv(
        analysis_directory 
        + '/' 
        + sorted_name
        )
        
    date_time_year = asctime(localtime(time()))

    return ((
         '\n\n'
         'Date, time, and year: %s \n'
         'Module: %s \n' 
         'Read unsorted: %s \n' 
         'Saved sorted: %s '
         )
        % (
            date_time_year,
            module_path, 
            (analysis_directory + '/raw/' + csv_name), 
            (analysis_directory + '/' + sorted_name), 
            ))


if __name__ == '__main__':
    print(
        sort_csv(
            csv_name='phase1_corr_fitness_genome_length_raw.csv', 
            sorted_name='phase1_corr_fitness_genome_length_dataframe.csv'
            ))