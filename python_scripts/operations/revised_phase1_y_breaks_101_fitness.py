"""
Custom breaks

function:: def revised_phase1_y_breaks(breaks: tuple) -> list
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from decimal import Decimal, ROUND_UP
from math import modf
import numpy as np
from time import asctime, localtime, time

     
def revised_phase1_y_breaks(breaks):
    """
    Return custom values for the axis.

    :param str breaks: Provide breaks to alter.
    :return: breaks (capitalized without underscores)
    :rtype: str
    """
    
    new_breaks = breaks
    print(breaks)
    minimum=min(breaks)
    print(minimum)
    # new_breaks = [.01, 10, 10000, 10000000, 10000000000]
    new_breaks = [.1, 1, 10, 100, 1000]

    # if minimum == 4.46683592e-04 :
    #     new_breaks = [.01, 10, 10000, 10000000, 10000000000]

    # if minimum == 67.86655031756403:
    #     new_breaks = [80, 90, 100, 110, 120]
    # maximum=max(breaks)

    return new_breaks
 
if __name__ == '__main__':

    date_time_year = asctime(localtime(time())) 
    print('Date, time, and year:', date_time_year)
    
    input_lists = [
        [1.8, 1.9000000000000001, 2.0, 2.1], 
        [0.0, 5.0, 10.0, 15.0, 20.0], 
        [32.03456, 32.03455, 32.03450, 12.325, 006.25, 19.0005, 19.0006, 56.00]
        ]
        
    for input_list in input_lists:
        print('input_list:', input_list)
        print('breaks_list:', revised_phase1_y_breaks(input_list))

