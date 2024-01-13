"""
Create the data trajectory plot for shallow Phase 2 populations.

function:: def create_phase2_plot() -> str

This is Fig. 4.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import mask, select, X
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format, custom_format
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
        ggplot, 
        labeller, 
        scale_x_continuous, 
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
from label_title import label_title as label_title

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=12)
axis_title_properties = FontProperties(fname=font_path, size=11)
legend_title_properties = FontProperties(fname=font_path, size=11)
strip_text_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)

phase2_dataframe = read_csv(
    output_folder 
    + '/phase2_dataframe.csv')


def create_phase2_plot():

    """
    Create the Phase 2 plot.

    :return: 'Date, time, and year: date_time_year
            Module: module_path
            Saved image: phase2_plot_location'
    :rtype: str
    """
        
    run_length = 20000
    environment = 'overlapping'
    combined_filters = [(run_length, environment)]

    for each in combined_filters:
        each_run_length = each[0]
        each_environment = each[1]

        phase2_dataframe_masked = (
            phase2_dataframe  
            >> select (
                X.series, 
                X.lineage, 
                X.time, 
                X.ancestor_run_length, 
                X.replicate, 
                X.environment, 
                X.trait, 
                X.ancestor_value, 
                X.ancestor_value_log10, 
                X.evolved_population_average_value, 
                X.evolved_population_average_value_log10) 
            >>  mask (
                X.ancestor_run_length == each_run_length, 
                X.environment == each_environment))
      
        # Use fake data assigned to geom_blank for frame control 
        # 1. Mute genome_blank in plot initially.
        # 2. Insert frame data below to control limits.
        # 3. Unmute genome_blank.
        trait = ["fitness", "fitness", "genome_length", "genome_length"] 
        value = [0, 20, 1.8, 2.1]
        frame_nums = {'trait': trait, 'value': value}  
        frame_data = DataFrame(frame_nums) 

        phase2_plot  = (
            ggplot(
                data=phase2_dataframe_masked, 
                mapping=aes(
                    x='time',
                    y='evolved_population_average_value_log10', 
                    color='factor(lineage)', 
                    group= 'series'))
            + geom_line(size=.5)
            + geom_blank(
                data=frame_data, 
                mapping=aes(y='value'), 
                inherit_aes=False)
            + facet_wrap(
                '~ trait', 
                nrow=2, 
                scales='free_y', 
                labeller= labeller(trait=label_title))
            + scale_x_continuous(
                name='Time (updates)',
                labels= currency_format(
                    prefix='', 
                    suffix='', 
                    digits=0, 
                    big_mark=','))

            + scale_y_continuous(
                name='Log\u2081\u2080 average value', 
                labels = fixed_precision)
            + theme(
                figure_size=(5.2, 4.375),
                text=element_text(fontproperties=text_properties),
                title=element_text(
                    # margin= {'b': 20}, 
                    fontproperties=plot_title_properties),
                legend_position= 'none', 
                plot_background=element_rect(fill='white'),
                axis_text_x=element_text(
                    margin={'t':6}, 
                    color='black', 
                    size=8, 
                    fontproperties=text_properties),
                axis_text_y=element_text(
                    margin={'r':6}, 
                    color='black', 
                    size=8, 
                    fontproperties=text_properties),
                axis_title_x=element_text(
                    margin= {'t': 12}, 
                    fontproperties=axis_title_properties), 
                axis_title_y=element_text(
                    margin= {'r': 16}, 
                    fontproperties=axis_title_properties),
                axis_ticks_major_x=element_blank(),
                axis_ticks_major_y=element_blank(),
                rect=element_rect(color='white', size=3, fill='white'),
                panel_grid_major_y=element_line(
                    linetype='solid', 
                    color='gray', 
                    size= .5),
                panel_spacing = .05
                ))

        phase2_plot_name= (
            'phase2_byenvironment_%s_%s.pdf' 
            % (each_environment, each_run_length))
        phase2_plot.save(
            filename = phase2_plot_name, 
            path = output_folder 
                + '/masked/phase2_byenvironment_plots')
            
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
                    + '/masked/phase2_byenvionment_plots/' 
                    + phase2_plot_name)))


if __name__ == '__main__':
        print(create_phase2_plot())
