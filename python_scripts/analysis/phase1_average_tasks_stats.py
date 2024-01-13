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

from contextlib import redirect_stdout
from dfply import mask, group_by, summarize, X
from matplotlib.font_manager import FontProperties
from pandas import DataFrame, read_csv
from pathlib import Path
from plotnine import aes, element_blank, element_line, element_rect, element_text, facet_wrap, geom_blank, geom_boxplot, geom_crossbar, geom_jitter, geom_point, ggplot, position_jitterdodge, scale_color_manual, scale_x_log10, scale_y_continuous, theme
from time import asctime, localtime, time
from scipy.stats import friedmanchisquare
from sys import path

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(scripts_folder))

font_path = str(project_folder) + '/resources/fonts/Arial-Unicode-Regular.ttf'             
plot_title_properties = FontProperties(fname=font_path, size=12)
axis_title_properties = FontProperties(fname=font_path, size=11)
legend_title_properties = FontProperties(fname=font_path, size=11)
strip_text_properties = FontProperties(fname=font_path, size=11)
text_properties = FontProperties(fname=font_path, size=10)


def analysis():
        
    ACH_phase1_average_tasks_data_dataframe = read_csv(
        str(project_folder) 
        + '/output_analysis/'
        + 'phase1_average_tasks_data_dataframe.csv'
        )

    color_dict = {
            20000 : 'black',
            100000 : 'black',
            500000 : 'black',
    }


    df_awards = (
        ACH_phase1_average_tasks_data_dataframe
        >>mask(X.trait =='rewards')
        )
    # print(df_awards)

    #Friedman test
    filter_20k= df_awards.loc[(df_awards['depth'] == 20000)]
    filter_100k = df_awards.loc[(df_awards['depth'] == 100000)]
    filter_500k = df_awards.loc[(df_awards['depth'] == 500000)]
    # print('20k_filter: ', filter_20k)
    # print('100k_filter: ', filter_100k)
    # print('500k_filter: ', filter_500k)


    rewards_20k = filter_20k['evolved_population_value'].values.tolist()
    rewards_100k = filter_100k['evolved_population_value'].values.tolist()
    rewards_500k = filter_500k['evolved_population_value'].values.tolist()
    print('rewards_20k: ', rewards_20k)
    print('rewards_100k: ', rewards_100k)
    print('rewards_500k: ', rewards_500k)


    median_20k = statistics.median(rewards_20k)
    median_100k = statistics.median(rewards_100k)
    median_500k = statistics.median(rewards_500k)
    print('median_20k', median_20k)
    print('median_100k', median_100k)
    print('median_500k', median_500k)

    trait_names = ["rewards", "rewards", "rewards"]
    depths = [20000, 100000, 500000]
    values = [median_20k, median_100k, median_500k]
    median_dict = {'trait': trait_names, 'depth': depths, 'value': values}  
    rewards_median_data = DataFrame(median_dict)
    print('median data: ', rewards_median_data)

    res = friedmanchisquare(rewards_20k, rewards_100k, rewards_500k)
    stat = res.statistic
    p_value = res.pvalue

    print('Friedman stat, p_value: ', stat, p_value)

    # Dunn test
    data = [rewards_20k, rewards_100k, rewards_500k]
    # print('data: ', data)

    p_values= sp.posthoc_dunn(data, p_adjust = 'holm')
    print('Rewards P values:\n', p_values)

    sig = p_values < 0.05
    print('Rewards significant a=0.05:\n', sig)

    # # Generate fake data for framing.
    # trait_names = ["rewards", "rewards"] 
    # value = [0, 100000]
    # frame_nums = {'trait': trait_names, 'value': value}  
    # frame_data = DataFrame(frame_nums) 

    # rewards_plot = (
    #     ggplot(
    #         data = df_awards,
    #         mapping = aes(
    #             x='depth',
    #             y='evolved_population_value' ,
    #             color='factor(depth)'
    #             # color='factor(ancestor_seed)',
    #             # fill=black
    #         )
    #     )
    #     + geom_jitter(alpha=1, position = position_jitterdodge())
    #     + geom_crossbar(
    #         data=rewards_median_data,
    #         mapping=aes(
    #             x='depth',
    #             y='value',
    #             ymin='value', 
    #             ymax='value'),
    #         size=.125,
    #         color='black',
    #         width=.5,
    #         inherit_aes=False        
    #                 )
    #     + geom_blank(
    #             data=frame_data, 
    #             mapping=aes(y='value'), 
    #             inherit_aes=False)
        
    #     +scale_x_log10(
    #         name='Depth',
    #         breaks=[20000, 100000, 500000],
    #         labels=['20,000', '100,000', '500,000']
    #         )
    #     +scale_y_continuous(
    #         name='Rewarded Functions',
    #         breaks=[0, 25000, 50000, 75000, 100000],
    #         labels=['0', '25,000', '50,000', '75,000', '100,000']
    #         )
    #     + scale_color_manual(values = color_dict)
        
    #     + theme(
    #             figure_size=(5.2, 4.375),
    #             legend_title_align= 'center',
    #             text=element_text(fontproperties=text_properties),
    #             title=element_text(
    #                     margin= {'b': 20}, 
    #                     fontproperties=plot_title_properties),
    #             legend_position= 'none', 
    #             plot_background=element_rect(fill='white'),
    #             axis_text_x=element_text(
    #                     margin={'t':6}, 
    #                     color='black', 
    #                     fontproperties=text_properties),
    #             axis_text_y=element_text(
    #                     margin={'r':6}, 
    #                     color='black', 
    #                     fontproperties=text_properties),
    #             axis_title_x=element_text(
    #                     margin= {'t': 12}, 
    #                     fontproperties=axis_title_properties), 
    #             axis_title_y=element_text(
    #                     margin= {'r': 18}, 
    #                     fontproperties=axis_title_properties),
    #             axis_ticks_major_x=element_blank(),
    #             axis_ticks_major_y=element_blank(),
    #             rect=element_rect(
    #                     color='white', 
    #                     size=3, 
    #                     fill='white'),
    #             panel_grid_major_y=element_line(
    #                     linetype='solid', 
    #                     color='gray', 
    #                     size=.5),
    #             strip_text_x = element_text(
    #                     fontproperties=strip_text_properties)
    #     )
    # )

    # plot_name = 'phase1_rewards.pdf'
    # rewards_plot.save(
    #     filename = plot_name,
    #     path = output_folder
    #     + '/masked/phase1_plot'
    # )


    # Nonreward (unrewarded tasks)

    df_nonrewards = (
        ACH_phase1_average_tasks_data_dataframe
        >>mask(X.trait =='unrewarded_tasks')
        )
    # print(df_nonrewards)

    #Friedman test
    filter_20k= df_nonrewards.loc[(df_nonrewards['depth'] == 20000)]
    filter_100k = df_nonrewards.loc[(df_nonrewards['depth'] == 100000)]
    filter_500k = df_nonrewards.loc[(df_nonrewards['depth'] == 500000)]
    # print('20k_filter: ', filter_20k)
    # print('100k_filter: ', filter_100k)
    # print('500k_filter: ', filter_500k)


    nonrewards_20k = filter_20k['evolved_population_value'].values.tolist()
    nonrewards_100k = filter_100k['evolved_population_value'].values.tolist()
    nonrewards_500k = filter_500k['evolved_population_value'].values.tolist()
    print('nonrewards_20k: ', nonrewards_20k)
    print('nonrewards_100k: ', nonrewards_100k)
    print('nonrewards_500k: ', nonrewards_500k)


    median_20k = statistics.median(nonrewards_20k)
    median_100k = statistics.median(nonrewards_100k)
    median_500k = statistics.median(nonrewards_500k)
    print('median_20k', median_20k)
    print('median_100k', median_100k)
    print('median_500k', median_500k)

    trait_names = ["nonrewards", "nonrewards", "nonrewards"]
    depths = [20000, 100000, 500000]
    values = [median_20k, median_100k, median_500k]
    median_dict = {'trait': trait_names, 'depth': depths, 'value': values}  
    nonrewards_median_data = DataFrame(median_dict)
    print('median data: ', nonrewards_median_data)

    # Friedman test
    res = friedmanchisquare(nonrewards_20k, nonrewards_100k, nonrewards_500k)
    stat = res.statistic
    p_value = res.pvalue
    print('Friedman stat, p_value:\n', stat, p_value)

    # Dunn test
    data = [nonrewards_20k, nonrewards_100k, nonrewards_500k]
    # print('data: ', data)

    p_values= sp.posthoc_dunn(data, p_adjust = 'holm')
    print('nonreward significant a=0.05\n', p_values)

    sig = p_values < 0.05
    print(sig)

    # # Generate fake data for framing.
    # trait_names = ["nonrewards", "nonrewards"] 
    # value = [0, 100000]
    # frame_nums = {'trait': trait_names, 'value': value}  
    # frame_data = DataFrame(frame_nums) 

    # nonrewards_plot = (
    #     ggplot(
    #         data = df_nonrewards,
    #         mapping = aes(
    #             x='depth',
    #             y='evolved_population_value' ,
    #             color='factor(depth)',
    #             # fill=black
    #         )
    #     )
    #     + geom_jitter(alpha=1, position = position_jitterdodge(0.5))
    #     + geom_crossbar(
    #         data=nonrewards_median_data,
    #         mapping=aes(
    #             x='depth',
    #             y='value',
    #             ymin='value', 
    #             ymax='value'),
    #         size=.125,
    #         color='black',
    #         width=.5,
    #         inherit_aes=False        
    #                 )
    #     + geom_blank(
    #             data=frame_data, 
    #             mapping=aes(y='value'), 
    #             inherit_aes=False)
        
    #     +scale_x_log10(
    #         name='Depth',
    #         breaks=[20000, 100000, 500000],
    #         labels=['20,000', '100,000', '500,000']
    #         )
    #     +scale_y_continuous(
    #         name='Nonrewarded Functions',
    #         breaks=[0, 25000, 50000, 75000, 100000],
    #         labels=['0', '25,000', '50,000', '75,000', '100,000']
    #         )
    #     + scale_color_manual(values = color_dict)
        
    #     + theme(
    #             figure_size=(5.2, 4.375),
    #             legend_title_align= 'center',
    #             text=element_text(fontproperties=text_properties),
    #             title=element_text(
    #                     margin= {'b': 20}, 
    #                     fontproperties=plot_title_properties),
    #             legend_position= 'none', 
    #             plot_background=element_rect(fill='white'),
    #             axis_text_x=element_text(
    #                     margin={'t':6}, 
    #                     color='black', 
    #                     fontproperties=text_properties),
    #             axis_text_y=element_text(
    #                     margin={'r':6}, 
    #                     color='black', 
    #                     fontproperties=text_properties),
    #             axis_title_x=element_text(
    #                     margin= {'t': 12}, 
    #                     fontproperties=axis_title_properties), 
    #             axis_title_y=element_text(
    #                     margin= {'r': 18}, 
    #                     fontproperties=axis_title_properties),
    #             axis_ticks_major_x=element_blank(),
    #             axis_ticks_major_y=element_blank(),
    #             rect=element_rect(
    #                     color='white', 
    #                     size=3, 
    #                     fill='white'),
    #             panel_grid_major_y=element_line(
    #                     linetype='solid', 
    #                     color='gray', 
    #                     size=.5),
    #             strip_text_x = element_text(
    #                     fontproperties=strip_text_properties)
    #     )
    # )

    # plot_name = 'phase1_nonrewards.pdf'
    # nonrewards_plot.save(
    #     filename = plot_name,
    #     path = output_folder
    #     + '/masked/phase1_plot'
    # )

    # g1 = rewards_plot
    # g2 = nonrewards_plot 

    # g1 = pw.load_ggplot(g1)
    # g2 = pw.load_ggplot(g2)


    # # g1 = pw.load_ggplot(g1, figsize=(3,3))
    # # g2 = pw.load_ggplot(g2, figsize=(3,3))

    # g12= g1|g2
    # g12.savefig(fname= output_folder 
    #                 + '/masked/phase1_plot/phase1_combined_functions_plot.tif',
    #                 format= 'tif'
    #                 )
    return ''

log_name= 'phase1_average_tasks_data_stats_analysis_log.txt'  
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
        