"""
Perform the ANOVA and estimated variance components analyses.

function:: def make_ANOVAandVariance_trajectory_dict() -> str

1. Run make_ANOVAandVariance_trajectory_dict().
2. Save the analysis dict as a csv.
3. Save the Adaptation, Chance, and History (ACH) dict as a csv.
4. Import the analysis csv and sort it.
5. Import the ACH csv and sort it.
6. Print 'Date, time, and year: date_time_year
          Module: module_path
          Saved dataframe: analysis_dataframe_location
          Saved dataframe: ACH_dataframe_location'
"""

__author__ = 'Jason Bundy'
__version__ = '1.0'

from collections import namedtuple, defaultdict
from csv import writer
from dfply import arrange, group_by, mask, mutate, select, summarize, X
from math import sqrt as sqrt
from numpy import log10 as log10, std as std
from pandas import read_csv
from pandas.api.types import CategoricalDtype
from pathlib import Path
from plotnine import *
from scipy import stats as stats
from sys import path
from time import asctime, localtime
from time import time as t_time

module_path = Path(__file__).resolve()
analysis_folder = module_path.parent
scripts_folder = analysis_folder.parent
operations_folder = str(scripts_folder) + '/operations'
project_folder = scripts_folder.parent
output_folder = str(project_folder) + '/output_analysis'
path.insert(0, str(operations_folder))
path.insert(0, str(scripts_folder))

"""
Establish a list of keys for the dictionaries we'll be using.
"""
keys = []
ACH_keys = []

"""
Establish some default dicts we'll add the data to later
"""
analysis_trajectory_data_dict = defaultdict(dict)
ACH_estimate_trajectory_dict = defaultdict(dict)

ACH_trajectory_phase2_dataframe_name = 'phase2_dataframe.csv'
ACH_trajectory_phase2_dataframe = read_csv(
    output_folder 
    + '/' 
    + ACH_trajectory_phase2_dataframe_name
    )
ancestor_dataframe = read_csv(
    output_folder 
    + '/' 
    + ACH_trajectory_phase2_dataframe_name
    )

ACH_trajectory_phase2_dataframe = (
    ACH_trajectory_phase2_dataframe 
    >> select(
        X.environment, 
        X.ancestor_run_length, 
        X.lineage, 
        X.replicate, 
        X.time, 
        X.trait, 
        X.ancestor_value, 
        X.evolved_population_average_value, 
        X.ancestor_value_log10, 
        X.evolved_population_average_value_log10, 
        X.evolved_relative_value, 
        X.evolved_relative_value_log10
        ))
ancestor_dataframe = (
    ancestor_dataframe 
    >> select(
        X.environment, 
        X.ancestor_run_length, 
        X.lineage, 
        X.replicate, 
        X.time, 
        X.trait, 
        X.ancestor_value, 
        X.evolved_population_average_value, 
        X.ancestor_value_log10, 
        X.evolved_population_average_value_log10, 
        X.evolved_relative_value, 
        X.evolved_relative_value_log10
        ))


