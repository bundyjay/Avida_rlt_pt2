"""
Create the data trajectory plot for intermediate Phase 2 populations.

function:: def create_phase2_plot() -> str

This is S7 fig.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import mask, select, X
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

phase2_dataframe = read_csv(output_folder + '/phase2_dataframe.csv')


def create_phase2_plot():

    """
    Create the Phase 2 plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: phase2_plot_location'
    :rtype: str
    """

    run_length = 500000
    trait = 'genome_length'
    trait_label = 'genome length'

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
        >>  mask(
            X.ancestor_run_length == run_length, 
            X.trait == trait))

    # Use fake data assigned to geom_blank for frame control 
    # 1. Mute genome_blank in plot initially.
    # 2. Insert frame data below to control limits.
    # 3. Unmute genome_blank.
    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [1.9, 2.1, 1.9, 2.1]
    frame_nums = {
        'environment': environment_names, 
        'value': value}  
    frame_data = DataFrame(frame_nums) 

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
    phase2_dataframe_masked['environment_category'] = (
        phase2_dataframe_masked['environment']
        .astype(str).astype(environment_category))

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
            '~ environment_category', 
            nrow=2, 
            scales='free_y', 
            labeller= labeller(environment_category=label_title))
        + scale_x_continuous(
            name='Time (updates)',
            labels= currency_format(
                prefix='', 
                suffix='', 
                digits=0, 
                big_mark=','))
        + scale_y_continuous(
            name='Log\u2081\u2080 average %s' % trait_label,
            labels = fixed_precision)
        + theme(
            figure_size=(5.2, 4.375),
            text=element_text(fontproperties=text_properties),
            title=element_text(
                margin= {'b': 20}, 
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
                margin= {'r': 12}, 
                fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(color='white', size=3, fill='white'),
            panel_grid_major_y=element_line(
                linetype='solid', 
                color='gray', 
                size= .5),
            panel_spacing = .3))

    phase2_plot_name = (
        'phase2_bytrait_%s_%s.pdf' 
        % (run_length, trait)) 
    phase2_plot.save(
        filename = phase2_plot_name, 
        path = output_folder + '/masked/phase2_bytrait_plots')

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
                    + '/masked/phase2_bytrait_plots/' 
                    + phase2_plot_name)))


if __name__ == '__main__':
    print(create_phase2_plot())

