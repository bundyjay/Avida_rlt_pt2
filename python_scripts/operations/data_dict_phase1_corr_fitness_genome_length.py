"""
Create the data_dict for Phase 1.

function:: def create_data_dict(log_name: str) -> dict
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

from find_subfolders import find_subfolders as find_subfolders

input_folder= str(project_folder) + '/output_phase1'
input_folders = list(find_subfolders(input_folder))


def create_data_dict(log_name='data_dict_phase1_log.txt'):

    '''
    Create the data_dict.

    :param str log_name: Name the log.
    :return: data_dict
    :rtype: dict
    '''

    data_dict = defaultdict(dict)
    trajectory_updates = [x for x in range(0,501000,1000)]

    for each_folder in input_folders:       
            """
            Example string to serve as run_info pattern: 
            'Ancestors_Env_38tasks_noequ_even_
            '50k_'
            '101'
            """  
            run_info = search(
                # e.g.'Ancestors_Env_38tasks_noequ_even_'
                # -> environment
                r'Ancestors_Env_([\d]+)([a-z]+)_([a-z]+)_([a-z]+)_'
                # e.g.'500k_'
                # -> depth (run_length) 
                r'([\d]+)k_'
                #'101'
                # -> 'lineage'
                r'([\d]+)', 
                each_folder
                )
            lineage = run_info.group(6)

            for each_update in trajectory_updates: 
                update = int(each_update)
                run_key = (
                    'Seed%s_Update%s' 
                    % (lineage, update)
                    )

            """
            Read and store the run information 
            with the ancestor values.
            Stores the same values from Avida for all updates.
            """
            archive_folder = (
                input_folder 
                + '/' 
                + each_folder 
                + '/data/archive'
                )
            for each_file in listdir(archive_folder):
                file_path =  (
                    input_folder 
                    + '/' 
                    + each_folder 
                    + '/data/archive/' 
                    + each_file
                    )
                with open(file_path, 'r+') as saved_organism_file:
                    lines = saved_organism_file.readlines()
                    for line in lines:
                        update_0_organism = search(
                            r'Update Output\.\.\.: 0\n', 
                            line
                            )
                        if update_0_organism:
                            for line in lines:
                                fitness_line = search(
                                    r'Fitness\.\.\.\.\.\.\.\.\.:' 
                                    + r' ([0-9,.e+]+)\n', 
                                    line)
                                if fitness_line:
                                    fitness = Decimal(
                                        fitness_line.group(1)
                                        )
                                genome_length_line = search(
                                    r'Copied Size\.\.\.\.\.:' 
                                    + r' ([0-9,.e+]+)\n', line)
                                if genome_length_line:
                                    genome_length = Decimal(
                                        genome_length_line.group(1)
                                        )
                                else: pass
                        else: pass

            for each_update in trajectory_updates: 
                update = int(each_update)
                run_key = (
                    'Seed%s_Update%s' 
                    % (lineage, update)
                    )
                lineage_series = '%s' % (lineage)
                time_series = '%s' % (update)
                data_dict[run_key] = ({ 
                    'lineage_series': lineage_series, 
                    'time_series': time_series, 
                    'lineage': lineage, 
                    'time': update,  
                    'fitness_ancestor_value': fitness, 
                    'fitness_ancestor_value_log10': fitness.log10(),
                    'genome_length_ancestor_value': genome_length, 
                    'genome_length_ancestor_value_log10': genome_length.log10()
                    })
            
            """
            Read and store the evolved population data.
            Stores unique information from Avida for each update.
            """
            data_folder = (
                input_folder 
                + '/' 
                + each_folder 
                + '/data'
                )    
            average_file_path = data_folder + '/average.dat'
            for each_update in trajectory_updates:
                update = int(each_update)
                if each_update == 0:    
                    run_key = (
                        'Seed%s_Update%s' 
                        % (lineage, update)
                        )
                    data_dict[run_key].update({
                        'fitness_average_value': 
                        data_dict[run_key]['fitness_ancestor_value'], 
                        'fitness_average_value_log10': 
                        log10(data_dict[run_key]['fitness_ancestor_value'])
                        })
                    data_dict[run_key].update({
                        'genome_length_average_value': 
                        data_dict[run_key]['genome_length_ancestor_value'], 
                        'genome_length_average_value_log10': 
                        log10(data_dict[run_key]['genome_length_ancestor_value'])
                        })
                else:
                    run_key = (
                        'Seed%s_Update%s' 
                        % (lineage, update)
                        )
                    # length_key = (
                    #     'Depth%s_Seed%s_Update%s_Length' 
                    #     % (depth, lineage, update)
                    #     )            
                    with open(average_file_path, 'r') as average_file:
                        average_lines = average_file.readlines()
                        for a_line in average_lines:
                            update_line = search(
                                # 1.Update 
                                (r'(^%d)\s'
                                # 2.Merit 
                                r'([0-9,.e+-]+)\s'
                                # 3.Gestation_Time 
                                r'([0-9,.e+-]+)\s'
                                # 4.Fitness 
                                r'([0-9,.e+-]+)\s'
                                # 5.Repro_Rate? 
                                r'([0-9,.e+-]+)\s'
                                # 6.(deprecated)size 
                                r'([0-9,.e+-]+)\s'
                                # 7.Copied_Size 
                                r'([0-9,.e+-]+)\s'
                                # 8.Executed_Size 
                                r'([0-9,.e+-]+)\s'
                                # 9.(deprecated)abundance 
                                r'([0-9,.e+-]+)\s'
                                # 10.Proportion_giving_birth
                                # _this_update 
                                r'([0-9,.e+-]+)\s'
                                # 11.Proportion_breed_true 
                                r'([0-9,.e+-]+)\s'
                                # 12.(deprecated)genotype_depth 
                                r'([0-9,.e+-]+)\s'
                                # 13.Generation 
                                r'([0-9,.e+-]+)\s'
                                # 14.Neutral_metric 
                                r'([0-9,.e+-]+)\s'
                                # 15.Lineage_label 
                                r'([0-9,.e+-]+)\s'
                                # 16.True_Replication_Rate
                                # (based on births/update,
                                # time-averaged)"""
                                r'([0-9,.e+-]+) \n') 
                                % (update), 
                                a_line
                                )
                            if update_line:
                                    fitness = (
                                    Decimal(update_line.group(4))
                                    )
                                    data_dict[run_key].update({
                                        'fitness_average_value': 
                                            fitness, 
                                        'fitness_average_value_log10': 
                                            fitness.log10()
                                            })
                                    genome_length = (
                                    Decimal(update_line.group(7))
                                    )
                                    data_dict[run_key].update({
                                        'genome_length_average_value': 
                                            genome_length, 
                                        'genome_length_average_value_log10': 
                                            str(genome_length.log10())
                                            })
                  
    """
    Log the data dict.
    """
    date_time_year = asctime(localtime(time()))
    text = data_dict
    filename = (
        str(project_folder) 
        + '/logs/' + log_name
        ) 
    with open(filename, 'w+') as file:
        file.writelines([
            'Date, time, and year: %s \n' % date_time_year,
            'Signator: J. Bundy', 
            '\n\n', 
            'The data_dict is:', 
            '\n', 
            str(text)
            ])

    return data_dict


if __name__ == '__main__':
    create_data_dict(log_name='data_dict_phase1_corr_fitness_genome_length_log.txt')  
