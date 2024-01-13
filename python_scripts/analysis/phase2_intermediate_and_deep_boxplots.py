"""
Create the adaptation, chance, and history by depth plot.

function:: def create_ACH_phase2_boxplot() -> str

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

def create_ACH_phase2_boxplot():

    """
    Create adaptation, chance, and history estimates by depth plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: phase2_boxplot location'
    :rtype: str
    """
    
    """
    Intermediate
    Fitness
    """
    trait = 'fitness'
    trait_label = 'fitness'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.trait == 'fitness',
                X.depth == 100000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.trait == 'fitness',
                X.depth == 100000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.environment)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [-2, 10, 0, 20]
    frame_nums = {'environment': environment_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    """
    Determine 'order' and create a categorical type. 
    Or else the environments will be in alphabetical order. 
    We want Overlapping to be first
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    frame_data['environment_category'] = (
        frame_data['environment']
        .astype(str).astype(environment_category) )

    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    boxplot_dataframe['environment_category'] = (
        boxplot_dataframe['environment']
        .astype(str).astype(environment_category))

    """
    Repeat for grand mean.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    grand_mean['environment_category'] = (
        grand_mean['environment']
        .astype(str).astype(environment_category))
    """
    Repeat for founder data.    
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    founder_dataframe['environment_category'] = (
        founder_dataframe['environment']
        .astype(str).astype(environment_category))

    phase2_boxplot= (
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
            '~ environment_category',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(environment_category=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average %s' % (trait_label), 
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
        +'/masked/phase2_bytrait_boxplots/' 
        + 'phase2_bytrait_100000_boxplot_%s.tif' % (trait))
    phase2_boxplot.save(
        filename = plot_location)

    """
    Intermediate
    Genome length
    """

    trait = 'genome_length'
    trait_label = 'genome length'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.trait == 'genome_length',
                X.depth == 100000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.trait == 'genome_length',
                X.depth == 100000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.environment)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [1.85, 2.05, 1.85, 2.05]
    frame_nums = {'environment': environment_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    """
    Determine 'order' and create a categorical type. 
    Or else the environments will be in alphabetical order. 
    We want Overlapping to be first
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    frame_data['environment_category'] = (
        frame_data['environment']
        .astype(str).astype(environment_category) )

    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    boxplot_dataframe['environment_category'] = (
        boxplot_dataframe['environment']
        .astype(str).astype(environment_category))

    """
    Repeat for grand mean.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    grand_mean['environment_category'] = (
        grand_mean['environment']
        .astype(str).astype(environment_category))
    """
    Repeat for founder data.    
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    founder_dataframe['environment_category'] = (
        founder_dataframe['environment']
        .astype(str).astype(environment_category))

    phase2_boxplot= (
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
            '~ environment_category',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(environment_category=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average %s' % (trait_label), 
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
        +'/masked/phase2_bytrait_boxplots/' 
        + 'phase2_bytrait_100000_boxplot_%s.tif' % (trait))
    phase2_boxplot.save(
        filename = plot_location2)


    """
    Deep
    Fitness
    """
    trait = 'fitness'
    trait_label = 'fitness'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.trait == 'fitness',
                X.depth == 500000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.trait == 'fitness',
                X.depth == 500000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.environment)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [-2, 10, 0, 20]
    frame_nums = {'environment': environment_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    """
    Determine 'order' and create a categorical type. 
    Or else the environments will be in alphabetical order. 
    We want Overlapping to be first
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    frame_data['environment_category'] = (
        frame_data['environment']
        .astype(str).astype(environment_category) )

    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    boxplot_dataframe['environment_category'] = (
        boxplot_dataframe['environment']
        .astype(str).astype(environment_category))

    """
    Repeat for grand mean.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    grand_mean['environment_category'] = (
        grand_mean['environment']
        .astype(str).astype(environment_category))
    """
    Repeat for founder data.    
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    founder_dataframe['environment_category'] = (
        founder_dataframe['environment']
        .astype(str).astype(environment_category))

    phase2_boxplot= (
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
            '~ environment_category',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(environment_category=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average %s' % (trait_label), 
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

    plot_location3 = (
        str(output_folder) 
        +'/masked/phase2_bytrait_boxplots/' 
        + 'phase2_bytrait_500000_boxplot_%s.tif' % (trait))
    phase2_boxplot.save(
        filename = plot_location3)

    """
    Deep
    Genome length
    """

    trait = 'genome_length'
    trait_label = 'genome length'

    boxplot_dataframe = (
        phase2_dataframe
        >> mask(X.trait == 'genome_length',
                X.depth == 500000))

    founder_dataframe = (
        ancestor_dataframe
        >> mask(X.trait == 'genome_length',
                X.depth == 500000))

    grand_mean = (
        boxplot_dataframe
        >> group_by(X.environment)
        >> summarize(grand_mean = X.evolved_population_value.mean()))

    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [1.9, 2.1, 1.9, 2.1]
    frame_nums = {'environment': environment_names, 'value': value}  
    frame_data = DataFrame(frame_nums) 

    """
    Determine 'order' and create a categorical type. 
    Or else the environments will be in alphabetical order. 
    We want Overlapping to be first
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    frame_data['environment_category'] = (
        frame_data['environment']
        .astype(str).astype(environment_category) )

    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    boxplot_dataframe['environment_category'] = (
        boxplot_dataframe['environment']
        .astype(str).astype(environment_category))

    """
    Repeat for grand mean.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    grand_mean['environment_category'] = (
        grand_mean['environment']
        .astype(str).astype(environment_category))
    """
    Repeat for founder data.    
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    founder_dataframe['environment_category'] = (
        founder_dataframe['environment']
        .astype(str).astype(environment_category))

    phase2_boxplot= (
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
            '~ environment_category',
            nrow=2, 
            scales='free_y', 
            labeller= labeller(environment_category=label_title))
        +geom_hline(data= grand_mean,
                    inherit_aes=False,
                    mapping= aes(
                        yintercept= 'grand_mean'),
                    linetype= 'dashed')
        + scale_y_continuous(
            name='Log\u2081\u2080 average %s' % (trait_label), 
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

    plot_location4 = (
        str(output_folder) 
        +'/masked/phase2_bytrait_boxplots/' 
        + 'phase2_bytrait_500000_boxplot_%s.tif' % (trait))
    phase2_boxplot.save(
        filename = plot_location4)


   

    date_time_year = asctime(localtime(time()))

    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved images: %s & %s & %s & %s'  
            % (
            date_time_year, 
            module_path, 
            plot_location, 
            plot_location2,
            plot_location3,
            plot_location4
            ))

    
if __name__ == '__main__':
    print(create_ACH_phase2_boxplot())
 