"""
Capitalize labels (title-case) and remove underscores.

function:: def label_title(label: str) -> str
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from time import asctime, localtime, time
     
def label_title(label):

    """
    Capitalize labels (title-case).

    :param str label: Provide label to alter.
    :return: label (capitalized without underscores)
    :rtype: str
    """
    label= label.replace('_', ' ').capitalize()
    return label
 
if __name__ == '__main__':
    
    input_string = 'make_This_a_title.'
    test_title= label_title(input_string)

    date_time_year = asctime(localtime(time())) 

    print('Date, time, and year:', date_time_year)
    print('input string:', input_string)
    print('label_title:', test_title)