"""
Sort the Phase 1 trajectory dataframe.

function:: def sort_csv(csv_name: str, sorted_name: str) -> str
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from decimal import Decimal
from dfply import arrange, select, X
from pandas import read_csv
from pathlib import Path
from sys import path
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
operations_folder = module_path.parent
scripts_folder = operations_folder.parent
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(scripts_folder))

def sort_csv(
    csv_name='phase2_gestation.csv', 
    sorted_name='phase2_gestation_dataframe.csv'
    ):
    
    '''
    Sort the csv.

    :param str csv_name: Name the input .csv.
    :param str sorted_name: Name the sorted .csv. (dataframe)
    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Read unsorted: csv_location
              Saved sorted .csv: csv_location'
    :rtype: str
    '''

    csv = read_csv(
        output_folder 
        + '/raw/' 
        + csv_name, 
        dtype={
            'lineage': str, 
            'replicate': str
            }, 
        converters= {
            'ancestor_value': Decimal, 
            'ancestor_value_log10': Decimal, 
            'evolved_population_average_value': Decimal,  
            'evolved_population_average_value_log10': Decimal, 
            'evolved_relative_value': Decimal, 
            'evolved_relative_value_log10': Decimal
            })
    csv_trajectory_phase2_dataframe = (csv >> 
    select(
        X.run_id, 
        X.series, 
        X.environment, 
        X.ancestor_run_length, 
        X.lineage, 
        X.replicate, 
        X.time, 
        X.trait, 
        X.ancestor_value, 
        X.ancestor_value_log10, 
        X.evolved_population_average_value, 
        X.evolved_population_average_value_log10, 
        X.evolved_relative_value, 
        X.evolved_relative_value_log10
        ) 
        >> arrange(
            X.trait, 
            X.environment, 
            X.ancestor_run_length, 
            X.lineage, 
            X.replicate, 
            X.time
            )) 
    sorted_csv_location =  output_folder + '/' + sorted_name
    csv_trajectory_phase2_dataframe.to_csv(sorted_csv_location)

    date_time_year = asctime(localtime(time()))

    return ((
         '\n\n'
         'Date, time, and year: %s \n'
         'Module: %s \n' 
         'Read unsorted .csv: %s \n' 
         'Saved sorted .csv: %s '
         )
        % (
            date_time_year,
            module_path, 
            (
                output_folder 
                + '/raw/' 
                + csv_name
                ), 
            (
                output_folder 
                + '/' 
                + sorted_name
                )))


if __name__ == '__main__':
    sort_csv(
        csv_name='phase2_gestation_raw.csv', 
        sorted_name='phase2_gestation_dataframe.csv'
        )
