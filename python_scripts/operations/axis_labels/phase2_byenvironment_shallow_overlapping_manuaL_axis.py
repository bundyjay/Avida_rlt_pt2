"""
Capitalize labels (title-case) and remove underscores.

function:: def label_title(label: str) -> str
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from time import asctime, localtime, time
import numpy as np

     
def manual_axis(label):

    """
    Return custom values for the axis.

    :param str label: Provide label to alter.
    :return: label (capitalized without underscores)
    :rtype: str
    """

    label = list(label)
    a = [0.0, 5.0, 10.0, 15.0, 20.0]
    b = [1.8, 1.9000000000000001, 2.0, 2.1]
    if label == a:
        label = [0, 5, 10, 15, 20]    
    if label == b:
        label = [1.8, 1.9, 2.0, 2.1]
        
    return label
 
if __name__ == '__main__':
    
    input_list = [1.8, 1.9000000000000001, 2.0, 2.1]
    test_title= manual_axis(input_list)

    date_time_year = asctime(localtime(time())) 

    print('Date, time, and year:', date_time_year)
    print('input string:', input_string)
    print('label_title:', test_title)