def make_ANOVAandVariance_trajectory_dict():

    """
    Make analysis and Adaptation, Chance, & History estimates dicts.

    :return: 'Date, time, and year: date_time_year
              Module: module_path
              Saved dict: analysis_trajectory_data_dict
              Saved dict: ACH_estimate_trajectory_dict'
    :rtype: str
    """
        
    environments = ['orthogonal', 'overlapping']
    run_lengths = ['20000', '100000', '500000'] 
    times = range(0, 101000, 1000)
    traits = ['fitness', 'genome_length']

    final_update_num = 100000

    combined_filters = [
        (
            environment, 
            run_length, 
            time, 
            trait
            ) 
                for environment in environments 
                for run_length in run_lengths 
                for time in times for trait in traits
            ]
    
    for each in combined_filters:
        environment = each[0]
        run_length = each[1]
        time = each[2]
        trait = each[3]
    
        key = (
            'Environment_%s_RunLength_%s_Time_%d_Trait_%s' 
            % (
                environment, 
                run_length, 
                time, 
                trait
                ))
        keys.append(key)
        ancestral_key = (
            'Environment_%s_RunLength_%s_Time_%d_Trait_%s_Ancestral' 
            % (
                environment, 
                run_length, 
                time, 
                trait
                ))
        adaptation_key = (
            'Environment_%s_RunLength_%s_Time_%d_Trait_%s_Adaptation' 
            % (
                environment, 
                run_length, 
                time, 
                trait
                ))
        chance_key = (
            'Environment_%s_RunLength_%s_Time_%d_Trait_%s_Chance' 
            % (
                environment, 
                run_length, 
                time, 
                trait
                ))
        history_key = (
            'Environment_%s_RunLength_%s_Time_%d_Trait_%s_History' 
            % (
                environment, 
                run_length, 
                time, 
                trait
                ))
        ACH_keys.append(ancestral_key)
        ACH_keys.append(adaptation_key)
        ACH_keys.append(chance_key)
        ACH_keys.append(history_key)
        ACH_estimate_trajectory_dict[ancestral_key] = dict
        ACH_estimate_trajectory_dict[adaptation_key] = dict
        ACH_estimate_trajectory_dict[chance_key] = dict
        ACH_estimate_trajectory_dict[history_key] = dict
        analysis_trajectory_data_dict[key] = dict
       
        ACH_trajectory_phase2_dataframe_masked =  (
            ACH_trajectory_phase2_dataframe 
            >> mask(
                X.environment == environment, 
                X.ancestor_run_length == int(run_length), 
                X.time== time, 
                X.trait== trait
                ))
    

        """
        ANOVA and Variance Component Calculations
        """
        """
        Number of groups (lineages)
        """
        a = 10
        """
        Number of replicates (i.e. populations- 1001-1010), per group.
        """
        n = 10 # Note the lower-case n (within group observations).
        """
        Total number of observations
        """
        N = a * n # Total observations

        """
        Total Mean Square Calculations
        """
        ms_total_dataframe = (
            ACH_trajectory_phase2_dataframe_masked 
            >> mutate(
                grand_mean = X.evolved_population_average_value_log10.mean()
                ) 
            >> mutate(
                deviation_from_grand_mean = (
                    X.evolved_population_average_value_log10 
                    - X.grand_mean
                    )) 
            >> mutate(
                deviation_from_grand_mean_sqrd = (
                    X.deviation_from_grand_mean**2
                    )))
        ss_total_from_data = (
            ms_total_dataframe
                ['deviation_from_grand_mean_sqrd']
                    .sum()
                )
        df_total = N - 1
        ms_total = ss_total_from_data/df_total
        ms_total_dataframe = (
            ms_total_dataframe 
            >> mutate(
                ss_total = ss_total_from_data, 
                df_total = df_total, 
                ms_total = ms_total
                ))
     
        """
        Grand Mean
        """
        grand_mean = float(ms_total_dataframe['grand_mean'].iloc[0])
   
        """
        Grab information about the initial spread of the trait.
        """
        ms_ancestral_dataframe = (
            ancestor_dataframe 
            >> mask(
                X.environment == environment, 
                X.ancestor_run_length == int(run_length), 
                X.time== 0, 
                X.trait== trait
                )) 

        ancestral_grand_mean = ((
            ms_ancestral_dataframe['evolved_population_average_value_log10']
                .sum()
            )
            / (
                len(
                    ms_ancestral_dataframe
                        ['evolved_population_average_value_log10']
                        )))
        
        ms_ancestral_dataframe = (
            ms_ancestral_dataframe 
            >> group_by(X.lineage) 
            >> summarize(
                group_mean = X.evolved_population_average_value_log10.mean()
                ) 
            >> mutate(
                grand_mean = ancestral_grand_mean,
                group_deviations = (X.group_mean - ancestral_grand_mean)
                ) 
            >> mutate(
                group_deviations_sqrd = (X.group_deviations**2)
                ))
        sum_of_squared_ancestral_group_deviations = (
            ms_ancestral_dataframe
            ['group_deviations_sqrd'].
            sum()
            )
        ss_ancestral = (sum_of_squared_ancestral_group_deviations * n) 
        df_ancestral = a - 1
        ms_ancestral = (ss_ancestral / df_ancestral)
        observed_variance_ancestral_group = ms_ancestral/n
        ms_ancestral_dataframe = (
            ms_ancestral_dataframe 
            >> mutate(
                sum_of_squared_ancestral_group_deviations = (
                    sum_of_squared_ancestral_group_deviations
                    ),
                ss_ancestral = ss_ancestral, 
                df_ancestral = df_ancestral, 
                ms_ancestral = ms_ancestral, 
                observed_variance_ancestral_group = (
                    observed_variance_ancestral_group
                    )))

        alpha= .05
        sd_ancestral = sqrt(
            float(
                ms_ancestral_dataframe
                    ['observed_variance_ancestral_group']
                        .iloc[0]
                        ))
        sd_lower_endpoint_ancestral = (
            (df_ancestral * sd_ancestral)
            / stats.chi2.ppf(
                (1-(alpha/2)), df_ancestral
                ))
        sd_upper_endpoint_ancestral = (
            (df_ancestral * sd_ancestral)
            / stats.chi2.ppf(
                (alpha/2), df_ancestral
                ))

        """
        Groups (i.e. lineages- 101-103)
        Group means (ancestor run lengths- 4k, 20k, 50k)
        Mean square between groups
        """
        ms_group_dataframe = (
            ACH_trajectory_phase2_dataframe_masked 
            >> group_by(X.lineage) 
            >> summarize(
                group_mean = X.evolved_population_average_value_log10.mean()) 
            >> mutate(
                grand_mean = grand_mean,
                group_deviations = (X.group_mean - grand_mean)
                ) 
            >> mutate(
                group_deviations_sqrd = (X.group_deviations**2)
                ))
        sum_of_squared_group_deviations = (
            ms_group_dataframe
            ['group_deviations_sqrd']
            .sum()
            )
        ss_group = (sum_of_squared_group_deviations * n)
        df_group = a - 1
        ms_group = (ss_group / df_group)   
        ms_group_dataframe = (
            ms_group_dataframe 
            >> mutate(
                sum_of_squared_group_deviations = (
                    sum_of_squared_group_deviations),
                ss_group = ss_group, 
                df_group = df_group, 
                ms_group = ms_group
                ))
    
        """
        Replicate mean square within groups
        """
        ms_replicate_dataframe = (
            ACH_trajectory_phase2_dataframe_masked 
            >> group_by(X.lineage) 
            >> mutate(
                group_mean = X.evolved_population_average_value_log10.mean()
                ) 
            >> mutate(
                replicate_deviations = (
                    X.evolved_population_average_value_log10 
                    - X.group_mean
                    )
                        .round(15) # Avoid non-zero values at update 0.
                        ) 
            >> mutate(
                replicate_deviations_sqrd = (X.replicate_deviations**2)
                ))
        ss_replicate = (
            ms_replicate_dataframe
                ['replicate_deviations_sqrd']
                    .sum()
                    )
        df_replicate = a * (n-1)  #=N-a
        ms_replicate = (ss_replicate / df_replicate) 
        ms_replicate_dataframe = (
            ms_replicate_dataframe 
            >> mutate(
                ss_replicate = ss_replicate, 
                df_replicate = df_replicate, 
                ms_replicate = ms_replicate
                ))

        """
        Total sum of squares, different than when calculated from data.
        Probably not an issue. 
        Might be from float calculation.
        """
        ss_total_ssgroup_plus_ssreplicate = ss_group + ss_replicate

        """
        P-value lookup:
        f-ratio = MSlevel/MSerror 
        df numerator = degress of freedom for numerator 
        df denominator = degress of freedom for denominator

        You can verify with a website for lookup:
        https://www.socscistatistics.com/pvalues/fdistribution.aspx
        https://www.danielsoper.com/statcalc/calculator.aspx?id=7
        http://epitools.ausvet.com.au/content.php?page=f_dist
        """
        numerator_df = df_group
        denominator_df = df_replicate

        f_ratio = (ms_group/ms_replicate)

        """F-ratio p-value calculation"""
        cumulative_distribution_function = stats.f.cdf(
            f_ratio, 
            df_group, 
            df_replicate
            )
        p_value = 1 - cumulative_distribution_function 
        if p_value < 0.00001:
            p_value_string = '****<0.00001'
        elif p_value < 0.0001:
            p_value_string = '***<0.0001'
        elif p_value < 0.001:
            p_value_string = '**<0.001'
        elif p_value < 0.05:
            p_value_string = '*%s' % (p_value)   
        else:
            p_value_string = str(p_value)

        if time == final_update_num: 
            """
            Produce and save ANOVA table for final update.
            """ 
            anova = namedtuple(
                'anova', 
                    'source ' 
                    'df ' 
                    'ss ' 
                    'ms ' 
                    'f_ratio ' 
                    'p_value ' 
                    'p_value_string '
                )
            group = anova(
                'lineage', 
                    df_group, 
                    ss_group, 
                    ms_group, 
                    f_ratio, 
                    p_value, 
                    p_value_string
                    )
            replicate = anova(
                'replicate', 
                    df_replicate, 
                    ss_replicate, 
                    ms_replicate, 
                    None, 
                    None, 
                    None
                    )
            total = anova(
                'total', 
                    df_total, 
                    ss_total_from_data, 
                    ms_total, 
                    None, 
                    None, 
                    None
                    )
            anova_dict = {
                'group': group, 
                'replicate': replicate, 
                'total': total
                }
            anova_csv_name = (
                'anova_table_%s_%s_%s.csv' 
                % (
                    environment, 
                    run_length, 
                    trait
                    ))
            anova_csv_location = (
                output_folder 
                + '/masked/anova_tables/' 
                + anova_csv_name
                )
            with open(anova_csv_location, 'w+', newline='') as csvfile:
                csv_writer = writer(csvfile, delimiter=',')
                csv_writer.writerow([
                    'source', 
                    'df', 
                    'ss', 
                    'ms', 
                    'f_ratio', 
                    'p_value', 
                    'p_value_string'
                    ])
                for anova_key, anova_attributes in anova_dict.items():
                    csv_writer.writerow([*anova_attributes]) 
        else:pass

        """
        Variance Components
        1. Use observed variance to calculate estimated variance.
        2. Report estimated variance components.
        """
        # Account for number of measurements in each group
        observed_variance_group = ms_group/n 
        """
        observed_variance_total = ss_total_from_data/df_total  
        -This is equivalent to meansquare (ms_total). 
        """

        """
        Estimated Variance Components
        -Set to 0 if they are negative to avoid negative variance.
        """
        estimated_variance_replicate = ms_replicate  #same as ANOVA
        estimated_variance_group = (
            observed_variance_group-(estimated_variance_replicate/n)
            ) 
        if estimated_variance_group < 0:
            estimated_variance_group = 0
        estimated_variance_total = (
            estimated_variance_group + estimated_variance_replicate
            )

        """
        Estimated Variance Component Confidence Intervals
        Confidence interval calculations: 
        Use stats.chi.ppf for percent point function. 
        Thi is the inverse of cdf — percentiles.
        """
        """
        Replicate
        """
        variance_lower_endpoint_replicate = ((
            df_replicate * estimated_variance_replicate
            )
            / stats.chi2.ppf((1-(alpha/2)), df_replicate)
            )
        variance_upper_endpoint_replicate = ((
            df_replicate * estimated_variance_replicate
            )
            / stats.chi2.ppf((alpha/2), df_replicate)
            )
        """
        Group
        """
        variance_lower_endpoint_group = ((
            df_group * estimated_variance_group)
            / stats.chi2.ppf((1-(alpha/2)), df_group)
            )
        variance_upper_endpoint_group = ((
            df_group * estimated_variance_group
            )
            / stats.chi2.ppf((alpha/2), df_group)
            )
        """
        Total
        """
        variance_lower_endpoint_total = ((
            df_total * estimated_variance_total)
            / stats.chi2.ppf((1-(alpha/2)), df_total)
            )
        variance_upper_endpoint_total = ((
            df_total * estimated_variance_total
            )
            / stats.chi2.ppf((alpha/2), df_total)
            )
        """
        Percent of Variation
        """
        variance_percentage_replicate = ((
            estimated_variance_replicate / estimated_variance_total
            ) 
            * 100
            )
        variance_percentage_group = ((
            estimated_variance_group / estimated_variance_total
            ) * 100
            )
        variance_percentage_total = ((
            estimated_variance_total / estimated_variance_total
            ) * 100
            )
        """
        Standard Deviations-not additive, 
        -We use these to be on the same scale as changes in mean.
        """
        sd_replicate = sqrt(estimated_variance_replicate)
        sd_group = sqrt(estimated_variance_group)
        sd_total = sqrt(estimated_variance_total)
        
        """
        Standard Deviation confidence intervals
        -Created like estimated variance confidence intervals. (Chi^2)
        """
        
        """
        Replicate
        observed_variance_replicate = ms_replicate (from ANOVA)
        """
        sd_lower_endpoint_replicate = ((
            df_replicate * sd_replicate
            )
            / stats.chi2.ppf((1-(alpha/2)), df_replicate)
            )
        sd_upper_endpoint_replicate = ((
            df_replicate * sd_replicate
            )
            / stats.chi2.ppf((alpha/2), df_replicate)
            )
        """
        Group
        """
        sd_lower_endpoint_group = ((
            df_group * sd_group
            )
            / stats.chi2.ppf((1-(alpha/2)), df_group)
            )
        sd_upper_endpoint_group = ((
            df_group * sd_group
            )
            / stats.chi2.ppf((alpha/2), df_group)
            )
        """
        Total
        """
        sd_lower_endpoint_total = ((
            df_total * sd_total
            )
            / stats.chi2.ppf((1-(alpha/2)), df_total)
            )
        sd_upper_endpoint_total = ((
            df_total * sd_total
            ) 
            / stats.chi2.ppf((alpha/2), df_total)
            )

        if time == final_update_num:
            """
            Produce and save estimated variance component table
            with standard deviations and confidence intervals.
            """
            estimated_variance = namedtuple(
                'estimated_variance', 
                    'source '
                    'df '
                    'ms '
                    'estimated_variance ' 
                    'var_lower_endpoint ' 
                    'var_upper_endpoint '
                    'total_variance_percentage ' 
                    'sd ' 
                    'sd_lower_endpoint ' 
                    'sd_upper_endpoint'
                )
            group_estimated_variance = estimated_variance(
                'lineage', 
                    df_group, 
                    ms_group, 
                    estimated_variance_group, 
                    variance_lower_endpoint_group, 
                    variance_upper_endpoint_group, 
                    variance_percentage_group, 
                    sd_group, 
                    sd_lower_endpoint_group, 
                    sd_upper_endpoint_group
                    )
            replicate_estimated_variance = estimated_variance(
                'replicate', 
                    df_replicate, 
                    ms_replicate, 
                    estimated_variance_replicate, 
                    variance_lower_endpoint_replicate, 
                    variance_upper_endpoint_replicate, 
                    variance_percentage_replicate, 
                    sd_replicate, 
                    sd_lower_endpoint_replicate, 
                    sd_upper_endpoint_replicate
                    )
            total_estimated_variance = estimated_variance(
                'total', 
                    df_total, 
                    ms_total, 
                    estimated_variance_total, 
                    variance_lower_endpoint_total, 
                    variance_upper_endpoint_total, 
                    variance_percentage_total, 
                    sd_total, 
                    sd_lower_endpoint_total, 
                    sd_upper_endpoint_total
                    )
            estimated_variance_dict = {
                'group_estimated_variance': group_estimated_variance, 
                'replicate_estimated_variance': replicate_estimated_variance, 
                'total_estimated_variance': total_estimated_variance
                }
            estimated_variance_csv_name = (
                'masked/estimated_variance/estimated_variance_%s_%s_%s.csv' 
                % (
                    environment, 
                    run_length, 
                    trait
                    ))
            estimated_variance_csv_location = (
                output_folder 
                + '/' 
                + estimated_variance_csv_name
                )
            with open(
                    estimated_variance_csv_location, 
                    'w+', 
                    newline=''
                    ) as csvfile:
                csv_writer = writer(csvfile, delimiter=',')
                csv_writer.writerow([
                    'source', 
                    'df', 
                    'ms', 
                    'estimated_variance', 
                    'var_lower_endpoint', 
                    'var_upper_endpoint', 
                    'total_variance_percentage', 
                    'sd', 
                    'sd_lower_endpoint', 
                    'sd_upper_endpoint'
                    ])
                for (
                        estimated_variance_key, 
                        estimated_variance_attributes
                        ) in estimated_variance_dict.items():
                    csv_writer.writerow([*estimated_variance_attributes]
                    )
        else:pass
    
        """
        Quantifying Adaptation
        Paired T-test
        """
        adaptation_t_test_dataframe = (
            ACH_trajectory_phase2_dataframe_masked
            >> mutate(
                difference = (
                    X.evolved_population_average_value_log10 
                    - X.ancestor_value_log10
                    ))
            >> mutate(difference_sqrd = (X.difference ** 2))
            )
        adaptation_mean_difference = (
            adaptation_t_test_dataframe['difference'].sum() / N
            )
        difference_standard_deviation = (
            sqrt((
                adaptation_t_test_dataframe['difference_sqrd'].sum()
                ) 
                / (N-1)
                ))
        difference_standard_error = difference_standard_deviation / sqrt(N)
        difference_lower_endpoint = (
            adaptation_mean_difference - (1.96 * difference_standard_error)
            )
        difference_upper_endpoint = (
            adaptation_mean_difference + (1.96 * difference_standard_error)
            )
        t = adaptation_mean_difference / difference_standard_error

        """
        Calculate p-value for t test.
        Perform two-tailed test.
        df = df_total (i.e. N-1) 
        """
        t_p_value = stats.t.sf(t, df = df_total) * 2
        if t_p_value < 0.00001:
            t_p_value_string = '****<0.00001'
        elif t_p_value < 0.0001:
            t_p_value_string = '***<0.0001'
        elif t_p_value < 0.001:
            t_p_value_string = '**<0.001'
        elif t_p_value < 0.05:
            t_p_value_string = '*%s' % (t_p_value)   
        else:
            t_p_value_string = str(t_p_value)        

        if time == final_update_num:
            """
            Save t-test results.
            """
            paired_ttest = namedtuple(
                't_test', 
                    'mean_difference ' 
                    'df ' 
                    'sd ' 
                    'se ' 
                    'lower_endpoint ' 
                    'upper_endpoint ' 
                    't p_value ' 
                    'p_value_string'
                    )
            adaptation_ttest = paired_ttest(
                adaptation_mean_difference, 
                df_total, 
                difference_standard_deviation, 
                difference_standard_error, 
                difference_lower_endpoint, 
                difference_upper_endpoint, 
                t, 
                t_p_value, 
                t_p_value_string
                )
            adaptation_ttest_dict = {'adaptation_ttest': adaptation_ttest}
            adaptation_ttest_csv_name = (
                'masked/paired_ttest/adaptation_paired_ttest_%s_%s_%s.csv' 
                % (
                    environment, 
                    run_length, 
                    trait
                    ))
            adaptation_ttest_csv_location = (
                output_folder 
                + '/' 
                + adaptation_ttest_csv_name
                )
            with open(
                    adaptation_ttest_csv_location, 
                    'w+', 
                    newline=''
                    ) as csvfile:
                csv_writer = writer(csvfile, delimiter=',')
                csv_writer.writerow([
                    'mean_difference', 
                    'df', 
                    'sd', 
                    'se', 
                    'lower_endpoint', 
                    'upper_endpoint', 
                    't', 
                    'p_value', 
                    'p_value_string'
                    ])
                for (
                    ttest_key, 
                    ttest_attributes
                    ) in adaptation_ttest_dict.items():
                    csv_writer.writerow([*ttest_attributes])
        else:pass

        """
        Combining ANOVA, variance components, and paired t-test into one dict
        """
        analysis_trajectory_data_dict[key] = {
            'environment': environment, 
            'run_length': run_length, 
            'time': time, 
            'trait': trait,
            'group_anova_source': 'lineage', 
            'df_group': df_group, 
            'ss_group': ss_group, 
            'ms_group': ms_group, 
            'f_ratio': f_ratio, 
            'f_ratio_p_value': p_value, 
            'f_ratio_p_value_string': p_value_string,
            'replicate_anova_source': 'replicate', 
            'df_replicate': df_replicate, 
            'ss_replicate': ss_replicate, 
            'ms_replicate': ms_replicate,  
            'total_anova_source': 'total', 
            'df_total': df_total, 
            'ss_total': ss_total_from_data, 
            'ms_total': ms_total,
            'group_estimated_variance_source': 'lineage', 
            'df_group': df_group, 
            'estimated_variance_group': estimated_variance_group, 
            'variance_lower_endpoint_group': variance_lower_endpoint_group, 
            'variance_upper_endpoint_group': variance_upper_endpoint_group, 
            'variance_percentage_group': variance_percentage_group, 
            'sd_group': sd_group, 
            'sd_lower_endpoint_group': sd_lower_endpoint_group, 
            'sd_upper_endpoint_group': sd_upper_endpoint_group,
            'replicate_estimated_variance_source': 'replicate', 
            'df_replicate': df_replicate, 
            'estimated_variance_replicate': estimated_variance_replicate, 
            'variance_lower_endpoint_replicate': variance_lower_endpoint_replicate, 
            'variance_upper_endpoint_replicate': variance_upper_endpoint_replicate, 
            'variance_percentage_replicate': variance_percentage_replicate, 
            'sd_replicate': sd_replicate, 
            'sd_lower_endpoint_replicate': sd_lower_endpoint_replicate, 
            'sd_upper_endpoint_replicate': sd_upper_endpoint_replicate,
            'total_estimated_variance_source': 'total', 
            'df_total': df_total, 
            'estimated_variance_total': estimated_variance_total, 
            'variance_lower_endpoint_total': variance_lower_endpoint_total, 
            'variance_upper_endpoint_total': variance_upper_endpoint_total, 
            'variance_percentage_total': variance_percentage_total, 
            'sd_total': sd_total, 
            'sd_lower_endpoint_total': sd_lower_endpoint_total, 
            'sd_upper_endpoint_total': sd_upper_endpoint_total,
            'adaptation_ttest_source': 'evolved_minus_ancestor', 
            'adaptation_mean_difference': adaptation_mean_difference, 
            'df_total': df_total, 
            'difference_standard_deviation': difference_standard_deviation, 
            'difference_standard_error': difference_standard_error, 
            'difference_lower_endpoint': difference_lower_endpoint, 
            'difference_upper_endpoint': difference_upper_endpoint, 
            't': t, 
            't_p_value': t_p_value, 
            't_p_value_string': t_p_value_string
            } 

        """
        Adaptation, Chance, and History estimates
        Combine Adaptation, Chance, and History estimates in a dict.
        """
        ancestral_series = (
        'environment_%s_run_length_%s_trait_%s_source_ancestral' 
        % (environment, run_length, trait))
        adaptation_series = (
        'environment_%s_run_length_%s_trait_%s_source_adaptation' 
        % (environment, run_length, trait))
        chance_series = (
        'environment_%s_run_length_%s_trait_%s_source_chance' 
        % (environment, run_length, trait))
        history_series = (
        'environment_%s_run_length_%s_trait_%s_source_history' 
        % (environment, run_length, trait))

        ACH_estimate_trajectory_dict[adaptation_key] = {
            'series': adaptation_series, 
            'environment': environment, 
            'run_length': run_length, 
            'time': time, 
            'trait': trait,
            'source': 'adaptation', 
            'value': adaptation_mean_difference, 
            'lower_endpoint': difference_lower_endpoint, 
            'upper_endpoint': difference_upper_endpoint
            }
        ACH_estimate_trajectory_dict[chance_key] = {
            'series': chance_series, 
            'environment': environment, 
            'run_length': run_length, 
            'time': time, 
            'trait': trait,
            'source': 'chance', 
            'value': sd_replicate, 
            'lower_endpoint': sd_lower_endpoint_replicate, 
            'upper_endpoint': sd_upper_endpoint_replicate
            }
        ACH_estimate_trajectory_dict[history_key] = {
            'series': history_series, 
            'environment': environment, 
            'run_length': run_length, 
            'time': time, 
            'trait': trait,
            'source': 'history', 
            'value': sd_group, 
            'lower_endpoint': sd_lower_endpoint_group, 
            'upper_endpoint': sd_upper_endpoint_group
            }
        ACH_estimate_trajectory_dict[ancestral_key] = {
            'series': ancestral_series, 
            'environment': environment, 
            'run_length': run_length, 
            'time': time, 
            'trait': trait,
            'source': 'ancestral', 
            'value': sd_ancestral, 
            'lower_endpoint': sd_lower_endpoint_ancestral, 
            'upper_endpoint': sd_upper_endpoint_ancestral
            }

    date_time_year = asctime(localtime(t_time()))       
    
    return (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved dict: analysis_trajectory_data_dict \n'
            'Saved dict: ACH_estimate_trajectory_dict' 
            % (
                date_time_year,
                module_path
                ))

