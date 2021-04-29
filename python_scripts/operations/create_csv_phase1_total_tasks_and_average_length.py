"""
Create the Phase 1 total tasks and average genome length dataframe.

function:: def create_csv(data_dict: dict, csv_name: str) -> str
function:: def create_and_sort_csv() -> generator
"""
__author__ = 'Jason Bundy'
__version__ = '1.0'

from collections import defaultdict
from csv import writer
from decimal import Decimal
from math import log10 as log10
from os import listdir
from pathlib import Path
from re import search
from sys import path
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
operations_folder = module_path.parent
scripts_folder = operations_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))
 
from data_dict_phase1_total_tasks_and_average_length import create_data_dict
from sort_csv_phase1_total_tasks_and_average_length import sort_csv 

output_folder = str(project_folder) + '/output_analysis'


def create_csv(
    data_dict= create_data_dict(
        log_name= 'data_dict_phase1_total_tasks_and_average_length_log.txt'
        ), 
    csv_name= 'phase1_total_tasks_and_average_length_raw.csv'
    ):
    
    """
    Create the csv.

    :param dict data_dict: Store data in dict.
    :param str csv_name: Name the .csv.
    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Created csv: file_location'
    :rtype: str
    """

    file_location = output_folder + '/raw/' + csv_name
    with open(file_location, 'w+', newline='') as csvfile:
        csv_writer = writer(csvfile, delimiter=',')
        csv_writer.writerow([
            'run_id', 
            'depth', 
            'ancestor_seed', 
            'trait', 
            'evolved_population_value'
            ])
        for key, attributes in data_dict.items():
            values = data_dict[key].values()
            csv_writer.writerow([key, *values])

    log_name= 'create_csv_phase1_total_tasks_and_average_length_log.txt'
    text = (
        'Created the .csv file %s \nin the analysis directory:\n%s' 
        % (csv_name, output_folder)
        )
    
    date_time_year = asctime(localtime(time())) 
    
    filename = str(project_folder) + '/logs/' +  log_name
    with open(filename, 'w+') as file:
        file.writelines([
            'Signator: J. Bundy', 
            '\nDate, time, and year: \n',
            date_time_year, ('\n'), 
            str(text)
            ])

    return (
        '\n\n'
        'Date, time, and year: %s \n' 
        'Module: %s \n'
        'Created csv: %s' 
        % (
            date_time_year, 
            module_path, 
            file_location
            ))


def create_and_sort_csv():

    '''
    Run create_csv then sort_csv.

    Uses generator syntax to enforce order.
    :return: generator_object
    :yields: (print(create_csv()), print(sort_csv())
    :rtype: generator
    '''    

    yield print(create_csv(
        data_dict= create_data_dict(
            log_name= 
                'data_dict_phase1_total_tasks_and_average_length_log.txt'
            ), 
        csv_name= 'phase1_total_tasks_and_average_length_raw.csv'
        ))
    yield print(sort_csv(
        csv_name = 'phase1_total_tasks_and_average_length_raw.csv', 
        sorted_name= 'phase1_total_tasks_and_average_length_dataframe.csv'
        ))


if __name__ == '__main__':
    csv_sort = create_and_sort_csv()
    next(csv_sort)
    next(csv_sort)

