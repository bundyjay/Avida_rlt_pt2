"""
Combine genome length and fitness correlation graphs.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

import patchworklib as pw 
from plotnine import *
from plotnine.data import *
# import seaborn as sns
# sns.set_theme()
pw.overwrite_axisgrid() #Overwrite Grid class provided by seaborn.


import pandas as pd
import numpy as np
import math
from math import sqrt as sqrt
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format, custom_format, mpl_format,scientific_format
from dfply import gather, group_by, mask, mutate, select, spread, summarize, X
from pandas import DataFrame, read_csv
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
        geom_point, 
        geom_vline, 
        ggplot, 
        labeller, 
        scale_color_manual,
        scale_size_manual,
        scale_x_continuous, 
        scale_y_continuous, 
        scale_y_log10, 
        theme)
from time import asctime, localtime, time
from scipy import stats as stats
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
path.insert(0, str(scripts_folder))
output_folder = str(project_folder) + '/output_analysis'


font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=30)
axis_title_properties = FontProperties(fname=font_path, size=30)
legend_title_properties = FontProperties(fname=font_path, size=30)
strip_text_properties = FontProperties(fname=font_path, size=30)
text_properties = FontProperties(fname=font_path, size=30)


phase1_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase1_corr_fitness_genome_length_dataframe.csv'
    )


def create_phase1_plot():

    """
    Create the Phase 1 plot.

    :return: 'Date, time, and year: date_time_year
            Module: module_path
            Saved image: phase1_plot_location'
    :rtype: str
    """

    # Generate fake data for framing.
    trait_names = ["genome_length_average_value_log10", "genome_length_average_value_log10", "fitness_average_value_log10", "fitness_average_value_log10"] 
    value = [1.80, 2.20, -2, 8]
    frame_nums = {'trait': trait_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 
    
    
    # Use ancestor data to plot ancestor values.
    genome_length_ancestor_value =  (
            phase1_dataframe['genome_length_ancestor_value_log10'].mean())
    fitness_ancestor_value =  (
            phase1_dataframe['fitness_ancestor_value_log10'].mean())
    
    
    trait_names = ["genome_length_average_value_log10", "fitness_average_value_log10"] 
    value = list([genome_length_ancestor_value, fitness_ancestor_value])
    ancestor_values = {'trait': trait_names, 'ancestor_value': value}  
    ancestor_data = DataFrame(ancestor_values) 
    print(ancestor_data)
        
    points_plot = (
            ggplot(
                    data=phase1_dataframe, 
                    mapping=aes(
                            x='genome_length_average_value_log10',
                            y='fitness_average_value_log10'))
            
            + geom_point(
                    data= ancestor_data, 
                    mapping=aes(
                            x= ancestor_data['ancestor_value'][0], 
                            y= ancestor_data['ancestor_value'][1]
                            ), 
                    shape= '*', 
                    size= 20, 
                    color='#4B0055',
                #     color='green',
                    inherit_aes= False)           
            + geom_point(size=2)
            
            + scale_x_continuous(
                    name='Size log\u2081\u2080',
                    breaks=[1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15],
                    labels=['1.85','1.90', '1.95', '2.00', '2.05', '2.10', '2.15'],
                    limits=[1.9, 2.05]
                    )
            + scale_y_continuous(
                    name='Log Fitness',
                    breaks=[-2, 0, 2, 4, 6, 8],
                    labels=['-2','0', '2','4','6', '8' ]
                            )
            + geom_blank(
                    data=frame_data, 
                    mapping=aes(y='value'), 
                    inherit_aes=False)            
            + theme(
                    figure_size=(5.2, 4.375),
                    # panel_spacing = .03,
                    legend_title_align= 'center',
                    text=element_text(fontproperties=text_properties),
                    title=element_text(fontproperties=plot_title_properties),
                    legend_position= 'none', 
                    plot_background=element_rect(fill='white'),
                    axis_text_x=element_text(
                            margin={'t':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    axis_text_y=element_text(
                            margin={'r':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    # axis_title_x=element_text(
                    #         margin= {'t': 12}, 
                    #         fontproperties=axis_title_properties), 
                    axis_title_y=element_text(
                            margin= {'r': 12}, 
                            fontproperties=axis_title_properties),
                    axis_title_x=element_blank(), 
                #     axis_title_y=element_blank(),
                    axis_ticks_major_x=element_blank(),
                    axis_ticks_major_y=element_blank(),
                    rect=element_rect(
                            color='white', 
                            size=3, 
                            fill='white'),
                    panel_grid_major_y=element_line(
                            linetype='solid', 
                            color='gray', 
                            size=.5),
                    strip_text_x = element_text(
                            fontproperties=strip_text_properties),
                    )
                )   

    lines_time_plot = (
            ggplot(
                    data=phase1_dataframe,
                    mapping=aes(
                        x='genome_length_average_value_log10',
                        y='fitness_average_value_log10',
                        color= 'time',
                        group= 'time_series'
                        )
                    )

            + geom_smooth(method='glm', se=False)
            
        #     + geom_blank(
        #             data=frame_data, 
        #             mapping=aes(y='value'), 
        #             inherit_aes=False)

            + scale_x_continuous(
                    name='Size log\u2081\u2080',
                    breaks=[1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15],
                    labels=['1.85','1.90', '1.95', '2.00', '2.05', '2.10', '2.15'],
                    limits=[1.9, 2.05]
                    )
            + scale_y_continuous(
                    name='Fitness log\u2081\u2080',
                    breaks=[-2, 0, 2, 4, 6, 8],
                    labels=['-2', '0', '2', '4', '6', '8'],
                    limits=[-2, 8]
                            )
            + scale_color_continuous(
                    breaks=[100000,200000,300000,400000,500000],
                    labels=['100k', '200k', '300k', '400k', '500k']
                    )
            + labs(color='Time')
            + theme(
                    figure_size=(5.2, 4.375),
                    # panel_spacing = .03,
                    legend_title_align= 'center',
                    text=element_text(fontproperties=text_properties),
                    title=element_text(fontproperties=plot_title_properties),
                #     legend_position= 'none',
                    plot_background=element_rect(fill='white'),
                    axis_text_x=element_text(
                            margin={'t':6},
                            color='black',
                            fontproperties=text_properties),
                    axis_text_y=element_text(
                            margin={'r':6},
                            color='black',
                            fontproperties=text_properties),
                    # axis_title_x=element_text(
                    #         margin= {'t': 12},
                    #         fontproperties=axis_title_properties),
                    # axis_title_y=element_text(
                    #         margin= {'r': 12},
                    #         fontproperties=axis_title_properties),
                    axis_title_x=element_blank(),
                    axis_title_y=element_blank(),
                    axis_ticks_major_x=element_blank(),
                    axis_ticks_major_y=element_blank(),
                    rect=element_rect(
                            color='white',
                            size=3,
                            fill='white'),
                    panel_grid_major_y=element_line(
                            linetype='solid',
                            color='gray',
                            size=.5),
                    strip_text_x = element_text(
                            fontproperties=strip_text_properties),
                    ))

    lines_lineage_plot = (
            ggplot(
                    data=phase1_dataframe, 
                    mapping=aes(
                        x='genome_length_average_value_log10',
                        y='fitness_average_value_log10',
                        color= 'factor(ancestor_seed)',  
                        group= 'lineage_series'
                        )
                    )
        
            + stat_smooth(method='glm',
                          size = 4,
                          se=False)     
            
            + scale_x_continuous(
                    name='Size log\u2081\u2080',
                    breaks=[1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15],
                    labels=['1.85','1.90', '1.95', '2.00', '2.05', '2.10', '2.15'],
                    limits=[1.9, 2.05]
                    )
            + scale_y_continuous(
                    name='Fitness log\u2081\u2080',
                    breaks=[-2, 0, 2, 4, 6, 8],
                    labels=['-2', '0', '2', '4', '6', '8'],
                    limits=[-2,8]
                            )           
            + theme(
                    figure_size=(5.2, 4.375),
                    # panel_spacing = .03,
                    legend_title_align= 'center',
                    text=element_text(fontproperties=text_properties),
                    title=element_text(fontproperties=plot_title_properties),
                    legend_position= 'none', 
                    plot_background=element_rect(fill='white'),
                    axis_text_x=element_text(
                            margin={'t':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    axis_text_y=element_text(
                            margin={'r':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    # axis_title_x=element_text(
                    #         margin= {'t': 12}, 
                    #         fontproperties=axis_title_properties), 
                    # axis_title_y=element_text(
                    #         margin= {'r': 12}, 
                    #         fontproperties=axis_title_properties),
                    axis_title_x=element_blank(), 
                    axis_title_y=element_blank(),
                    axis_ticks_major_x=element_blank(),
                    axis_ticks_major_y=element_blank(),
                    rect=element_rect(
                            color='white', 
                            size=4, 
                            fill='white'),
                    panel_grid_major_y=element_line(
                            linetype='solid', 
                            color='gray', 
                            size=.5),
                    strip_text_x = element_text(
                            fontproperties=strip_text_properties),
                    ))

    comb_lines_plot = (
            ggplot(
                    data=phase1_dataframe, 
                    mapping=aes(
                        x='genome_length_average_value_log10',
                        y='fitness_average_value_log10',  
                        )
                    )
            
            + stat_smooth(
                    method='glm',
                    se=False,
                    linetype='solid',
                    size=.5,
                    alpha=.5,
                    data=phase1_dataframe, 
                    mapping=aes(
                        x='genome_length_average_value_log10',
                        y='fitness_average_value_log10',
                        color= 'time',  
                        group= 'time_series',
                        inherit_aes= False
                        )
                    ) 
                    
            + stat_smooth(
                    method='glm',
                    # linetype='dashed',
                    color='red',
                    size=3,
                    se=False,
                    data=phase1_dataframe, 
                    mapping=aes(
                        x='genome_length_average_value_log10',
                        y='fitness_average_value_log10',  
                        group= 'lineage_series',
                        inherit_aes= False
                        ))     
        #     + scale_color_gradient()
            + scale_x_continuous(
                    name='Log Size',
                    breaks=[1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15],
                    labels=['1.85','1.90', '1.95', '2.00', '2.05', '2.10', '2.15'],
                    limits=[1.9, 2.05]
                    )
            + scale_y_continuous(
                    name='Log Fitness',
                    breaks=[-2, 0, 2, 4, 6, 8],
                    labels=['-2', '0', '2', '4', '6', '8'],
                    limits=[-2, 8]
                            )       
            + theme(
                    figure_size=(5.2, 4.375),
                    # panel_spacing = .03,
                    legend_title_align= 'center',
                    text=element_text(fontproperties=text_properties),
                    title=element_text(fontproperties=plot_title_properties),
                    legend_position= 'none', 
                    plot_background=element_rect(fill='white'),
                    axis_text_x=element_text(
                            margin={'t':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    axis_text_y=element_text(
                            margin={'r':6}, 
                            color='black', 
                            fontproperties=text_properties),
                    axis_title_x=element_blank(), 
                    axis_title_y=element_blank(),
                #     axis_title_x=element_text(
                #             margin= {'t': 12}, 
                #             fontproperties=axis_title_properties), 
                #     axis_title_y=element_text(
                #             margin= {'r': 12}, 
                #             fontproperties=axis_title_properties),
                    axis_ticks_major_x=element_blank(),
                    axis_ticks_major_y=element_blank(),
                    rect=element_rect(
                            color='white', 
                            size=3, 
                            fill='white'),
                    panel_grid_major_y=element_line(
                            linetype='solid', 
                            color='gray', 
                            size=.5),
                    strip_text_x = element_text(
                            fontproperties=strip_text_properties),
                    ))


    g1 = points_plot
    g2 = lines_time_plot
    g3 = lines_lineage_plot
    g4 = comb_lines_plot
 
    g1 = pw.load_ggplot(g1)
    g2 = pw.load_ggplot(g2)
    g3 = pw.load_ggplot(g3) 
    g4 = pw.load_ggplot(g4) 
      
    # g1 = pw.load_ggplot(g1, figsize=(3,3))
    # g2 = pw.load_ggplot(g2, figsize=(3,3))
    # g3 = pw.load_ggplot(g3, figsize=(6,6))
    # g4 = pw.load_ggplot(g4, figsize=(6,6))
    
    g1234 = (g1|g2|g3)/g4
    g1234.savefig(fname= output_folder 
                    + '/masked/phase1_plot/combined_correlations.tif',
                format= 'tif'
                    )
    
    date_time_year = asctime(localtime(time()))       
    
    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved image: %s' 
            % (
            date_time_year, 
            module_path, (
                    output_folder 
                    + '/masked/phase1_plot/' 
                    + 'combined_correlations.tif')))

if __name__ == '__main__':
   print(create_phase1_plot())
  