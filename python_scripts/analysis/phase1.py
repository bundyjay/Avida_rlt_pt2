"""
Create the data trajectory plot for Phase 1.

function:: def create_phase1_plot() -> str

This is Fig. 3.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import select, X
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format
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

phase1_dataframe = read_csv(
        str(output_folder) 
        + '/phase1_dataframe.csv') 


def create_phase1_plot():

        """
        Create the Phase 1 plot.

        :return: 'Date, time, and year: date_time_year
                Module: module_path
                Saved image: phase1_plot_location'
        :rtype: str
        """
        
        phase1_dataframe_combined = phase1_dataframe >> select (
                X.series, 
                X.trait, 
                X.time, 
                X.ancestor_seed,  
                X.ancestor_value, 
                X.ancestor_value_log10, 
                X.evolved_population_average_value, 
                X.evolved_population_average_value_log10)
        
        # Use ancestor data to plot ancestor values.
        fitness_ancestor_value =  (
                phase1_dataframe_combined.query(
                        "trait == 'fitness'")
                        ['ancestor_value_log10']
                        .mean())
        genome_length_ancestor_value =  (
                phase1_dataframe_combined.query(
                        "trait == 'genome_length'")
                        ['ancestor_value_log10']
                        .mean())
        trait_names = ["fitness", "genome_length",] 
        value = list([fitness_ancestor_value, genome_length_ancestor_value])
        ancestor_values = {'trait': trait_names, 'ancestor_value': value}  
        ancestor_data = DataFrame(ancestor_values) 

        # Generate fake data for framing.
        trait_names = ["fitness", "fitness", "genome_length", "genome_length"] 
        value = [-2, 10, 1.90, 2.05]
        frame_nums = {'trait': trait_names, 'value': value}  
        frame_data = DataFrame(frame_nums) 
        
        phase1_plot = (
                ggplot(
                        data=phase1_dataframe_combined, 
                        mapping=aes(
                                x='time',
                                y='evolved_population_average_value_log10', 
                                color= 'factor(ancestor_seed)', 
                                group= 'series'))
                + geom_line(size= .5)
                + geom_vline(xintercept=20000)
                + geom_vline(xintercept=100000)
                + geom_vline(xintercept=500000)

                + geom_point(
                        data= ancestor_data, 
                        mapping=aes(
                                x=0, 
                                y='ancestor_value'
                                ), 
                        shape= '*', 
                        size= 4, 
                        inherit_aes= False)
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
                        labels = currency_format(
                                prefix='', 
                                suffix='', 
                                digits=0, 
                                big_mark=','))
            + scale_y_continuous(
                name='Log\u2081\u2080 average value', 
                labels = fixed_precision)
                + theme(
                        figure_size=(5.2, 4.375),
                        legend_title_align= 'center',
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
                                margin= {'r': 18}, 
                                fontproperties=axis_title_properties),
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
                        panel_spacing = .3)) 

        phase1_plot_name= 'phase1.pdf'
        phase1_plot.save(
                filename = phase1_plot_name, 
                path = (
                        output_folder 
                        + '/masked/phase1_plot'))

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
                        + phase1_plot_name)))


if __name__ == '__main__':
   print(create_phase1_plot())
  
