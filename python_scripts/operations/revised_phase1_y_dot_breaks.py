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
    minimum=min(breaks)
    if minimum == -3.125:
        new_breaks = [-2.5, 0, 2.5, 5, 7.5, 10]

    if minimum == 1.8924999999999998:
        new_breaks = [1.90, 1.95, 2, 2.05]
    maximum=max(breaks)
    
    # print('breaks: ', breaks)
    # print('minimum: ', minimum)

    
    return new_breaks
 
if __name__ == '__main__':

    date_time_year = asctime(localtime(time())) 
    print('Date, time, and year:', date_time_year)
    
    input_lists = [
        [1.8, 1.9000000000000001, 2.0, 2.1], 
        [0.0, 5.0, 10.0, 15.0, 20.0], 
        [32.03456, 32.03455, 32.03450, 12.325, 006.25, 19.0005, 19.0006, 56.00]
        ]
        
    # for input_list in input_lists:
    #     print('input_list:', input_list)
    #     print('breaks_list:', revised_phase1_y_breaks(input_list))

