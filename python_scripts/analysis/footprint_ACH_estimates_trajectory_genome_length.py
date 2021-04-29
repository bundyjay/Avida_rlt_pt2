"""
Create the adaptation, chance, and history by depth trajectory plot.

function:: def create_estimates_trajectory_plot() -> str

This is S8 Fig.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from sys import path
from dfply import select, mask, X
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format
from pandas import CategoricalDtype, DataFrame, read_csv
from pathlib import Path
from plotnine import (
    aes, 
    element_blank, 
    element_line, 
    element_rect, 
    element_text, 
    facet_wrap, 
    geom_blank, 
    geom_line, 
    ggplot, 
    labeller, 
    labs, 
    scale_alpha_manual,
    scale_linetype_manual, 
    scale_x_continuous, 
    scale_y_continuous,
    theme) 
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = scripts_folder / 'operations'
project_folder = scripts_folder.parent
output_folder = project_folder / 'output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))

from fixed_precision import fixed_precision as fixed_precision
from label_title import label_title

font_path = (
    str(project_folder)
    + '/resources/fonts/Arial-Unicode-Regular.ttf')             
axis_title_properties = FontProperties(fname = font_path, size = 11)
text_properties = FontProperties(fname = font_path, size = 10)


def create_estimates_trajectory_plot():

    """
    Create adaptation, chance, and history estimates by depth plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: estimates_trajectory_plot location'
    :rtype: str
    """

    trait = 'genome_length'
    trait_label= 'genome length'  
    estimates_dataframe = read_csv(
        str(output_folder) 
        + '/ACH_trajectory_dataframe.csv')                                
    plot_dataframe = estimates_dataframe >> mask(X.trait == trait)
    
    """
    Create fake data to use with geom_blank for frame control.
    """
    environment_names = ([
        'orthogonal', 
        'orthogonal',
        'overlapping', 
        'overlapping'])
    value_description = ([
        'orthogonal_min', 
        'orthogonal_max', 
        'overlapping_min', 
        'overlapping_max'])
    value = [-.01, .04, -.01, .05]
    fake_data = ({
        'environment': environment_names, 
        'value_description': value_description, 
        'value': value}) 
    frame_data = DataFrame(fake_data) 

    """
    Determine 'order' and create a categorical type. 
    Or else the x-axis will be in alphabetical order. 
    We want Ancestral to be last
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    frame_data['environment_category'] = (
        frame_data['environment']
        .astype(str).astype(environment_category))
    
    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    plot_dataframe['environment_category'] = (
        plot_dataframe['environment']
        .astype(str).astype(environment_category))

    """
    Comment out geom_blank initially. 
    Run to view limits of y-axis.
    Then use desired limits as values for fake_data.
    """
    estimates_trajectory_plot = (
        ggplot(data=plot_dataframe, 
               mapping=aes(
                   x='time', 
                   y='value', 
                   color='factor(run_length)', 
                   group='series'))
        + geom_line(mapping=aes(
                        linetype='factor(source)', 
                        alpha='factor(source)'), 
                    size=1)
        + scale_linetype_manual(name='Source', 
                                values=['-', ':', '--', '-.'], 
                                labels=([
                                    'Adaptation', 
                                    'Ancestral',
                                    'Chance', 
                                    'History'])) 
        + scale_alpha_manual(values=[1, .5, 1, 1], 
                             labels=([
                                 'Adaptation', 
                                 'Ancestral',
                                 'Chance', 
                                 'History']))  
        + scale_x_continuous(name='Time (updates)', 
                             labels=currency_format(
                                 prefix='', 
                                 digits=0, 
                                 big_mark=','))
        + scale_y_continuous(labels = fixed_precision)      
        + labs(y= 'Contribution to log\u2081\u2080 %s' % (trait_label))
        + facet_wrap('~ environment_category', nrow=2, scales='free_y', 
                     labeller=labeller(environment_category=label_title))
        + geom_blank(data=frame_data, 
                     mapping=aes(y='value'), 
                     inherit_aes=False)
        + theme(figure_size=(5.2, 7),
                legend_position='none',
                text=element_text(fontproperties=text_properties),
                axis_title_x=element_text(
                    margin={'t': 12}, 
                    fontproperties=axis_title_properties
                    ), 
                axis_title_y=element_text(
                    margin={'r': 12}, 
                    fontproperties=axis_title_properties
                    ),
                axis_text_x=element_text(
                    margin={'t': 6}, 
                    color='black', 
                    size=10, 
                    fontproperties=text_properties
                    ),
                axis_text_y=element_text(
                    margin={'r': 6}, 
                    color='black', 
                    size=10, 
                    fontproperties=text_properties
                    ),
                axis_ticks_major_x=element_blank(),
                axis_ticks_major_y=element_blank(),
                rect=element_rect(color='white', size=3, fill='white'),
                plot_background=element_rect(fill='white'),
                panel_grid_major_y=element_line(
                    linetype='solid', 
                    color='black'
                    ),
                panel_spacing=.3))
    plot_location = (
        str(output_folder) 
        +'/masked/footprint_ACH_estimates_trajectory_bytrait/' 
        + 'footprint_ACH_estimates_trajectory_%s.pdf' % (trait))
    estimates_trajectory_plot.save(
        filename= plot_location)

    date_time_year = asctime(localtime(time()))

    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved image: %s' 
            % (
            date_time_year, 
            module_path, 
            plot_location))


if __name__ ==  '__main__':
    print(create_estimates_trajectory_plot())


