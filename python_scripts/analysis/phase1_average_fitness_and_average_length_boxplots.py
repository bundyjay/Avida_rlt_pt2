"""
Analyze the Phase 1 total tasks and average length by depth.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import group_by, mask, select, summarize, X
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
        geom_errorbar, 
        facet_wrap, 
        geom_blank,
        geom_boxplot,
        geom_hline, 
        geom_line,  
        geom_point, 
        ggplot, 
        labeller,
        labs,
        positions, 
        scale_alpha_manual,
        scale_linetype_manual,
        scale_x_discrete,
        scale_y_continuous,
        theme)
from sys import path
from time import asctime, localtime, time

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))

from fixed_precision import fixed_precision as fixed_precision
from phase1_boxplot_label_title import label_title as label_title

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=12)
axis_title_properties = FontProperties(fname=font_path, size=11)
legend_title_properties = FontProperties(fname=font_path, size=11)
strip_text_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)


phase1_dataframe = read_csv(
    str(project_folder) 
    + '/output_analysis/'
    + 'phase1_average_fitness_and_average_length_dataframe.csv'
    )

def create_phase1_boxplots():

    """
    Create adaptation, chance, and history estimates by depth plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: phase2_boxplot location'
    :rtype: str
    """

    """
    Calculate group means by depth.
    """
    group_means = (
        phase1_dataframe 
        >> group_by(X.trait, X.depth) 
        >> summarize(group_mean = X.evolved_population_value.mean(),
                    group_std = X.evolved_population_value.std()
                    ))

    trait_names = [
        "fitness", 
        "fitness", 
        "genome_length", 
        "genome_length"] 
    value = [0, 8, 1.9, 2.1]
    frame_nums = {'trait': trait_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 


    phase1_boxplot= (
        ggplot(
            data=phase1_dataframe, 
            mapping=aes(
                x='factor(depth)', 
                y='evolved_population_value',
                )
            )
        + geom_boxplot()
        + facet_wrap(
                '~ trait',
                nrow=2, 
                scales='free_y', 
                labeller= labeller(trait=label_title))
        + scale_y_continuous(
            name='Log\u2081\u2080 average value', 
            labels = fixed_precision
            )
        + scale_x_discrete(
            name='Depth'
            )
        + geom_blank(
            data=frame_data, 
            mapping=aes(y='value'), 
            inherit_aes=False)
        + theme(
            figure_size=(5.2, 4.375),
            text=element_text(fontproperties=text_properties),
            title=element_text(
                # margin= {'b': 20}, 
                fontproperties=plot_title_properties),
            legend_position= 'none', 
            plot_background=element_rect(fill='white'),
            axis_text_x=element_text(
                # margin={'t':6}, 
                color='black', 
                size=8, 
                fontproperties=text_properties),
            axis_text_y=element_text(
                # margin={'r':6}, 
                color='black', 
                size=8, 
                fontproperties=text_properties),
            axis_title_x=element_text(
                margin= {'t': 12}, 
                fontproperties=axis_title_properties), 
            axis_title_y=element_text(
                margin= {'r': 12}, 
                fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(color='white', size=3, fill='white'),
            panel_grid_major_y=element_line(
                linetype='solid', 
                color='gray', 
                ),
            panel_spacing = .03)
                )

    plot_location = (
        str(output_folder) 
        +'/masked/phase1_boxplots/' 
        + 'phase1_boxplots.tif')
    phase1_boxplot.save(
        filename = plot_location)

    date_time_year = asctime(localtime(time()))

    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved images: %s'  
            % (
            date_time_year, 
            module_path, 
            plot_location
            ))

if __name__ == '__main__':
    print(create_phase1_boxplots())
 