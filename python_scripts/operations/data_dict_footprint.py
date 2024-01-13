"""
Create the data_dict for Phase 2.

function:: def create_data_dict(log_name: str) -> dict

Logic of function:

How the make the Phase 2 trajectory:
1. Look into the folder of each run (output_phase2).
2. Find the ancestral fitness and genome length.
3. Record it for the entire series.
4. Also record it for update 0 evolved values.
5. Record the values for the other updates in the trajectory.
6. Look at the average data file. (Update 0 values are inaccurate.)
7. Record the value for all other updates in the trajectory.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from collections import defaultdict
from decimal import Decimal
from math import log10 as log10
from os import listdir, path
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
input_folder = str(project_folder) + '/output_phase2'
input_subfolders = list(find_subfolders(input_folder))


def create_data_dict(log_name='data_dict_footprint_log.txt'):
    
    '''
    Create the data_dict.

    :param str log_name: Name the log.
    :return: data_dict
    :rtype: dict
    '''

    data_dict = defaultdict(dict)
    trajectory_updates = [100000] 
    for each_input_folder in input_subfolders: 
        current_directory = each_input_folder
        """Example string to serve as pattern (template) 
        for run_info search below: (directory names)

        ReplicateEnv38tasksnoequodd10k_
        AncestorSeed102Env38tasksnoequeven4k_
        1002

        or

        ReplicateEnv76tasksnoequ10k_
        AncestorSeed101Env38tasksnoequeven4k_
        1001
        """        
        run_info = search(
            # e.g. 'ReplicateEnv38tasksnoequodd'
            # -> new environment 
            r'ReplicateEnv([\d]+)([a-z]+)'
            # e.g. '10k_'
            # -> evolved run length
            r'([\d]+)k_'
            # e.g.'AncestorSeed102'
            # -> lineage  
            r'AncestorSeed([\d]+)'
            #'Env38tasksnoequeven'
            # -> old environment
            r'Env([\d]+)([a-z]+)'
            # e.g. '4k_'
            #-> depth
            r'([\d]+)k_'
            # e.g. '1002'
            # -> seed
            r'([\d]+)' , each_input_folder
            )
        seed = run_info.group(8)
        replicate_environment = run_info.group(1) + run_info.group(2)
        if replicate_environment == '38tasksnoequodd':
            environment = 'orthogonal'
        if replicate_environment == '76tasksnoequ':
            environment = 'overlapping'
        evolved_run_length_in_k = run_info.group(3)
        lineage = run_info.group(4)
        ancestor_environment = run_info.group(5) + run_info.group(6)
        depth = int(run_info.group(7)) * 1000
        depth_in_k = run_info.group(7)
        ancestor_length = None
        ancestor_fitness = None
        ancestor_found = False

        archive_directory = (
            input_folder 
            + '/' 
            + each_input_folder 
            + '/data/archive'
            )
        for each_file in listdir(archive_directory):
            file_location =  (
                input_folder 
                + '/' 
                + each_input_folder 
                + '/data/archive/' 
                + each_file
                )
            ancestor_file = each_file.endswith(r'-aaaaa.org')
            if ancestor_file:
                location =(
                    input_folder 
                    + '/' 
                    + each_input_folder 
                    + '/data/archive/' 
                    + each_file
                    )
                with open(str(location), 'r+') as saved_organism_file:
                    lines = saved_organism_file.readlines()
                    for line in lines:
                        #Check to make sure file is from update=0
                        update_0_organism = search(
                            r'Update Output\.\.\.: 0\n', 
                            line
                            )
                        if update_0_organism:
                            for line in lines:

                                ancestor_fitness_line = (
                                    search(
                                        r'Fitness\.\.\.\.\.\.\.\.\.: '
                                        r'([0-9,.e+]+)\n', line
                                        ))
                                if ancestor_fitness_line:
                                    ancestor_fitness = Decimal(
                                        ancestor_fitness_line.group(1)
                                        ) 
                                ancestor_length_line = search(
                                    r'Copied Size.....: ([0-9,.e+]+)\n', 
                                    line
                                    )
                                if ancestor_length_line:
                                    ancestor_length = Decimal(
                                        ancestor_length_line.group(1)
                                        )
                                else: pass
                            ancestor_found = True
                        else:
                            pass
            else: pass

        if ancestor_fitness is None:
            keys_from_same_ancestor= []
            for each_input_folder in input_subfolders:
                ancestor_match = search(
                        # e.g.'ReplicateEnv38tasksnoequodd10k_'
                        # -> new environment
                        r'ReplicateEnv%s%sk_'
                        # e.g.'AncestorSeed102Env38tasksnoequeven4k_'
                        # ->old environment w/ depth
                        r'AncestorSeed%sEnv%s%sk_'
                        # e.g.'1002'
                        # ->seed
                        r'([\d]+)' 
                    % (
                        replicate_environment, 
                        evolved_run_length_in_k, 
                        lineage, 
                        ancestor_environment, 
                        depth_in_k
                        ), 
                    each_input_folder
                    )
                if ancestor_match:
                    keys_from_same_ancestor.append(
                        ancestor_match.group()
                        )
            keys_from_same_ancestor.remove(current_directory)
            for each_key in keys_from_same_ancestor:
                if  ancestor_found == False:
                    alternate_archive_directory = (input_folder 
                    + '/' 
                    + each_key 
                    + '/data/archive'
                    )
                    for each_alternate_file in listdir(
                            alternate_archive_directory
                        ):

                        alternate_file_location =  (
                            input_folder 
                            + '/' 
                            + each_key 
                            + '/data/archive/' 
                            + each_alternate_file
                            )
                        with open(alternate_file_location, 'r+')  \
                                as alternate_saved_organism_file:
                            alternate_lines = (
                                alternate_saved_organism_file.readlines()
                                )
                            for alt_line in alternate_lines:
                                update_0_organism = search(
                                    r'Update Output\.\.\.: 0\n', 
                                    alt_line
                                    )
                                if update_0_organism:
                                    for alt_line in alternate_lines:
                                        ancestor_fitness_line = search(
                                                r'Fitness'
                                                r'\.\.\.\.\.\.\.\.\.: '
                                                r'([0-9,.e+]+)\n', 
                                            alt_line
                                            )
                                        if ancestor_fitness_line:
                                            ancestor_fitness = Decimal(
                                                ancestor_fitness_line.group(1)
                                                )
                                        ancestor_length_line = search(
                                                r'Copied Size'
                                                r'\.\.\.\.\.: '
                                                r'([0-9,.e+]+)\n', 
                                            alt_line
                                            )
                                        if ancestor_length_line:
                                            ancestor_length = (
                                                Decimal(
                                                    (ancestor_length_line
                                                    .group(1))
                                                    ))
                                        else: pass
                                    ancestor_found = True
                                else: pass 

        for each_update in trajectory_updates:
        
            update = int(each_update)
            fitness_key = (
                'Environment%s_'
                'Depth%s_'
                'AncestorSeed%s_'
                'ReplicateSeed%s_'
                'Update%s_'
                'Fitness' 
                % (
                    environment, 
                    depth, 
                    lineage, 
                    seed, 
                    update
                    ))
            fitness_series = (
                'Environment_%s_'
                'RunLength_%s_'
                'Lineage_%s_'
                'Replicate_%s_'
                'Trait_Fitness' 
                %(
                    environment, 
                    depth, 
                    lineage, 
                    seed
                    ))
            data_dict[fitness_key].update({
                'series': fitness_series, 
                'environment': environment, 
                'depth': depth ,
                'lineage': lineage,
                'replicate': seed, 
                'time': update, 
                'trait': 'fitness', 
                'ancestor_value': ancestor_fitness, 
                'ancestor_value_log10': ancestor_fitness.log10()
                })
            length_key = (
                'Environment%s_'
                'Depth%s_'
                'AncestorSeed%s_'
                'ReplicateSeed%s_'
                'Update%s_'
                'Length' 
                % (
                    environment, 
                    depth, 
                    lineage, 
                    seed, 
                    update
                    ))
            length_series = (
                'Environment_%s_'
                'RunLength_%s_'
                'Lineage_%s_'
                'Replicate_%s_'
                'Trait_Length' 
                %(
                    environment, 
                    depth, 
                    lineage, 
                    seed
                    ))
            data_dict[length_key].update({
                'series': length_series, 
                'environment': environment,
                'depth': depth ,
                'lineage': lineage,
                'replicate': seed, 
                'time': update, 
                'trait': 'genome_length', 
                'ancestor_value': ancestor_length, 
                'ancestor_value_log10': ancestor_length.log10()
                })
        
    for each_input_folder in input_subfolders:

        run_info = search(
            # e.g. 'ReplicateEnv38tasksnoequodd'
            # -> new environment 
            r'ReplicateEnv([\d]+)([a-z]+)'
            # e.g. '10k_'
            # -> evolved run length
            r'([\d]+)k_'
            # e.g.'AncestorSeed102'
            # -> lineage  
            r'AncestorSeed([\d]+)'
            #'Env38tasksnoequeven'
            # -> old environment
            r'Env([\d]+)([a-z]+)'
            # e.g. '4k_'
            #-> depth
            r'([\d]+)k_'
            # e.g. '1002'
            # -> seed
            r'([\d]+)' , each_input_folder
            )
        seed = run_info.group(8)
        replicate_environment = run_info.group(1) + run_info.group(2)
        if replicate_environment == '38tasksnoequodd':
            environment = 'orthogonal'
        if replicate_environment == '76tasksnoequ':
            environment = 'overlapping'
        evolved_run_length_in_k = run_info.group(3)
        lineage = run_info.group(4)
        ancestor_environment = run_info.group(5) + run_info.group(6)
        depth = int(run_info.group(7)) * 1000
        depth_in_k = run_info.group(7)
        ancestor_length = None
        ancestor_fitness = None
        ancestor_found = False

        data_directory = (
            input_folder 
            + '/' 
            + each_input_folder 
            + '/data'
            )  
        average_data_file_location = data_directory + '/average.dat'
        with open(average_data_file_location, 'r') as average_file:
            average_lines = average_file.readlines()
            for a_line in average_lines:
                #print('a_line:', a_line)
                data_line = search(
                    # 1.Update 
                    (r'([0-9,.e+-]+)\s'
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
                    r'([0-9,.e+-]+) \n'), 
                    a_line
                    )

                if data_line:
                    update= int(data_line.group(1))
                    if update in trajectory_updates:

                        length_key = (
                            'Environment%s_'
                            'Depth%s_'
                            'AncestorSeed%s_'
                            'ReplicateSeed%s_'
                            'Update%s_'
                            'Length' 
                            % (
                                environment, 
                                depth, 
                                lineage, 
                                seed, 
                                update
                                ))
                        fitness_key = (
                            'Environment%s_'
                            'Depth%s_'
                            'AncestorSeed%s_'
                            'ReplicateSeed%s_'
                            'Update%s_'
                            'Fitness' % (
                                environment, 
                                depth, 
                                lineage, 
                                seed, 
                                update
                                ))

                        if update == 0:
                            data_dict[fitness_key].update({
                                'evolved_population_average_value': (
                                    data_dict[fitness_key]['ancestor_value']
                                    ), 
                                'evolved_population_average_value_log10': ((
                                    data_dict[fitness_key]
                                    ['ancestor_value_log10']
                                    )), 
                                'evolved_relative_value': (
                                    (data_dict[fitness_key]['ancestor_value'])
                                    /
                                    (data_dict[fitness_key]['ancestor_value'])
                                    ),
                                'evolved_relative_value_log10': ((
                                    data_dict[fitness_key]['ancestor_value'
                                    ])
                                    /(
                                        data_dict[fitness_key]
                                        ['ancestor_value']
                                        ))
                                    .log10()
                                    })
                            data_dict[length_key].update({
                                'evolved_population_average_value': (
                                    data_dict[length_key]['ancestor_value']
                                    ), 
                                'evolved_population_average_value_log10': ((
                                    data_dict
                                    [length_key]['ancestor_value_log10']
                                    )), 
                                'evolved_relative_value': (
                                    (data_dict[length_key]['ancestor_value'])
                                    /
                                    (data_dict[length_key]['ancestor_value'])
                                    ), 
                                'evolved_relative_value_log10': ((
                                    data_dict[length_key]['ancestor_value'])
                                    /(
                                        data_dict
                                        [length_key]['ancestor_value']
                                        ))
                                    .log10()
                                    })

                        else:
                            evolved_population_average_fitness = (
                                Decimal(data_line.group(4))
                                )
                            data_dict[fitness_key].update({
                                'evolved_population_average_value': 
                                    evolved_population_average_fitness, 
                                'evolved_population_average_value_log10': 
                                    (
                                        evolved_population_average_fitness
                                            .log10()
                                        ),
                                'evolved_relative_value':  (
                                    (evolved_population_average_fitness)
                                    /
                                    (data_dict[fitness_key]['ancestor_value'])
                                    ), 
                                'evolved_relative_value_log10': (
                                        (evolved_population_average_fitness)
                                        /
                                        (
                                        data_dict[fitness_key]
                                            ['ancestor_value']
                                            ))
                                        .log10(),
                                'evolved_difference': (
                                    (evolved_population_average_fitness) 
                                    - 
                                    (data_dict[fitness_key]['ancestor_value']) 
                                    ),
                                'evolved_log10_difference': (
                                    ((evolved_population_average_fitness)
                                        .log10())
                                    -
                                    ((
                                    data_dict[fitness_key]
                                        ['ancestor_value']
                                        )
                                        .log10())
                                    )
                                })
                            evolved_population_average_copied_size = Decimal(
                                data_line.group(7)
                                )
                            data_dict[length_key].update({
                                'evolved_population_average_value': 
                                    evolved_population_average_copied_size, 
                                'evolved_population_average_value_log10': (
                                    evolved_population_average_copied_size
                                    .log10()
                                    ), 
                                'evolved_difference': (
                                    (evolved_population_average_copied_size)
                                    -
                                    (data_dict[length_key]['ancestor_value'])
                                    ),
                                'evolved_log10_difference': (
                                    ((evolved_population_average_copied_size)
                                        .log10())
                                    -
                                    ((data_dict[length_key]['ancestor_value'])
                                        .log10())
                                    ),                                                                        
                                'evolved_relative_value': (
                                    (evolved_population_average_copied_size)
                                    /
                                    (data_dict[length_key]['ancestor_value'])
                                    ),  
                                'evolved_relative_value_log10': (
                                    (evolved_population_average_copied_size)
                                    /
                                    (data_dict[length_key]['ancestor_value'])
                                    )
                                    .log10()
                                })

    date_time_year = (
        '\nDate, time, and year: %s \n' 
        % (asctime(localtime(time())))
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
    create_data_dict(log_name='data_dict_footprint_log.txt')
