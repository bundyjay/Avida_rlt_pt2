"""
Create the adaptation, chance, and shallow history estimates plot.

function:: def create_ACH_estimate_plot() -> str

This is S2 Fig.
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from dfply import mask, select, X
from matplotlib.font_manager import FontProperties
from mizani.formatters import currency_format
from pandas import Categorical, DataFrame, read_csv
from pathlib import Path
from plotnine import (
        aes, 
        element_blank, 
        element_line, 
        element_rect, 
        element_text, 
        facet_wrap, 
        geom_blank,
        geom_errorbar, 
        geom_line,  
        geom_point, 
        ggplot, 
        labeller,
        labs, 
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

ACH_estimate_dataframe = read_csv(
    output_folder 
    + '/ACH_trajectory_dataframe.csv')


def create_ACH_estimate_plot():

    """
    Create the adaptation, chance, and history estimates plot.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved image: ACH_estimate_plot location'
    :rtype: str
    """
    
    environment = 'orthogonal'
    run_length = '20000'
    final_update_num = 100000
    
    ACH_estimate_dataframe_masked = (
        ACH_estimate_dataframe 
        >> mask(
            X.environment == environment, 
            X.run_length == int(run_length), 
            X.time== final_update_num)) 

    """
    Determine 'order' and create a categorical type. 
    Or else the x-axis will be in alphabetical order. 
    We want Ancestral to be last
    """
    source_list =  ["adaptation", "chance", "history", "ancestral"]
    ACH_estimate_dataframe_masked['source'] = Categorical(
        ACH_estimate_dataframe_masked['source'], 
        categories=source_list, 
        ordered=True)

    trait_names = ["fitness", "fitness", "genome_length", "genome_length"] 
    value = [0, 4, -.05, .10]
    frame_nums = {
        'trait': trait_names, 
        'value': value}  
    frame_data = DataFrame(frame_nums) 
   
    ACH_estimate_plot= (
        ggplot(ACH_estimate_dataframe_masked) 
        + geom_point(aes(x="source", y="value"), size=2) 
        + geom_errorbar(aes(
            x="source", 
            ymin="lower_endpoint",
            ymax="upper_endpoint"))
        + facet_wrap(
            '~ trait', 
            nrow=2, 
            scales= 'free_y', 
            labeller= labeller(trait=label_title))
        + labs(
            x= 'Source', 
            y= 'Contribution to log\u2081\u2080 average value')
        + scale_x_discrete(
            breaks= [
                'ancestral', 
                'adaptation', 
                'chance', 
                'history'], 
            labels=[
                'Ancestral', 
                'Adaptation', 
                'Chance', 
                'History'])
        + scale_y_continuous(
            labels = fixed_precision)      
        + geom_blank(
            data=frame_data, 
            mapping=aes(y='value'), 
            inherit_aes=False)
        + theme(
            figure_size=(5.2, 4.375),
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
                margin= {'r': 24}, 
                fontproperties=axis_title_properties),
            axis_ticks_major_x=element_blank(), 
            axis_ticks_major_y=element_blank(),
            rect=element_rect(
                color='white', 
                size=3, 
                fill='white'),
            panel_grid_major_y=element_line(
                linetype='solid', 
                color='black', 
                size=.4),
            panel_spacing = .3))

    plot_location = (
        str(output_folder) 
        + '/masked/ACH_estimates_shallow/' 
        + 'ACH_estimates_plot_%s_%s.pdf' % (
            environment, run_length))
    ACH_estimate_plot.save(
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
        print(create_ACH_estimate_plot())

