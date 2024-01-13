"""
Create the Phase 2 total tasks and average length dict.

function:: def data_dict(log_name: str) -> dict
"""
__author__ = 'Jason Bundy'
__version__ = '1.0'

from collections import defaultdict
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

from find_subfolders import find_subfolders

input_folder= str(project_folder) + '/output_phase2'
input_folders = list(find_subfolders(input_folder))

def create_data_dict(log_name= 'data_dict_phase2_average_gestation_and_average_length_log.txt'):

    '''
    Create the data_dict.

    :param str log_name: Name the log.
    :return: data_dict
    :rtype: dict
    '''

    data_dict = defaultdict(dict)
    run_data_dict = defaultdict(dict)
    evolved_data_dict = defaultdict(dict)
    list_of_keys = []
        
    for each_input_folder in input_folders:
 
        """
        Example string to serve as pattern (template) for run_info:
        ReplicateEnv38tasksnoequodd10k_
        AncestorSeed102Env38tasksnoequeven
        4k_
        1002 
        or 
        ReplicateEnv76tasksnoequ10k_
        AncestorSeed101Env38tasksnoequeven
        20k_1003
        """      
        run_info = search(
            r'ReplicateEnv([\d]+)([a-z]+)([\d]+)k_'
            r'AncestorSeed([\d]+)Env([\d]+)([a-z]+)'
            r'([\d]+)k_'
            r'([\d]+)' , 
            each_input_folder
            )
        evolved_seed = run_info.group(8)
        replicate_environment = run_info.group(1) + run_info.group(2)
        evolved_run_length = int(run_info.group(3)) * 1000
        run_length_unit = 'updates' #updates or generations
        ancestor_seed = run_info.group(4)
        ancestor_environment = run_info.group(5) + run_info.group(6)
        ancestor_run_length = int(run_info.group(7)) * 1000
        if replicate_environment == '38tasksnoequodd':
            evolved_environment = 'orthogonal'
        if replicate_environment == '76tasksnoequ':
            evolved_environment = 'overlapping'

        gestation_key = (
            'ReplicateEnvironment%s_'
            'AncestorRunLength%s_'
            'AncestorSeed%s_'
            'ReplicateSeed%s_'
            'Gestation' 
            % (
                evolved_environment, 
                ancestor_run_length, 
                ancestor_seed, 
                evolved_seed
                ))
        list_of_keys.append(gestation_key) 
        run_data_dict[gestation_key] = {
            'evolved_run_length': evolved_run_length, 
            'run_length_unit': run_length_unit, 
            'ancestor_environment': ancestor_environment, 
            'evolved_environment': evolved_environment, 
            'ancestor_run_length': ancestor_run_length, 
            'ancestor_seed': ancestor_seed, 
            'evolved_seed' : evolved_seed
            }
        length_key = (
            'ReplicateEnvironment%s_'
            'AncestorRunLength%s_'
            'AncestorSeed%s_'
            'ReplicateSeed%s_'
            'Length' 
            % (
                evolved_environment, 
                ancestor_run_length, 
                ancestor_seed, 
                evolved_seed
                ))
        list_of_keys.append(length_key) 
        run_data_dict[length_key] = {
            'evolved_run_length': evolved_run_length, 
            'run_length_unit': run_length_unit, 
            'ancestor_environment': ancestor_environment, 
            'evolved_environment': evolved_environment, 
            'ancestor_run_length': ancestor_run_length, 
            'ancestor_seed': ancestor_seed, 
            'evolved_seed' : evolved_seed
            }
       
        data_folder = input_folder + '/' + each_input_folder + '/data'    
        average_data_file_location = data_folder + '/average.dat'
        with open(average_data_file_location, 'r') as average_file:
            average_lines = average_file.readlines()
            for a_line in average_lines:
                final_update_line = search(
                    r'(^%d)\s.*\n' 
                    % (evolved_run_length), 
                    a_line
                    )
                if final_update_line:
                
                    final_update_info = search(
                        #1.Update 
                        r'(^%d)\s'
                        #2.Merit 
                        r'([0-9,.e+-]+)\s'
                        #3.Gestation_Time 
                        r'([0-9,.e+-]+)\s'
                        #4.Fitness 
                        r'([0-9,.e+-]+)\s'
                        #5.Repro_Rate? 
                        r'([0-9,.e+-]+)\s'
                        #6.(deprecated)size 
                        r'([0-9,.e+-]+)\s'
                        #7.Copied_Size 
                        r'([0-9,.e+-]+)\s'
                        #8.Executed_Size 
                        r'([0-9,.e+-]+)\s'
                        #9.(deprecated)abundance 
                        r'([0-9,.e+-]+)\s'
                        #10.Proportion_giving_birth_this_update 
                        r'([0-9,.e+-]+)\s'
                        #11.Proportion_breed_true 
                        r'([0-9,.e+-]+)\s'
                        #12.(deprecated)genotype_depth 
                        r'([0-9,.e+-]+)\s'
                        #13.Generation 
                        r'([0-9,.e+-]+)\s'
                        #14.Neutral_metric 
                        r'([0-9,.e+-]+)\s'
                        #15.Lineage_label 
                        r'([0-9,.e+-]+)\s'
                        #16.True_Replication_Rate
                        #(based on births/update, time-averaged)
                        r'([0-9,.e+-]+)' 
                        % (evolved_run_length), 
                        final_update_line.group()
                        )
                    evolved_population_average_gestation = float(
                        #3. Gestation time
                        final_update_info.group(3)
                        )
                    evolved_population_average_length = float(
                        #7. Copied_size
                        final_update_info.group(7)
                        )
                    evolved_data_dict[gestation_key] = {
                        'trait': 'gestation', 
                        'evolved_population_value':
                                Decimal(evolved_population_average_gestation).log10(),
                        'raw_evolved_population_value':
                                Decimal(evolved_population_average_gestation)
                        }
                    evolved_data_dict[length_key] = {
                        'trait': 'genome_length', 
                        'evolved_population_value':
                                Decimal(evolved_population_average_length).log10(),
                        'raw_evolved_population_value':
                                Decimal(evolved_population_average_length)
                        }
    
    for key in list_of_keys:     
        data_dict[key] = dict(**run_data_dict[key], **evolved_data_dict[key])        

    date_time_year = (
        '\nDate, time, and year: %s \n' % (asctime(localtime(time())))
        )
    
    text = data_dict
    filename = str(project_folder) + '/logs/' +  log_name
    with open(filename, 'w+') as file:
        file.writelines([
            'Signator: J. Bundy', 
            str(date_time_year), ('\n'), 
            'The data_dict is:', ('\n'), 
            str(text)
            ])

    return data_dict

if __name__ == '__main__':
    create_data_dict(
        log_name= 'data_dict_phase2_average_gestation_and_average_length_log.txt'
        )
       