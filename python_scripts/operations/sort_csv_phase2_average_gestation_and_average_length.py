"""
Create the sorted Phase 2 total tasks and average length dataframe.

function:: def sort_csv(csv_name: str, sorted_name: str) -> str
"""
from sys import path
from time import asctime, localtime, time
from dfply import arrange, select, X
from pandas import read_csv
from pathlib import Path

module_path = Path(__file__).resolve()
operations_folder = module_path.parent
scripts_folder = operations_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))

output_folder= str(project_folder) + '/output_analysis'

def sort_csv(
    csv_name = 'phase2_average_gestation_and_average_length.csv',  
    sorted_name= 'phase2_average_gestation_and_average_length_dataframe.csv'
    ):

    '''
    Sort the csv.

    :param str csv_name: Name the input .csv.
    :param str sorted_name: Name the sorted .csv. (dataframe)
    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Read unsorted: csv location
              Saved sorted: csv location'
    :rtype: str
    '''

    csv = read_csv(output_folder + '/raw/' + csv_name)
    csv_dataframe = (
        csv 
        >> select(
            X.environment, 
            X.depth, 
            X.lineage, 
            X.replicate, 
            X.trait, 
            X.evolved_population_value,
            X.raw_evolved_population_value
            ) 
        >> arrange(
            X.trait, 
            X.environment, 
            X.depth, 
            X.lineage, 
            X.replicate
            ))
    csv_dataframe.to_csv(output_folder + '/' +  sorted_name)

    log_name= 'sort_csv_phase2_average_gestation_and_average_length_log.txt'
    date_time_year = (
        '\nDate, time, and year: %s \n' % (asctime(localtime(time())))
        )
    text = (
        'Sorted the the .csv file %s \n'
        'from the analysis directory:\n%s\n\n'
        'Sorted dataframe located in analysis directory as:\n%s' 
        % (
            csv_name, 
            output_folder, 
            sorted_name
            ))
    filename = str(project_folder) + '/logs/' +  log_name
    with open(filename, 'w+') as file:
        file.writelines([
            'Signator: J. Bundy', 
            str(date_time_year), ('\n'), 
            str(text)
            ])


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
            (output_folder+ '/raw/' + csv_name), 
            (output_folder+ '/' + sorted_name), 
            ))

if __name__ == '__main__':
    print(
        sort_csv(
            csv_name = 'phase2_average_gestation_and_average_length.csv',  
            sorted_name= 'phase2_average_gestation_and_average_length_dataframe.csv'
            ))


