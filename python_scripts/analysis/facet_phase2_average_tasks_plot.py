"""
Analyze the Phase 1 total tasks and average length by depth.

Saves 'phase1_total_tasks_and_average_length_analysis_log.txt'
in the logs directory.

This module has no functions or classes.
It does not return anything. 
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'
import pandas as pd
import patchworklib as pw 
import scikit_posthocs as sp
import statistics

from collections import defaultdict
from dfply import mask, group_by, summarize, X
from matplotlib.font_manager import FontProperties
from pandas import CategoricalDtype, DataFrame, read_csv
from pathlib import Path
from plotnine import aes, element_blank, element_line, element_rect, element_text, facet_grid, geom_blank, geom_boxplot, geom_crossbar, geom_jitter, geom_point, ggplot, labeller, position_jitterdodge, scale_color_manual, scale_x_log10, scale_y_continuous, theme
from time import asctime, localtime, time
from scipy.stats import friedmanchisquare
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
colorspace_folder = str(scripts_folder) + '/operations/python-colorspace'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))
path.insert(0, str(colorspace_folder))

from phase1_tasks_custom_label import label_title as label_title
from colorspace import qualitative_hcl
colors = qualitative_hcl("dark3").colors(10)
from contextlib import redirect_stdout

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=12)
axis_title_properties = FontProperties(fname=font_path, size=11)
legend_title_properties = FontProperties(fname=font_path, size=11)
strip_text_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)

def analysis():
    
    ACH_phase2_average_tasks_data_dataframe = read_csv(
        str(project_folder) 
        + '/output_analysis/'
        + 'phase2_average_tasks_data_dataframe.csv'
        )


    color_dict = {
            20000 : 'black',
            100000 : 'black',
            500000 : 'black',
    }


    df_full = (
        ACH_phase2_average_tasks_data_dataframe
        >>mask(X.trait !='total_tasks')
        >> group_by(
            X.replicate_environment, 
            X.trait, 
            X.ancestor_run_length,
            X.ancestor_seed
            ) 
        >> summarize(group_mean = X.evolved_population_value.mean())
        )
    
    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    df_full['environment_category'] = (
       df_full['replicate_environment']
        .astype(str).astype(environment_category))
    
    # print(df_tasks)

    environments = ['orthogonal', 'overlapping']
    traits = ['rewards', 'unrewarded_tasks']
    data_dict = defaultdict(dict)
    list_of_keys = []

    for environment in environments:
        for trait in traits:
            df_filter= (
                ACH_phase2_average_tasks_data_dataframe
                >>mask(X.trait == trait, X.replicate_environment == environment)
                >> group_by(
                    X.replicate_environment, 
                    X.trait, 
                    X.ancestor_run_length,
                    X.ancestor_seed
                    ) 
                >> summarize(group_mean = X.evolved_population_value.mean())
                )
            
            key = '%s_%s' % (environment, trait)
            # print('\n')
            print('Environment: ', environment, ' Trait: ', trait, '\n')
            list_of_keys.append(key)
            # print(df_filter)

            #Friedman test
            filter_20k= df_filter.loc[(df_filter['ancestor_run_length'] == 20000)]
            filter_100k = df_filter.loc[(df_filter['ancestor_run_length'] == 100000)]
            filter_500k = df_filter.loc[(df_filter['ancestor_run_length'] == 500000)]
            # print('20k_filter: ', filter_20k)
            # print('100k_filter: ', filter_100k)
            # print('500k_filter: ', filter_500k)


            list_20k = filter_20k['group_mean'].values.tolist()
            list_100k = filter_100k['group_mean'].values.tolist()
            list_500k = filter_500k['group_mean'].values.tolist()
            # data_dict[key] = ['list_20k': list_20k, 'list_100k': list_100k, 'list_500k': list_500k]
            print('list_20k: ', list_20k)
            print('list_100k: ', list_100k)
            print('list_500k: ', list_500k)


            median_20k = statistics.median(list_20k)
            median_100k = statistics.median(list_100k)
            median_500k = statistics.median(list_500k)
            data_dict[key] = {'median_20k': median_20k, 'median_100k': median_100k, 'median_500k': median_500k}
            print('\n')
            print('median_20k', median_20k)
            print('median_100k', median_100k)
            print('median_500k', median_500k)

            # trait_names = ["rewards", "rewards", "rewards"]
            # depths = [20000, 100000, 500000]
            # values = [rewards_median_20k, rewards_median_100k, rewards_median_500k]
            # median_dict = {'trait': trait_names, 'depth': depths, 'value': values}  
            # rewards_median_data = DataFrame(median_dict)
            # # print('median data: ', rewards_median_data)

            res = friedmanchisquare(list_20k, list_100k, list_500k)
            stat = res.statistic
            p_value = res.pvalue
            # data_dict[key] = ['Friedman_stat': stat, 'Friedman_p': p_value]

            print('\nFriedman stat, p_value:\n', stat, p_value)

            # Dunn test (below) isn't necessary if Friedman test doesn't reject null hypothesis
            # # Dunn test
            data = [list_20k, list_100k, list_500k]
            # print('data: ', data)

            p_values= sp.posthoc_dunn(data, p_adjust = 'holm')
            print('\nDunn p values:\n', p_values)

            sig = p_values < 0.05
            print('\nSignificant a=0.05\n', sig)
            print('\n')

    environment = ["orthogonal", "orthogonal", "orthogonal", "orthogonal", "orthogonal", "orthogonal", "overlapping", "overlapping", "overlapping", "overlapping", "overlapping", "overlapping"]
    trait_names = ["rewards", "rewards", "rewards", "unrewarded_tasks", "unrewarded_tasks", "unrewarded_tasks", "rewards", "rewards", "rewards", "unrewarded_tasks", "unrewarded_tasks", "unrewarded_tasks"]
    depths = [20000, 100000, 500000, 20000, 100000, 500000, 20000, 100000, 500000, 20000, 100000, 500000]
    values = [data_dict['orthogonal_rewards']['median_20k'], data_dict['orthogonal_rewards']['median_100k'], data_dict['orthogonal_rewards']['median_500k'], data_dict['orthogonal_unrewarded_tasks']['median_20k'], data_dict['orthogonal_unrewarded_tasks']['median_100k'], data_dict['orthogonal_unrewarded_tasks']['median_500k'], data_dict['overlapping_rewards']['median_20k'], data_dict['overlapping_rewards']['median_100k'], data_dict['overlapping_rewards']['median_500k'], data_dict['overlapping_unrewarded_tasks']['median_20k'], data_dict['overlapping_unrewarded_tasks']['median_100k'], data_dict['overlapping_unrewarded_tasks']['median_500k'] ]
    median_dict = {'replicate_environment': environment,'trait': trait_names, 'ancestor_run_length': depths, 'value': values}  
    median_data = DataFrame(median_dict)
    # print('median data: ', median_data)

    # # Generate fake data for framing.
    # trait_names = ["rewards", "rewards"] 
    # value = [0, 100000]
    # frame_nums = {'trait': trait_names, 'value': value}  
    # frame_data = DataFrame(frame_nums) 
    
    """
    Repeat for main dataframe.   
    """
    environment_list = ['overlapping', 'orthogonal']
    environment_category = (
        CategoricalDtype(categories=environment_list, ordered=True))
    median_data['environment_category'] = (
        median_data['replicate_environment']
        .astype(str).astype(environment_category))

    tasks_plot = (
        ggplot(
            data = df_full,
            mapping = aes(
                x='ancestor_run_length',
                y='group_mean' ,
                color='factor(ancestor_run_length)'
                # color='factor(ancestor_seed)',
                # fill=black
            )
        )

        + geom_jitter(alpha=1, position = position_jitterdodge(0.6))
        # path.insert(0, str(colorspace_folder))+ geom_point()
        
        + geom_crossbar(
            data=median_data,
            mapping=aes(
                x='ancestor_run_length',
                y='value',
                ymin='value', 
                ymax='value'),
            size=.125,
            color='black',
            width=.5,
            inherit_aes=False        
                    )
        # + geom_blank(
        #     data=frame_data, 
        #     mapping=aes(y='value'), 
        #     inherit_aes=False)

        + facet_grid(
            'environment_category ~ trait', 
            # nrow=2, 
            # scales='free_y', 
            labeller= labeller(trait=label_title, environment_category=label_title))

        +scale_x_log10(
            name='Depth (updates x 1,000)',
            breaks=[20000, 100000, 500000],
            labels=['20', '100', '500']
            )
        +scale_y_continuous(
            name='Tasks performed (x 1,000)',
            breaks=[0, 50000, 100000, 150000, 200000],
            labels=['0', '50', '100', '150', '200']
            )
        + scale_color_manual(values = color_dict)
        
        + theme(
                figure_size=(5.2, 4.375),
                legend_title_align= 'center',
                text=element_text(fontproperties=text_properties),
                title=element_text(
                        margin= {'b': 12}, 
                        fontproperties=plot_title_properties),
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
                axis_title_x=element_text(
                        margin= {'t': 12}, 
                        fontproperties=axis_title_properties), 
                axis_title_y=element_text(
                        margin= {'r': 12}, 
                        fontproperties=axis_title_properties),
                axis_ticks_major_x=element_blank(),
                axis_ticks_major_y=element_blank(),
                rect=element_rect(
                        color='white', 
                        size=.5, 
                        fill='white'),
                panel_grid_major_y=element_line(
                        linetype='solid', 
                        color='gray', 
                        size=.5),
                strip_text_x = element_text(
                        fontproperties=strip_text_properties),
                panel_spacing=0.07
        )
    )

    plot_name = 'phase2_facet_functions.pdf'
    tasks_plot.save(
        filename = plot_name,
        path = output_folder
        + '/masked/phase2_plot'
    )


    return ''

log_name= 'facet_phase2_average_tasks_data_stats_analysis_log.txt'  
date_time_year = (
    '\nDate, time, and year: %s \n' % (asctime(localtime(time()))) 
    )

filename = str(project_folder) + '/logs/' +  log_name
with open(filename, 'w+') as file:
    file.writelines([
        'Signator: J. Bundy', 
        str(date_time_year), ('\n'), 
        'The data is as follows:', ('\n'), 
        ])
    
    with redirect_stdout(file):
        print(analysis())
        
        