if __name__ == '__main__':
    
    """
    Run the function that makes the trajectory dicts.
    """
    print(make_ANOVAandVariance_trajectory_dict())

    """
    Save the analysis trajectory dict as a csv.
    """
    analysis_trajectory_data_dict_name = 'analysis_trajectory.csv' 
    analysis_trajectory_data_dict_location = (
        output_folder 
        + '/raw/' 
        + analysis_trajectory_data_dict_name
        )
    with open(
            analysis_trajectory_data_dict_location, 
            'w+', 
            newline=''
            ) as csvfile:
        csv_writer = writer(csvfile, delimiter=',')
        csv_writer.writerow([
            'environment', 
            'run_length', 
            'time', 
            'trait',
            'group_anova_source', 
            'df_group', 
            'ss_group', 
            'ms_group', 
            'f_ratio', 
            'f_ratio_p_value', 
            'f_ratio_p_value_string', 
            'replicate_anova_source', 
            'df_replicate', 
            'ss_replicate', 
            'ms_replicate', 
            'total_anova_source', 
            'df_total', 
            'ss_total', 
            'ms_total',
            'estimated_variance_group_source', 
            'estimated_variance_group', 
            'variance_lower_endpoint_group', 
            'variance_upper_endpoint_group', 
            'variance_percentage_group', 
            'sd_group', 
            'sd_lower_endpoint_group', 
            'sd_upper_endpoint_group',
            'replicate_estimated_variance_source', 
            'estimated_variance_replicate', 
            'variance_lower_endpoint_replicate', 
            'variance_upper_endpoint_replicate', 
            'variance_percentage_replicate', 
            'sd_replicate', 
            'sd_lower_endpoint_replicate', 
            'sd_upper_endpoint_replicate',
            'estimated_variance_total_source', 
            'estimated_variance_total', 
            'variance_lower_endpoint_total', 
            'variance_upper_endpoint_total', 
            'variance_percentage_total', 
            'sd_total', 
            'sd_lower_endpoint_total', 
            'sd_upper_endpoint_total',
            'adaptation_ttest_source', 
            'adaptation_mean_difference', 
            'difference_standard_deviation', 
            'difference_standard_error', 
            'difference_lower_endpoint', 
            'difference_upper_endpoint', 
            't', 
            't_p_value', 
            't_p_value_string'
            ])
        for (
                analysis_key, 
                analysis_attributes
                ) in analysis_trajectory_data_dict.items():
            csv_writer.writerow([*analysis_attributes.values()])

    """
    Save the Adaptation, Chance, and History estimates dict as a csv.
    """
    ACH_estimate_trajectory_dict_name = 'ACH_estimate_trajectory.csv' 
    ACH_estimate_trajectory_dict_location = (
        output_folder 
        + '/raw/' 
        + ACH_estimate_trajectory_dict_name
        )
    with open(
            ACH_estimate_trajectory_dict_location, 
            'w+', 
            newline=''
            ) as csvfile:
        csv_writer = writer(csvfile, delimiter=',')
        csv_writer.writerow([
            'series', 
            'environment', 
            'run_length', 
            'time', 
            'trait', 
            'source', 
            'value', 
            'lower_endpoint', 
            'upper_endpoint'
            ])
        for ACH_key, ACH_attributes in ACH_estimate_trajectory_dict.items():
            csv_writer.writerow([*ACH_attributes.values()])

    """
    Import the analysis csv and sort it.
    """
    unsorted_analysis = read_csv(analysis_trajectory_data_dict_location)
    analysis_dataframe = (
        unsorted_analysis 
        >> select(
            X.environment, 
            X.run_length, 
            X.time, 
            X.trait, 
            X.group_anova_source, 
            X.df_group, 
            X.ss_group, 
            X.ms_group, 
            X.f_ratio, 
            X.f_ratio_p_value, 
            X.f_ratio_p_value_string, 
            X.replicate_anova_source, 
            X.df_replicate, 
            X.ss_replicate, 
            X.ms_replicate, 
            X.total_anova_source, 
            X.df_total,
            X.ss_total, 
            X.ms_total, 
            X.estimated_variance_group_source, 
            X.df_group, 
            X.estimated_variance_group, 
            X.variance_lower_endpoint_group, 
            X.variance_upper_endpoint_group, 
            X.variance_percentage_group, 
            X.sd_group, 
            X.sd_lower_endpoint_group, 
            X.sd_upper_endpoint_group,
            X.replicate_estimated_variance_source, 
            X.df_replicate, 
            X.estimated_variance_replicate, 
            X.variance_lower_endpoint_replicate, 
            X.variance_upper_endpoint_replicate, 
            X.variance_percentage_replicate, 
            X.sd_replicate, 
            X.sd_lower_endpoint_replicate, 
            X.sd_upper_endpoint_replicate,
            X.estimated_variance_total_source, 
            X.df_total, 
            X.estimated_variance_total, 
            X.variance_lower_endpoint_total, 
            X.variance_upper_endpoint_total, 
            X.variance_percentage_total, 
            X.sd_total, 
            X.sd_lower_endpoint_total, 
            X.sd_upper_endpoint_total,
            X.adaptation_ttest_source, 
            X.adaptation_mean_difference, 
            X.df_total, 
            X.difference_standard_deviation, 
            X.difference_standard_error, 
            X.difference_lower_endpoint, 
            X.difference_upper_endpoint, 
            X.t, 
            X.t_p_value, 
            X.t_p_value_string
            ) 
            >> arrange(
                X.trait, 
                X.environment,
                 X.run_length, 
                 X.time
                 )) 
    analysis_dataframe_csv_name = 'analysis_trajectory_dataframe.csv'
    analysis_dataframe_location =  (
        output_folder 
        + '/' 
        + analysis_dataframe_csv_name
        )
    analysis_dataframe.to_csv(analysis_dataframe_location)    
 
    """
    Import the Adaptation, Chance, and History csv and sort it.
    """
    unsorted_ACH_trajectory = read_csv(ACH_estimate_trajectory_dict_location)
    sorted_ACH_trajectory_dataframe = (
        unsorted_ACH_trajectory 
        >> select(
            X.series, 
            X.environment, 
            X.run_length, 
            X.time,
            X.trait, 
            X.source, 
            X.value, 
            X.lower_endpoint, 
            X.upper_endpoint
            ) 
        >> arrange(
            X.trait, 
            X.environment, 
            X.run_length, 
            X.source, 
            X.time
            )) 
    sorted_ACH_trajectory_dataframe_csv_name = 'ACH_trajectory_dataframe.csv'
    ACH_dataframe_location =  (
        output_folder 
        + '/' 
        + sorted_ACH_trajectory_dataframe_csv_name
        )
    sorted_ACH_trajectory_dataframe.to_csv(ACH_dataframe_location)

    date_time_year = asctime(localtime(t_time())) 

    print (
            '\n\n'
            'Date, time, and year: %s \n' 
            'Module: %s \n'
            'Saved dataframe: %s \n'  
            'Saved dataframe: %s'  
            % (
                date_time_year, 
                module_path,
                analysis_dataframe_location,
                ACH_dataframe_location
                ))

