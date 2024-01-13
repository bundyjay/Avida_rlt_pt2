"""
Create the Phase 1 total tasks and average length dict.

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

input_folder= str(project_folder) + '/output_phase1'
input_folders = list(find_subfolders(input_folder))


def create_data_dict(
    log_name='data_dict_phase1_ttest_log.txt'
    ):

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
    depths= [20000, 500000]  

    for each_input_folder in input_folders: 
        for each_depth in depths:      
            """
            Example string to serve as pattern (template): 
            Ancestors_Env_38tasks_noequ_even_
            50k_
            101
            """  
            run_info = search(
                r'Ancestors_Env_([\d]+)([a-z]+)_([a-z]+)_([a-z]+)_'
                r'([\d]+)k_'
                r'([\d]+)', 
                each_input_folder
                )
            ancestor_environment = (
                run_info.group(1) 
                + run_info.group(2) 
                + run_info.group(3) 
                + run_info.group(4)
                )
            ancestor_run_length = int(run_info.group(5)) * 1000
            ancestor_seed = run_info.group(6)
            depth = each_depth

            fitness_key = (
                'AncestorRunLength%s_'
                'AncestorEnvironment%s_'
                'AncestorSeed%s_'
                'Fitness' 
                % (
                    ancestor_run_length, 
                    ancestor_environment, 
                    ancestor_seed
                    ))
            list_of_keys.append(fitness_key) 
            run_data_dict[fitness_key] = {
                'ancestor_seed': ancestor_seed,
                'trait': 'average_fitness',
                }
            length_key = (
                'AncestorRunLength%s_'
                'AncestorEnvironment%s_'
                'AncestorSeed%s_'
                'Length' 
                % (
                    ancestor_run_length, 
                    ancestor_environment,
                    ancestor_seed
                    ))
            list_of_keys.append(length_key) 
            run_data_dict[length_key] = {
                'ancestor_seed': ancestor_seed,
                'trait': 'average_genome_length',
                }

            data_directory = input_folder + '/' + each_input_folder + '/data'    
            average_data_file_location = data_directory + '/average.dat'
            with open(average_data_file_location, 'r') as average_file:
                average_lines = average_file.readlines()
                for a_line in average_lines:
                    depth_update_line = search(r'(^%d)\s.*\n' % (depth), a_line)
                    if depth_update_line:
                        depth_update_info = search(
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
                            % (depth), 
                            depth_update_line.group()
                            )

                        if depth == 20000:
                            evolved_population_average_fitness = float(
                                #4.Fitness 
                                Decimal(depth_update_info.group(4)).log10()
                                )
                            evolved_data_dict[fitness_key]['shallow_evolved_population_value_log10'] = evolved_population_average_fitness 

                            evolved_population_average_length = float(
                                #7. Copied_size
                                Decimal(depth_update_info.group(7)).log10()
                                )
                            evolved_data_dict[length_key]['shallow_evolved_population_value_log10'] = evolved_population_average_length

                        if depth == 500000:
                            evolved_population_average_fitness = float(
                                #4.Fitness 
                                Decimal(depth_update_info.group(4)).log10()
                                )
                            evolved_data_dict[fitness_key]['deep_evolved_population_value_log10'] = evolved_population_average_fitness 

                            evolved_population_average_length = float(
                                #7. Copied_size
                                Decimal(depth_update_info.group(7)).log10()
                                )
                            evolved_data_dict[length_key]['deep_evolved_population_value_log10'] = evolved_population_average_length


    for key in list_of_keys:
        data_dict[key] = dict(**run_data_dict[key], **evolved_data_dict[key])        

    date_time_year = (
        '\nDate, time, and year: %s \n' % (asctime(localtime(time())))
        )
    text = data_dict
    filename = str(project_folder) + '/logs/' + log_name 
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
        log_name='data_dict_phase1_ttest_log.txt'
        )   