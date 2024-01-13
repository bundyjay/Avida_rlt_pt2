"""
Create the adaptation, chance, and history by depth plot.

function:: def create_ACH_footprint_boxplot() -> str

This is Fig. 8.
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
from label_title import label_title as label_title


font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=12)
axis_title_properties = FontProperties(fname=font_path, size=11)
legend_title_properties = FontProperties(fname=font_path, size=11)
strip_text_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)

phase2_dataframe= read_csv(
    output_folder 
    + '/phase2_average_fitness_and_average_length_dataframe.csv')

ancestor_dataframe= read_csv(
    output_folder 
    + '/ancestor_values_dataframe.csv')

def create_ACH_footprint_boxplot():

    """
    Create adaptation, chance, and history estimates by depth plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: footprint_boxplot location'
    :rtype: str
    """
    environment = 'orthogonal'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.environment == 'orthogonal',
                X.depth == 20000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.environment == 'orthogonal',
                X.depth == 20000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.trait)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    trait_names = [
        "fitness", 
        "fitness", 
        "genome_length", 
        "genome_length"] 
    value = [0, 10, 1.8, 2.1]
    frame_nums = {'trait': trait_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    footprint_boxplot= (
        ggplot(
            data=boxplot_dataframe, 
            mapping=aes(
                x='factor(lineage)', 
                y='evolved_population_value',
                color='factor(lineage)'))
        + geom_boxplot()
        + geom_point(data=founder_dataframe, 
                     mapping=aes(
                         x='factor(lineage)', 
                         y='ancestor_value'), 
                    color = 'green', 
                    shape = '*',
                    size = 3
                    )
        + facet_wrap(
            '~ trait',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(trait=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average value', 
            labels = fixed_precision
            )
        + scale_x_discrete(
            name='Lineage'
            )
        + geom_blank(
            data=frame_data, 
            mapping=aes(y='value'), 
            inherit_aes=False)
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
                margin= {'r': 16}, 
                fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(color='white', size=3, fill='white'),
            panel_grid_major_y=element_line(
                linetype='solid', 
                color='gray', 
                size= .5),
            panel_spacing = .3)
            )

    plot_location = (
        str(output_folder) 
        +'/masked/phase2_shallow_boxplots/' 
        + 'phase2_shallow_boxplot_%s.tif' % (environment))
    footprint_boxplot.save(
        filename = plot_location)

    """
    Overlapping environment
    """    
    
    environment = 'overlapping'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.environment == 'overlapping',
                X.depth == 20000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.environment == 'overlapping',
                X.depth == 20000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.trait)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    trait_names = [
        "fitness", 
        "fitness", 
        "genome_length", 
        "genome_length"] 
    value = [0, 20, 1.8, 2.1]
    frame_nums = {'trait': trait_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    footprint_boxplot= (
        ggplot(
            data=boxplot_dataframe, 
            mapping=aes(
                x='factor(lineage)', 
                y='evolved_population_value',
                color='factor(lineage)'))
        + geom_boxplot()
        + geom_point(data=founder_dataframe, 
                     mapping=aes(
                         x='factor(lineage)', 
                         y='ancestor_value'), 
                    color = 'green', 
                    shape = '*',
                    size = 3
                    )
        + facet_wrap(
            '~ trait',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(trait=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average value', 
            labels = fixed_precision
            )
        + scale_x_discrete(
            name='Lineage'
            )
        + geom_blank(
            data=frame_data, 
            mapping=aes(y='value'), 
            inherit_aes=False)
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
                margin= {'r': 16}, 
                fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(),
            axis_ticks_major_y=element_blank(),
            rect=element_rect(color='white', size=3, fill='white'),
            panel_grid_major_y=element_line(
                linetype='solid', 
                color='gray', 
                size= .5),
            panel_spacing = .3)
            )

    plot_location2 = (
        str(output_folder) 
        +'/masked/phase2_shallow_boxplots/' 
        + 'phase2_shallow_boxplot_%s.tif' % (environment))
    footprint_boxplot.save(
        filename = plot_location2)

    date_time_year = asctime(localtime(time()))

    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved images: %s & %s' 
            % (
            date_time_year, 
            module_path,
            plot_location,
            plot_location2))

    
if __name__ == '__main__':
    print(create_ACH_footprint_boxplot())
