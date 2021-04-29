"""
Create the adaptation, chance, and history by depth plot.

function:: def create_ACH_estimates_bydepth_plot() -> str

This is Fig. 8.
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
        geom_errorbar, 
        facet_wrap, 
        geom_blank, 
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
axis_title_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)  

sorted_ACH_trajectory_dataframe= read_csv(
    output_folder 
    + '/ACH_trajectory_dataframe.csv')
final_update = 100000
ACH_trajectory_final_update_dataframe= (
    sorted_ACH_trajectory_dataframe 
    >> mask(X.time==final_update))


def create_ACH_estimates_bydepth_plot():

    """
    Create adaptation, chance, and history estimates by depth plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: estimates_bydepth_plot location'
    :rtype: str
    """

    trait= 'fitness'
    trait_label = 'fitness'

    ACH_trajectory_final_update_dataframe_masked = (
        ACH_trajectory_final_update_dataframe 
        >> mask(X.trait== trait))

    """
    Determine 'order' and create a categorical type. 
    Or else the x-axis will be in alphabetical order. 
    We want Ancestral to be last
    """
    source_list= ['adaptation', 'chance', 'history', 'ancestral']
    source_category = CategoricalDtype(categories=source_list, ordered=True)
    ACH_trajectory_final_update_dataframe_masked['source_category'] = (
        ACH_trajectory_final_update_dataframe_masked['source']
        .astype(str).astype(source_category))

    environment_names = [
        "orthogonal", 
        "orthogonal", 
        "overlapping", 
        "overlapping"] 
    value = [0, 8, 0, 15]
    frame_nums = {'environment': environment_names, 'value': value}  
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
        .astype(str).astype(environment_category) )
    
    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    ACH_trajectory_final_update_dataframe_masked['environment_category'] = (
        ACH_trajectory_final_update_dataframe_masked['environment']
        .astype(str).astype(environment_category))

    dodge = positions.position_dodge(width=0.5)

    estimates_bydepth_plot= (
        ggplot(
            data=ACH_trajectory_final_update_dataframe_masked, 
            mapping=aes(
                x='factor(source_category)', 
                y='value', 
                color='factor(run_length)', 
                group='run_length'))
    + geom_point(size=2, position=dodge)
    + geom_errorbar(
        aes(
            x='factor(source_category)', 
            ymin='lower_endpoint',
            ymax='upper_endpoint'
            ),
        position=dodge)
    + facet_wrap(
        '~ environment_category', 
        nrow=2, 
        scales='free_y', 
        labeller= labeller(environment_category=label_title))
    + geom_blank(
        data=frame_data, 
        mapping=aes(y='value'), 
        inherit_aes=False)
    + labs(
        x= 'Source', 
        y= 'Contribution to log\u2081\u2080 %s' % (trait_label),
        color= 'Depth')
    + scale_x_discrete(
        values=[
            'ancestral', 
            'adaptation', 
            'chance', 
            'history'], 
        breaks= [
            'ancestral', 
            'adaptation', 
            'chance', 
            'history'], 
        labels= [
            'Ancestral', 
            'Adaptation', 
            'Chance', 
            'History'])
    + scale_y_continuous(labels = fixed_precision)      
    + theme(
        figure_size=(5.2, 7),
        legend_position='none',
        plot_background=element_rect(fill='white'),
        axis_text_x=element_text(
            margin={'t':6}, 
            color='black', 
            fontproperties=text_properties),
        axis_text_y=element_text(
            margin={'r':6}, 
            color='black', 
            fontproperties=text_properties),
        axis_title_x=element_text(
            margin= {'t': 12}, 
            fontproperties=axis_title_properties), 
        axis_title_y=element_text(
            margin= {'r': 18}, 
            fontproperties=axis_title_properties),
        axis_ticks_major_x=element_blank(),
        axis_ticks_major_y=element_blank(),
        rect=element_rect(color='white', size=3, fill='white'),
        panel_grid_major_y=element_line(
            linetype='solid', 
            color='gray', 
            size= .5),
        panel_spacing = .3))

    plot_location = (
        str(output_folder) 
        +'/masked/footprint_ACH_estimates_bytrait/' 
        + 'footprint_ACH_estimates_%s.pdf' % (trait))
    estimates_bydepth_plot.save(
        filename = plot_location)

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

    
if __name__ == '__main__':
    print(create_ACH_estimates_bydepth_plot())
