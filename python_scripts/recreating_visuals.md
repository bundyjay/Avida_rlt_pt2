## Recreating the visuals from the manuscript

<p>Overview</p>

<p>
Most figures require running three scripts to recreate. The first is a script that creates the data dictionary. These scripts have "data_dict" in the title and are found in the operations folder. These folders read the raw data output by Avida and creates Python dictionaries that store the raw data from each run. The second script creates a sorted dataframe and also outputs a .csv file so the data can be reviewed. These scripts have "create_csv" in the title and are found in the operations folder. Note that each of these "create_csv" scripts has an associated "sort_csv" script that is imported to create custom sorting for each dataframe. The third script creates plots and tables. These files have unique names and are found in the analysis folder in the scripts directory.
</p>

<p>
To run a script, ensure that you are in the same directory as the script (e.g., cd operations). Then execute the script (e.g, python3 phase1.py) If you have already executed the script to create the csv for a plot (to generate a plot or table that uses the same data) then you only need to run the analysis file script. 
</p>

<p>Figs 1-3</p>

<p>
Figures 1-3 are schematics that were created in Inkscape. There are no scripts to recreate them.
</p>

<p>Fig 4</p>

<p>
data dict file: data_dict_phase1.py<br/>
create csv file: create_csv_phase1.py<br/>
analysis file: phase1.py<br/>
</p>

<p>Fig 5</p>

<p>
data dict file: data_dict_phase1_average_tasks_data.py <br/>
create csv file: create_csv_phase1_average_tasks_data.py <br/>
analysis file: facet_phase1_average_tasks_plot.py <br/>
</p>

<p>Fig 6</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_byenvironment_shallow_overlapping.py <br/>
</p>

<p>Fig 7</p>

<p>
data dict file: data_dict_phase2.py <br>
create csv file: create_csv_phase2.py, ANOVA_variance_components.py (analysis folder) <br/>
analysis file:  combined_ACH_estimates_shallow_overlapping_w_traj.py <br/>
</p>

<p>Fig 8</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py, ANOVA_variance_components.py (analysis folder) <br/>
analysis file:  combined_ACH_estimates_shallow_orthogonal_w_traj.py <br/>
</p>

<p>Fig 9</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py, ANOVA_variance_components.py (analysis folder) <br/>
analysis file:  combined_footprint_ACH_estimates_genome_length_w_traj.py <br/>
</p>

<p>Fig 10</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py, ANOVA_variance_components.py (analysis folder) <br/>
analysis file:  combined_footprint_ACH_fitness_w_traj.py <br/>
</p>

<p>S1 Table</p>

<p>
data dict file: data_dict_phase1_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase1_average_fitness_and_average_length.py <br/>
analysis file: phase1_average_fitness_and_average_length_analysis.py <br/>
</p>

<p>S2 Table</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_average_fitness_and_average_length_analysis.py <br/>
</p>

<p>S3 Table</p>

<p>
data dict file: data_dict_phase1_average_gestation_and_average_length.py <br/>
create csv file: create_csv_phase1_average_gestation_and_average_length.py <br/>
analysis file: phase1_average_gestation_analysis.py <br/>
</p>

<p>S4 Table</p>

<p>
data dict file: data_dict_phase2_average_gestation_and_average_length.py <br/>
create csv file: create_csv_phase2_average_gestation_and_average_length.py <br/>
analysis file: phase2_average_gestation_analysis.py <br/>
</p>

<p>S1 Fig</p>

<p>
data dict file: data_dict_phase1_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase1_average_fitness_and_average_length.py <br/>
analysis file: phase1_average_fitness_and_average_length_boxplots.py <br/>
</p>

<p>S2 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_shallow_boxplots.py <br/>
</p>

<p>S3 Fig</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_byenvironment_shallow_orthogonal.py <br/>
</p>

<p>S4 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_shallow_boxplots.py <br/>
</p>

<p>S5 Fig</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_bytrait_intermediate_fitness.py <br/>
</p>

<p>S6 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_intermediate_and_deep_boxplots.py <br/>
</p>

<p>S7 Fig</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_bytrait_intermediate_genome_length.py <br/>
</p>

<p>S8 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_intermediate_and_deep_boxplots.py <br/>
</p>

<p>S9 Fig</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_bytrait_deep_fitness.py <br/>
</p>

<p>S10 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_intermediate_and_deep_boxplots.py <br/>
</p>

<p>S11 Fig</p>

<p>
data dict file: data_dict_phase2.py <br/>
create csv file: create_csv_phase2.py <br/>
analysis file:  phase2_bytrait_deep_genome_length.py <br/>
</p>

<p>S12 Fig</p>

<p>
data dict file: data_dict_phase2_average_fitness_and_average_length.py <br/>
create csv file: create_csv_phase2_average_fitness_and_average_length.py <br/>
analysis file: phase2_intermediate_and_deep_boxplots.py <br/>
</p>

<p>S13 Fig</p>

<p>
data dict file: data_dict_phase2_average_tasks_data.py <br/>
create csv file: create_csv_phase2_average_tasks_data.py <br/>
analysis file: facet_phase2_average_tasks_plot.py <br/>
</p>

