"""
Find subfolders when given an output folder.

function:: def find_subfolders(output_folder: str, log: bool) 
               yields subfolder.name

Run to find data subfolders while excluding qsub_files.
"""
__author__ = 'Jason Bundy'
__version__ = '1.0'


from os import scandir, path
from pathlib import Path
from sys import path
from time import asctime, localtime, time

def find_subfolders(output_folder, log = True):

    """
    Find output folder subfolders.
    :param str output_folder: Contain data subfolders.
    :param bool log: Log the subfolders.
    :yields: str subfolder.name
    :rtype: str
    """

    try:
        with scandir(output_folder) as output:
            for subfolder in output:
                if subfolder.is_dir() and subfolder.name != 'qsub_files':
                    yield subfolder.name      
    except IOError:
        return 'EXCEPTION: find_subfolders'


if __name__ == '__main__':  

    module_path = Path(__file__).resolve()
    operations_folder = module_path.parent
    scripts_folder = operations_folder.parent
    project_folder = scripts_folder.parent
    path.insert(0, str(scripts_folder))

    output_folder = (
        '/Volumes/bundyjas/ACH_Development/ACH_tests/ACH_quiz3/output_phase1'
        )
    output_folder = str(project_folder) + '/output_phase1'
    subfolders= sorted(list(find_subfolders(output_folder))) 
    
    date_time_year = asctime(localtime(time()))
    
    print(
        'Date, time, and year:', 
        date_time_year, 
        '\n',
        'Subfolders: \n', 
        subfolders
        )

    text ='\n'.join(subfolders)
    filename = str(project_folder) + '/logs/' + 'find_subfolders_log' + '.txt'
    with open(filename, 'w+') as file:
        file.writelines([
            'Signator: J. Bundy', ('\n'),
            'Date, time, and year:', ('\n'),
            date_time_year, ('\n'), 
            'Operations: (1) find_subfolders', ('\n'), 
            'Found subdirectories within: ', 
            str(output_folder), ('\n'), 
            'The subdirectories are:', ('\n'), 
            str(text), ('\n' * 2), 
            'Formatted list of (same) subdirectory names:', ('\n'), 
            str(subfolders)
            ])
          
    
