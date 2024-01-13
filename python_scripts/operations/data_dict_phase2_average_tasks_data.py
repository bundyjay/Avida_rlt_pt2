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

def create_data_dict(log_name= 'data_dict_phase2_log.txt'):

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

        tasks_key = (
            'ReplicateEnvironment%s_'
            'AncestorRunLength%s_'
            'AncestorSeed%s_'
            'ReplicateSeed%s_'
            'Tasks' 
            % (
                evolved_environment, 
                ancestor_run_length, 
                ancestor_seed, 
                evolved_seed
                ))
        rewards_key = (
            'ReplicateEnvironment%s_'
            'AncestorRunLength%s_'
            'AncestorSeed%s_'
            'ReplicateSeed%s_'
            'Rewards' 
            % (
                evolved_environment, 
                ancestor_run_length, 
                ancestor_seed, 
                evolved_seed
                ))
        nonrewards_key = (
            'ReplicateEnvironment%s_'
            'AncestorRunLength%s_'
            'AncestorSeed%s_'
            'ReplicateSeed%s_'
            'Nonrewards' 
            % (
                evolved_environment, 
                ancestor_run_length, 
                ancestor_seed, 
                evolved_seed
                ))
        
        list_of_keys.append(tasks_key) 
        list_of_keys.append(rewards_key) 
        list_of_keys.append(nonrewards_key) 
        run_data_dict[tasks_key] = {
            'evolved_run_length': evolved_run_length, 
            'run_length_unit': run_length_unit, 
            'ancestor_environment': ancestor_environment, 
            'evolved_environment': evolved_environment, 
            'ancestor_run_length': ancestor_run_length, 
            'ancestor_seed': ancestor_seed, 
            'evolved_seed' : evolved_seed
            }
        run_data_dict[rewards_key] = {
            'evolved_run_length': evolved_run_length, 
            'run_length_unit': run_length_unit, 
            'ancestor_environment': ancestor_environment, 
            'evolved_environment': evolved_environment, 
            'ancestor_run_length': ancestor_run_length, 
            'ancestor_seed': ancestor_seed, 
            'evolved_seed' : evolved_seed
            }
        run_data_dict[nonrewards_key] = {
            'evolved_run_length': evolved_run_length, 
            'run_length_unit': run_length_unit, 
            'ancestor_environment': ancestor_environment, 
            'evolved_environment': evolved_environment, 
            'ancestor_run_length': ancestor_run_length, 
            'ancestor_seed': ancestor_seed, 
            'evolved_seed' : evolved_seed
            }

        data_folder = input_folder + '/' + each_input_folder + '/data'    
        tasks_data_file_location = data_folder + '/tasks.dat'
        with open(tasks_data_file_location, 'r') as tasks_file:
            tasks_lines = tasks_file.readlines()
            for a_line in tasks_lines:

                final_update_line = search(
                    r'(^%d)\s.*\n' 
                    % (evolved_run_length), 
                    a_line
                    )
                if final_update_line:

                    final_update_info = search(
                        #  1: Update
                        r'(^%d)\s'
                        #  2: Not
                        r'([0-9,.e+-]+)\s'
                        #  3: Nand
                        r'([0-9,.e+-]+)\s'
                        #  4: And
                        r'([0-9,.e+-]+)\s'
                        #  5: OrNot
                        r'([0-9,.e+-]+)\s'
                        #  6: Or
                        r'([0-9,.e+-]+)\s'
                        #  7: AndNot
                        r'([0-9,.e+-]+)\s'
                        #  8: Nor
                        r'([0-9,.e+-]+)\s'
                        #  9: Xor
                        r'([0-9,.e+-]+)\s'
                        # 10: Equals
                        r'([0-9,.e+-]+)\s'
                        # 11: Logic 3AA (A+B+C == 0)
                        r'([0-9,.e+-]+)\s'
                        # 12: Logic 3AB (A+B+C == 1)
                        r'([0-9,.e+-]+)\s'
                        # 13: Logic 3AC (A+B+C <= 1)
                        r'([0-9,.e+-]+)\s'
                        # 14: Logic 3AD (A+B+C == 2)
                        r'([0-9,.e+-]+)\s'
                        # 15: Logic 3AE (A+B+C == 0,2)
                        r'([0-9,.e+-]+)\s'
                        # 16: Logic 3AF (A+B+C == 1,2)
                        r'([0-9,.e+-]+)\s'
                        # 17: Logic 3AG (A+B+C <= 2)
                        r'([0-9,.e+-]+)\s'
                        # 18: Logic 3AH (A+B+C == 3)
                        r'([0-9,.e+-]+)\s'
                        # 19: Logic 3AI (A+B+C == 0,3)
                        r'([0-9,.e+-]+)\s'
                        # 20: Logic 3AJ (A+B+C == 1,3) XOR
                        r'([0-9,.e+-]+)\s'
                        # 21: Logic 3AK (A+B+C != 2)
                        r'([0-9,.e+-]+)\s'
                        # 22: Logic 3AL (A+B+C >= 2)
                        r'([0-9,.e+-]+)\s'
                        # 23: Logic 3AM (A+B+C != 1)
                        r'([0-9,.e+-]+)\s'
                        # 24: Logic 3AN (A+B+C != 0)
                        r'([0-9,.e+-]+)\s'
                        # 25: Logic 3AO (A & ~B & ~C) [3]
                        r'([0-9,.e+-]+)\s'
                        # 26: Logic 3AP (A^B & ~C)  [3]
                        r'([0-9,.e+-]+)\s'
                        # 27: Logic 3AQ (A==B & ~C) [3]
                        r'([0-9,.e+-]+)\s'
                        # 28: Logic 3AR (A & B & ~C) [3]
                        r'([0-9,.e+-]+)\s'
                        # 29: Logic 3AS
                        r'([0-9,.e+-]+)\s'
                        # 30: Logic 3AT
                        r'([0-9,.e+-]+)\s'
                        # 31: Logic 3AU
                        r'([0-9,.e+-]+)\s'
                        # 32: Logic 3AV
                        r'([0-9,.e+-]+)\s'
                        # 33: Logic 3AW
                        r'([0-9,.e+-]+)\s'
                        # 34: Logic 3AX
                        r'([0-9,.e+-]+)\s'
                        # 35: Logic 3AY
                        r'([0-9,.e+-]+)\s'
                        # 36: Logic 3AZ
                        r'([0-9,.e+-]+)\s'
                        # 37: Logic 3BA
                        r'([0-9,.e+-]+)\s'
                        # 38: Logic 3BB
                        r'([0-9,.e+-]+)\s'
                        # 39: Logic 3BC
                        r'([0-9,.e+-]+)\s'
                        # 40: Logic 3BD
                        r'([0-9,.e+-]+)\s'
                        # 41: Logic 3BE
                        r'([0-9,.e+-]+)\s'
                        # 42: Logic 3BF
                        r'([0-9,.e+-]+)\s'
                        # 43: Logic 3BG
                        r'([0-9,.e+-]+)\s'
                        # 44: Logic 3BH
                        r'([0-9,.e+-]+)\s'
                        # 45: Logic 3BI
                        r'([0-9,.e+-]+)\s'
                        # 46: Logic 3BJ
                        r'([0-9,.e+-]+)\s'
                        # 47: Logic 3BK
                        r'([0-9,.e+-]+)\s'
                        # 48: Logic 3BL
                        r'([0-9,.e+-]+)\s'
                        # 49: Logic 3BM
                        r'([0-9,.e+-]+)\s'
                        # 50: Logic 3BN
                        r'([0-9,.e+-]+)\s'
                        # 51: Logic 3BO
                        r'([0-9,.e+-]+)\s'
                        # 52: Logic 3BP
                        r'([0-9,.e+-]+)\s'
                        # 53: Logic 3BQ
                        r'([0-9,.e+-]+)\s'
                        # 54: Logic 3BR
                        r'([0-9,.e+-]+)\s'
                        # 55: Logic 3BS
                        r'([0-9,.e+-]+)\s'
                        # 56: Logic 3BT
                        r'([0-9,.e+-]+)\s'
                        # 57: Logic 3BU
                        r'([0-9,.e+-]+)\s'
                        # 58: Logic 3BV
                        r'([0-9,.e+-]+)\s'
                        # 59: Logic 3BW
                        r'([0-9,.e+-]+)\s'
                        # 60: Logic 3BX
                        r'([0-9,.e+-]+)\s'
                        # 61: Logic 3BY
                        r'([0-9,.e+-]+)\s'
                        # 62: Logic 3BZ
                        r'([0-9,.e+-]+)\s'
                        # 63: Logic 3CA
                        r'([0-9,.e+-]+)\s'
                        # 64: Logic 3CB
                        r'([0-9,.e+-]+)\s'
                        # 65: Logic 3CC
                        r'([0-9,.e+-]+)\s'
                        # 66: Logic 3CD
                        r'([0-9,.e+-]+)\s'
                        # 67: Logic 3CE
                        r'([0-9,.e+-]+)\s'
                        # 68: Logic 3CF
                        r'([0-9,.e+-]+)\s'
                        # 69: Logic 3CG
                        r'([0-9,.e+-]+)\s'
                        # 70: Logic 3CH
                        r'([0-9,.e+-]+)\s'
                        # 71: Logic 3CI
                        r'([0-9,.e+-]+)\s'
                        # 72: Logic 3CJ
                        r'([0-9,.e+-]+)\s'
                        # 73: Logic 3CK
                        r'([0-9,.e+-]+)\s'
                        # 74: Logic 3CL
                        r'([0-9,.e+-]+)\s'
                        # 75: Logic 3CM
                        r'([0-9,.e+-]+)\s'
                        # 76: Logic 3CN
                        r'([0-9,.e+-]+)\s'
                        # 77: Logic 3CO
                        r'([0-9,.e+-]+)\s'
                        # 78: Logic 3CP
                        r'([0-9,.e+-]+)' 
                        % (evolved_run_length), 
                        final_update_line.group()
                        )
                    tasks_list = [
                        int(s) for s in final_update_info.group()
                        .split(' ')
                        ]
                    # original_list = [
                    #     int(s) for s in final_update_info.group()
                    #     .split(' ')
                    #     ]
  
                    # tasks_list = tasks_list[:12]
                    # original_list = original_list[:12]
                    
                    tasks_list.pop(0) #remove update number
                    tasks_list.pop(8) #remove tally for Equals (EQU)
  
                    # print('original: ', original_list)
                    # print('tasks: ', tasks_list)
                    
                    # print('environment: ', evolved_environment)
                    
                    tasks_total = sum(tasks_list[:]) 
                    # print('total: ', tasks_total)

                    evolved_data_dict[tasks_key] = {
                        'trait': 'total_tasks', 
                        'evolved_population_value' : tasks_total
                        }
                    
                    if evolved_environment == 'orthogonal':
                        # print('orthogonal')
                        
                        rewards = sum(tasks_list[0::2])
                        # print('rewards: ', rewards)                        

                        evolved_data_dict[rewards_key] = {
                            'trait': 'rewards', 
                            'evolved_population_value' : rewards
                            }
                
                        # unrewarded_tasks = tasks_total - rewards                

                    if evolved_environment == 'overlapping':
                        # print('overlapping') 

                        rewards = sum(tasks_list[:])
                        # print('rewards: ', rewards)       

                        evolved_data_dict[rewards_key] = {
                            'trait': 'rewards', 
                            'evolved_population_value' : rewards
                            }
                  
                 
                        # tasks_total = sum(tasks_list[:]) 
                        # print('total: ', tasks_total)   
        
                    
                    unrewarded_tasks = tasks_total - rewards
                    # print('unrewarded: ', unrewarded_tasks)                 
              
                    evolved_data_dict[nonrewards_key] = {
                        'trait': 'unrewarded_tasks', 
                        'evolved_population_value' : unrewarded_tasks
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
        log_name= 'data_dict_phase2_total_tasks_and_average_length_log.txt'
        )
       