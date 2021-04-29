"""
Capitalize labels (title-case) and remove underscores.

function:: def label_title(label: str) -> str
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from decimal import Decimal
from math import modf
import numpy as np
from time import asctime, localtime, time

     
def fixed_precision(label):

    """
    Return custom values for the axis.

    :param str label: Provide label to alter.
    :return: label (capitalized without underscores)
    :rtype: str
    """
    new_values = []
    cutoff = 3 
    label = list(label)
    decimals = [round(modf(val)[0], cutoff) for val in label]
    max_precision = max(
        [len(str(dec).split(".")[1]) 
        if dec > 0 else 0 
        for dec in decimals])

    for value in label:
        new_values.append("%0.*f" % (max_precision, value))
           
    return new_values
 
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
        print('label_list:', fixed_precision(input_list))

