from cmath import nan
import lasio
import pathlib 
from numpy.core.fromnumeric import mean
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns    
import plotly.express as px
from fpdf import FPDF
from tempfile import NamedTemporaryFile
import tempfile
import streamlit.components.v1 as components
import striplog
from striplog import Legend, Lexicon, Interval, Component, Decor
import missingno as ms
import lascheck
import traceback
from PIL import Image
from blinker import Signal

    
# Function to set interval transit values in μsec/m
def unit_meter():
    global dt_matrix_sandstone
    global dt_matrix_limestone
    global dt_matrix_dolomite
    global dt_fluid_seawater
    global dt_fluid_freshwater
    global correction_oil
    global correction_gas
    
    dt_matrix_sandstone = 55.5 * 12 * 2.54 * 0.01
    dt_matrix_limestone = 47.5 * 12 * 2.54 * 0.01
    dt_matrix_dolomite = 43.5 * 12 * 2.54 * 0.01
    dt_fluid_seawater = 189 * 12 * 2.54 * 0.01
    dt_fluid_freshwater = 204 * 12 * 2.54 * 0.01
    correction_oil = 0.9
    correction_gas = 0.7

# Function to set interval transit values in μsec/ft
def unit_feet():
    global dt_matrix_sandstone
    global dt_matrix_limestone
    global dt_matrix_dolomite
    global dt_fluid_seawater
    global dt_fluid_freshwater
    global correction_oil
    global correction_gas
    
    dt_matrix_sandstone = 55.5
    dt_matrix_limestone = 47.5
    dt_matrix_dolomite = 43.5
    dt_fluid_seawater = 189
    dt_fluid_freshwater = 204
    correction_oil = 0.9
    correction_gas = 0.7

# Set the dashboard layout to wide mode
st.set_page_config(page_title="Sonic Log Interpreter")

# Create tabs for this dashboard
tab1, tab2, tab3, tab4 = st.tabs(["HOME", "USER'S GUIDE", "INTERPRETATION", "ABOUT"])
with tab1:
    st.title('''Sonic Log Interpretation: Porosity Derivation''')
    st.markdown("Welcome!")
    st.markdown('This application handles large data file called LAS file. \nThe purpose of this application is to visualize and interpret the given data ')
    st.markdown('This was created by Engr. Gabriel Malasique, Engr. Ezekiel Guillo and Engr. Kurt Joshua Lior Diones ')

with tab2:
    st.subheader('Willie Time Average Formula')


# Display the image in Streamlit
    img_wyllie = Image.open(r"C:\Users\Malasique\Documents\GitHub\Sonic-Log-Interpreter-Web-Application\Sonic_Formula.png")
    img_wyllie = img_wyllie.resize([int(img_wyllie.width/3), int(img_wyllie.height/3.5)])
    st.image(img_wyllie)
    
    
    st.markdown('''The Wyllie time average method is used for estimating porosity from sonic measurements. It requires the following input parameters:
             \nϕs = Sonic Porosity
             \nΔtl = Sonic log interval transit time. Typically, its unit is μsec/ft
             \nΔtp = Pore fluid interval transit time.
             \nΔtma = Rock matrix interval transit time    
                 ''')
    
    img_transit = Image.open(r"C:\Users\Malasique\Documents\GitHub\Sonic-Log-Interpreter-Web-Application\Transit_Time.png")
    img_transit = img_transit.resize([int(img_transit.width/3), int(img_transit.height/3.5)])
    st.image(img_transit, caption= 'Typical interval transit time for lithologies and fluids')
    st.divider()
    
    
    
    st.subheader('Uncompacted Formation and Hydrocarbon-bearing Zone')
    st.markdown('''The existing equation tends to produce higher porosity estimates when applied to uncompacted sandstones and hydrocarbon-bearing reservoirs. 
            To mitigate this issue, we can introduce empirical corrections using two terms: the compaction factor (Cp) and the hydrocarbon correction (Hy).
             \nCp quantifies the impact of pore pressure on the sonic porosity equation. Typically, it is determined through a comparison of density and apparent sonic porosity or by analyzing the sonic response in nearby shale (Cp = Δtsh/100.0).
             \nHy, on the other hand, is an approximate correction factor and is assigned a value of 0.9 for oil and 0.7 for gas reservoirs.
             \nWith these adjustments, the revised Wyllie time average equation is as follows:''')
    img_compaction = Image.open(r"C:\Users\Malasique\Documents\GitHub\Sonic-Log-Interpreter-Web-Application\Correction.png")
    img_compaction = img_compaction.resize([int(img_compaction.width/3), int(img_compaction.height/3.5)])
    st.image(img_compaction)
    st.markdown('''Cp = Compaction correction factor
            \nHy = Hydrocarbon correction factor  ''')
    st.divider()
    
    
    
    track_subheader = 'Abbreviation of tracks'
    st.subheader(track_subheader)
    
    st.markdown = ('''Certainly, here's a list of common log curve abbreviations (mnemonics) and their corresponding names or descriptions:
                   \nDEPTH: Depth
                   \nGR: Gamma Ray
                   \nSP: Spontaneous Potential
                   \nCALI: Caliper
                   \nRHOB: Bulk Density
                   \nNPHI: Neutron Porosity
                   \nILD: Deep Resistivity
                   \nDT: Sonic Transit Time
                   \nGRS: Spectral Gamma Ray
                   \nPEF: Photoelectric Factor
                   \nMSFL: MicroSpherically Focused Log
                   \nLLD: Laterolog Deep
                   \nLSS: Laterolog Shallow
                   \nDPHI: Density Porosity
                   \nPE: Porosity Estimate
                   \nRES: Formation Resistivity
                   \nCALD: Dual Caliper
                   \nGRD: Gamma Ray Depth
                   \nTVD: True Vertical Depth
                   \nDELT: Differential Travel Time
                   \nDTS: Delta-T Shear
                   \nDTC: Delta-T Compressional
                   \nGR_EDTC: Enhanced Spectral Gamma Ray
                   \nGR_EDTH: Enhanced Spectral Gamma Ray
                   \nRDEP: Deep Resistivity
                   \nRMED: Medium Resistivity
                   \nRLL3: Laterolog Three
                   \nRESS: Shallow Resistivity
                   \nRXO: Rxo
                   \nCNL: CNL
                   \nRLA3: Laterolog Array Three
                   \nTENS: Tensile Strength
                   \nPOTA: Potassium
                   \nURAN: Uranium
                   \nTHOR: Thorium
                   \nTOC: Total Organic Carbon
                   \nCO2: Carbon Dioxide
                   \nH2S: Hydrogen Sulfide
                   \nTEMP: Temperature
                   \nCBL: Cement Bond Log
                   ''')
    st.markdown = ('''These are common mnemonics and names for log curves that you may encounter in well logging data. Please note that the availability of these curves and their names can vary depending on the specific well logging tools and data acquisition methods used during the logging operation. Always refer to the specific LAS file's "Curve Information" section or documentation to determine the mnemonics and descriptions of the log curves recorded in that file.''')
    st.divider()
    
    manual_subheader = 'Manual process of using the program'
    st.subheader(manual_subheader)

with tab3:
    st.set_option('deprecation.showfileUploaderEncoding', False)
    
    mode = st.radio(
        "**Select an option:**",
        ('Upload LAS file', 'Use sample LAS file')
    )
    st.divider()
    
    if mode == 'Upload LAS file':
        file = st.file_uploader('Upload the LAS file')
        if file is not None:
          tfile = tempfile.NamedTemporaryFile(delete=False)
          tfile.write(file.read())
          las_file = lasio.read(tfile.name)
          las_df=las_file.df()
          
    
    if mode == 'Use sample LAS file':
        file = r"C:\Users\Malasique\Downloads\Thesis\05.PETROPHYSICAL INTERPRETATION-20230725T073453Z-001\05.PETROPHYSICAL INTERPRETATION\15_9-F-1\WLC_PETRO_COMPUTED_INPUT_1.LAS"
        las_file = lasio.read(file)
        las_df = las_file.df()
          
    
    if file:
      las_df.insert(0, 'DEPTH', las_df.index)
      las_df.reset_index(drop=True, inplace=True)   
    
      try:
        well_name =  las_file.header['Well'].WELL.value
        start_depth = las_df['DEPTH'].min()
        stop_depth = las_df['DEPTH'].max()
        step = abs(las_file.header['Well'].STEP.value)
        company_name =  las_file.header['Well'].COMP.value
        date =  las_file.header['Well'].DATE.value
        curvename = las_file.curves
      except:
        well_name =  'unknown'
        start_depth = 0.00
        stop_depth = 10000.00
        step = abs(las_df['DEPTH'][1]-las_df['DEPTH'][0])
        company_name =  'unknown'
        date =  'unknown'
        curvename = las_file.curves
    
    if file:
      st.sidebar.subheader('Sections:')
      lascheck_mode = st.sidebar.checkbox("LAS file Specification")
      well_info_mode = st.sidebar.checkbox("Well Information")
      curve_info_mode = st.sidebar.checkbox("Curve Information")
      curve_data_mode = st.sidebar.checkbox("Curve Data Overview")
      visualization_log_mode = st.sidebar.checkbox("Log Visualization")
    
      if lascheck_mode:
        st.subheader("LAS File Conformity Check Result:")
    
        try:
                las = lascheck.read(file)
                las.check_conformity()
                las.get_non_conformities()
                st.write(las.check_conformity())
                st.write(las.get_non_conformities())
                
        except:
                # Handle the error gracefully
                st.error("LAS file doesn't meet the specifications. Error might occur.")
                # Capture and display the traceback
                st.write("Traceback:")
                st.code(traceback.format_exc())
        st.divider()
        
      if well_info_mode:
        st.subheader('Well Information')
        st.markdown(f'Well Name : {well_name}')
        st.markdown(f'Start Depth : {start_depth}')
        st.markdown(f'Stop Depth : {stop_depth}')
        st.markdown(f'Step : {step}')
        st.markdown(f'Company : {company_name}')
        st.markdown(f'Logging Date : {date}')
        st.divider()
    
      if curve_info_mode:
        st.subheader('Curve Information')
        st.markdown(f'================================================\n{curvename}')
        st.divider()
      
      if curve_data_mode:
        st.subheader('Curve Data Overview')
        st.markdown('The value on the left figure is number of rows. White space in each column of curve is a missing value rows/data. Expand to see more details')
        st.pyplot(ms.matrix(las_df, sparkline=False, labels=100).figure)
        st.divider()
    
      selected_column = st.sidebar.selectbox("**Select curve data to visualize:**", las_df.keys())
    
    # Check if 'DEPTH' is a valid curve in the LAS file
      if 'DEPTH' in las_file.keys():
          # Get the unit of the 'DEPTH' curve
          unit_curve = las_file.curves[selected_column].unit
          st.sidebar.write(f"Unit of {selected_column} curve: {unit_curve}")
      else:
          st.sidebar.write("'DEPTH' curve not found in the LAS file.")
    
    
        
    # Determine which unit to use based on unit_curve
      if unit_curve == 'us/m':
          unit_meter()
      elif unit_curve == 'us/ft': 
          unit_feet()
      else:
          st.warning('**Warning**: Unit must be either (us/m) or (us/ft). Assuming the unit of selected curve data is us/ft')
          unit_feet()
    
      st.sidebar.subheader('Sonic Porosity:')
      if file:
          mode_sandstone_seawater = st.sidebar.checkbox("Matrix: Sandstone | Fluid: Seawater")
          mode_limestone_seawater = st.sidebar.checkbox("Matrix: Limestone | Fluid: Seawater")
          mode_dolomite_seawater = st.sidebar.checkbox("Matrix: Dolomite | Fluid: Seawater")
          mode_sandstone_freshwater = st.sidebar.checkbox("Matrix: Sandstone | Fluid: Freshwater") 
          mode_limestone_freshwater = st.sidebar.checkbox("Matrix: Limestone | Fluid: Freshwater")
          mode_dolomite_freshwater = st.sidebar.checkbox("Matrix: Dolomite | Fluid: Freshwater")
    
      mode = st.sidebar.radio(
          "Hydrocarbon Correction:",
          ('None', 'Oil Correction', 'Gas Correction'))
        
      # Check if 'DT' is a valid curve in the LAS file
      data = []
      if selected_column in las_file.keys():
          for depth, dt_log in zip(las_df['DEPTH'], las_df[selected_column]):
              # Always include depth and Sonic Log Reading
              row_data = {"Depth": depth, 'Sonic Log Reading': dt_log}
              if mode == 'None':
                
                  if mode_sandstone_seawater:
                      phi_sandstone_seawater = (dt_log - dt_matrix_sandstone) / (dt_fluid_seawater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Seawater'] = phi_sandstone_seawater
                
                  if mode_limestone_seawater:
                      phi_limestone_seawater = (dt_log - dt_matrix_limestone) / (dt_fluid_seawater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Seawater'] = phi_limestone_seawater
                
                  if mode_dolomite_seawater:
                      phi_dolomite_seawater = (dt_log - dt_matrix_dolomite) / (dt_fluid_seawater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Seawater'] = phi_dolomite_seawater
                
                  if mode_sandstone_freshwater:
                      phi_sandstone_freshwater = (dt_log - dt_matrix_sandstone) / (dt_fluid_freshwater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Freshwater'] = phi_sandstone_freshwater
                
                  if mode_limestone_freshwater:
                      phi_limestone_freshwater = (dt_log - dt_matrix_limestone) / (dt_fluid_freshwater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Freshwater'] = phi_limestone_freshwater
                
                  if mode_dolomite_freshwater:
                      phi_dolomite_freshwater = (dt_log - dt_matrix_dolomite) / (dt_fluid_freshwater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Freshwater'] = phi_dolomite_freshwater
                    
                  # Add similar conditions for other checkboxes (e.g., mode_limestone_freshwater, mode_dolomite_freshwater, etc.)  
                  data.append(row_data)      
            
              if mode == 'Oil Correction':
                
                  if mode_sandstone_seawater:
                      phi_sandstone_seawater = (dt_log - dt_matrix_sandstone) / (dt_fluid_seawater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Seawater'] = phi_sandstone_seawater * correction_oil
                
                  if mode_limestone_seawater:
                      phi_limestone_seawater = (dt_log - dt_matrix_limestone) / (dt_fluid_seawater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Seawater'] = phi_limestone_seawater * correction_oil
                
                  if mode_dolomite_seawater:
                      phi_dolomite_seawater = (dt_log - dt_matrix_dolomite) / (dt_fluid_seawater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Seawater'] = phi_dolomite_seawater * correction_oil
                
                  if mode_sandstone_freshwater:
                      phi_sandstone_freshwater = (dt_log - dt_matrix_sandstone) / (dt_fluid_freshwater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Freshwater'] = phi_sandstone_freshwater * correction_oil
                
                  if mode_limestone_freshwater:
                      phi_limestone_freshwater = (dt_log - dt_matrix_limestone) / (dt_fluid_freshwater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Freshwater'] = phi_limestone_freshwater * correction_oil
                
                  if mode_dolomite_freshwater:
                      phi_dolomite_freshwater = (dt_log - dt_matrix_dolomite) / (dt_fluid_freshwater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Freshwater'] = phi_dolomite_freshwater * correction_oil
                    
                  # Add similar conditions for other checkboxes (e.g., mode_limestone_freshwater, mode_dolomite_freshwater, etc.)
                  data.append(row_data)
            
              if mode == 'Gas Correction':
                  
                  if mode_sandstone_seawater:
                      phi_sandstone_seawater = (dt_log - dt_matrix_sandstone) / (dt_fluid_seawater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Seawater'] = phi_sandstone_seawater * correction_gas
                
                  if mode_limestone_seawater:
                      phi_limestone_seawater = (dt_log - dt_matrix_limestone) / (dt_fluid_seawater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Seawater'] = phi_limestone_seawater * correction_gas
                
                  if mode_dolomite_seawater:
                      phi_dolomite_seawater = (dt_log - dt_matrix_dolomite) / (dt_fluid_seawater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Seawater'] = phi_dolomite_seawater * correction_gas
                
                  if mode_sandstone_freshwater:
                      phi_sandstone_freshwater = (dt_log - dt_matrix_sandstone) / (dt_fluid_freshwater - dt_matrix_sandstone)
                      row_data['Sonic_Sandstone_Freshwater'] = phi_sandstone_freshwater * correction_gas
                
                  if mode_limestone_freshwater:
                      phi_limestone_freshwater = (dt_log - dt_matrix_limestone) / (dt_fluid_freshwater - dt_matrix_limestone)
                      row_data['Sonic_Limestone_Freshwater'] = phi_limestone_freshwater * correction_gas
                
                  if mode_dolomite_freshwater:
                      phi_dolomite_freshwater = (dt_log - dt_matrix_dolomite) / (dt_fluid_freshwater - dt_matrix_dolomite)
                      row_data['Sonic_Dolomite_Freshwater'] = phi_dolomite_freshwater * correction_gas
                    
                  # Add similar conditions for other checkboxes (e.g., mode_limestone_freshwater, mode_dolomite_freshwater, etc.)
                  data.append(row_data)
                
    # Create the DataFrame with appropriate columns
      las_df_revised = pd.DataFrame(data)
    
    # Display the DataFrame as a presentable Excel-like table
      st.subheader('Data Sets:')
      st.dataframe(las_df_revised)
    
      if visualization_log_mode:    
        # Default values for visualization
        plot_h = 27
        plot_w = 22
        title_size = 12
        title_height = 1.0
        line_width = 1
        dt_color = 'black'
        trackname_1 = f'Sonic Log\n{unit_curve}'
        trackname_2 = 'Sonic Porosity\np.u.'
        trackname_3 = 'Result\np.u.'
    
        # Sidebar for user input
        st.sidebar.header("Depth Selection")
        top_depth = st.sidebar.number_input('Top Depth', min_value=0.00, value=start_depth, step=100.00, key="top_depth")
        bot_depth = st.sidebar.number_input('Bottom Depth', min_value=0.00, value=stop_depth, step=100.00, key="bot_depth")
    
        st.sidebar.header("Scale Setting (Track 1)")
        dt_left = st.sidebar.number_input('Left Scale', min_value=0.00, max_value=1000.00, value=140.00, step=5.0, key="dt_left")
        dt_right = st.sidebar.number_input('Right Scale', min_value=0.00, max_value=1000.00, value=40.00, step=5.0, key="dt_right")
        grid_num_1 = st.sidebar.number_input('Number of Grids', min_value=0, value=10, step=1, key="grid_num_1")
    
        st.sidebar.header("Scale Setting (Track 2)")
        phis_left = st.sidebar.number_input('Left Scale', min_value=-0.151, max_value=1.051, value=0.5, step=0.05, key="phis_left")
        phis_right = st.sidebar.number_input('Right Scale', min_value=-0.151, max_value=1.051, value=-0.15, step=0.05, key="phis_right")
        grid_num_2 = st.sidebar.number_input('Number of Grids', min_value=0, value=10, step=1, key="grid_num_2")
    
        st.sidebar.header("Scale Setting (Track 3)")
        result_left = st.sidebar.number_input('Left Scale', min_value=-0.151, max_value=1.51, value=1.15, step=0.05, key="result_left")
        result_right = st.sidebar.number_input('Right Scale', min_value=-0.151, max_value=1.51, value=-0.15, step=0.05, key="result_right")
        grid_num_3 = st.sidebar.number_input('Number of Grids', min_value=0, value=10, step=1, key="grid_num_3")    
        
        # Create a subplot with 1 row and 3 columns
        fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(plot_w, plot_h), sharey=True)
    
        # =============================================================================
        # Subplot 1
        ax1 = plt.subplot2grid((1, 3), (0, 0), rowspan=1, colspan=1)
    
        # Sonic Log Reading track
        ax1.plot(las_df_revised['Sonic Log Reading'], las_df_revised['Depth'], color=dt_color, lw=line_width)
        ax1.set_xlabel(trackname_1)
        ax1.set_xlim(dt_left, dt_right)
        ax1.set_ylim(bot_depth, top_depth)
        ax1.xaxis.label.set_color(dt_color)
        ax1.tick_params(axis='x', colors=dt_color)
        ax1.spines["top"].set_edgecolor(dt_color)
        ax1.spines["top"].set_position(("axes", 1.02))
    
        # Calculate the middle value
        dt_middle = (dt_left + dt_right) / 2
    
        # Calculate the grid interval
        grid_interval = (dt_right - dt_left) / (grid_num_1 - 1)
    
        # Generate the list of x-axis tick positions
        xtick_positions = [dt_left, dt_middle, dt_right]
    
        # Generate the list of grid positions
        grid_positions = np.linspace(dt_left, dt_right, num=grid_num_1)
    
        # Set the x-axis ticks and labels
        ax1.set_xticks(xtick_positions)
        ax1.set_xticklabels([str(x) for x in xtick_positions])
    
        # Set the grid lines
        ax1.set_xticks(grid_positions, minor=True)
        ax1.grid(which='minor', linestyle='--', linewidth=0.5)
    
        # Major and minor grid lines
        ax1.grid(which='major', color='silver', linestyle='-')
        ax1.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax1.xaxis.set_ticks_position("top")
        ax1.xaxis.set_label_position("top")
    
        # =============================================================================
        # Subplot 2
        ax2 = plt.subplot2grid((1, 3), (0, 1), rowspan=1, colspan=1)
    
        # Select all columns in las_df_revised except "Depth" and "Sonic Log Reading"
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
    
    
        # Plot the selected columns against 'Depth'
        for column in columns_to_plot:
            ax2.plot(las_df_revised[column], las_df_revised['Depth'], label=column)
    
        ax2.set_xlabel(trackname_2)
        ax2.set_xlim(phis_left, phis_right)
        ax2.set_ylim(bot_depth, top_depth)
        ax2.xaxis.label.set_color(dt_color)
        ax2.tick_params(axis='x', colors=dt_color)
        ax2.spines["top"].set_edgecolor(dt_color)
        ax2.spines["top"].set_position(("axes", 1.02))
    
        # Calculate the middle value
        phis_middle = (phis_left + phis_right) / 2
    
        # Calculate the grid interval
        grid_interval = (phis_right - phis_left) / (grid_num_2 - 1)
    
        # Generate the list of x-axis tick positions
        xtick_positions = [phis_left, phis_middle, phis_right]
    
        # Generate the list of grid positions
        grid_positions = np.linspace(phis_left, phis_right, num=grid_num_2)
    
        # Set the x-axis ticks and labels
        ax2.set_xticks(xtick_positions)
        ax2.set_xticklabels([str(x) for x in xtick_positions])
    
        # Set the grid lines
        ax2.set_xticks(grid_positions, minor=True)
        ax2.grid(which='minor', linestyle='--', linewidth=0.5)
    
        # Major and minor grid lines
        ax2.grid(which='major', color='silver', linestyle='-')
        ax2.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax2.xaxis.set_ticks_position("top")
        ax2.xaxis.set_label_position("top")
    
        # Add a legend to distinguish different columns
        ax2.legend()
    
    
        # Subplot 3
        ax3 = plt.subplot2grid((1, 3), (0, 2), rowspan=1, colspan=1)
    
        # Select all columns in las_df_revised except "Depth" and "Sonic Log Reading"
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
    
        # Create an empty list to store the maximum values
        max_values = []
    
        # Iterate over the rows in the DataFrame
        for index, row in las_df_revised.iterrows():
            # Initialize the maximum value as negative infinity
            max_value = float('-inf')
            
            # Iterate over the columns you want to compare
            for column in columns_to_plot:
                # Get the value from the current column
                value = row[column]
                
                # Update the maximum value if the current value is greater
                if value > max_value:
                    max_value = value
            
            # Append the maximum value to the list
            max_values.append(max_value)
    
        # Add the 'Max Value' column to the DataFrame and rename it
        max_values_df = pd.DataFrame(max_values, columns=["Max Value"])
    
        # Now you can use 'Max Value' in the plot
        ax3.plot(max_values_df['Max Value'], las_df_revised['Depth'], label="Max Value", color=dt_color)
    
            ##area-fill sand and shale for VSH
        ax3.fill_betweenx(las_df_revised['Depth'], -0.15, 0, interpolate=False, color = 'orange', linewidth=0, alpha=0.5, hatch = '=-')
        ax3.fill_betweenx(las_df_revised['Depth'], 0, 0.467, interpolate=False, color = 'green', linewidth=0, alpha=0.5, hatch = 'b')
        ax3.fill_betweenx(las_df_revised['Depth'], 0.467, 1, interpolate=False, color = 'gold', linewidth=0, alpha=0.5, hatch = 'o')
        ax3.fill_betweenx(las_df_revised['Depth'], 1, 1.51, interpolate=False, color = 'red', linewidth=0, alpha=0.5, hatch = 'x')
    
    
        ax3.set_xlabel(trackname_3)
        ax3.set_xlim(result_left, result_right)
        ax3.set_ylim(bot_depth, top_depth)
        ax3.xaxis.label.set_color(dt_color)
        ax3.tick_params(axis='x', colors=dt_color)
        ax3.spines["top"].set_edgecolor(dt_color)
        ax3.spines["top"].set_position(("axes", 1.02))
    
        # Calculate the middle value
        result_middle = (result_left + result_right) / 2
    
        # Calculate the grid interval
        grid_interval = (result_right - result_left) / (grid_num_3 - 1)
    
        # Generate the list of x-axis tick positions
        xtick_positions = [result_left, result_middle, result_right]
    
        # Generate the list of grid positions
        grid_positions = np.linspace(result_left, result_right, num=grid_num_3)
    
        # Set the x-axis ticks and labels
        ax3.set_xticks(xtick_positions)
        ax3.set_xticklabels([str(x) for x in xtick_positions])
    
        # Set the grid lines
        ax3.set_xticks(grid_positions, minor=True)
        ax3.grid(which='minor', linestyle='--', linewidth=0.5)
    
        # Major and minor grid lines
        ax3.grid(which='major', color='silver', linestyle='-')
        ax3.grid(which='minor', color='lightgrey', linestyle=':', axis='y')
        ax3.xaxis.set_ticks_position("top")
        ax3.xaxis.set_label_position("top")
        
        # Show the plot in Streamlit
        st.subheader('Log Visualization')
        st.pyplot(fig)
        
        #Legend for Result
        st.caption('''
                 Corresponding porosity value for each color:
                 \nGreen = 0% to 47.6%,
                 \nYellow = 47.6% to 100%,
                 \nOrange = less than 0%,
                 \nRed = More than 100%
                     ''')
        
        st.subheader('Depth vs Sonic Porosity')
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
    
        # Create a figure and axis object
        fig2, ax = plt.subplots()
    
        # Plot the selected columns against 'Depth' in a line graph
        for column in columns_to_plot:
            ax.plot(las_df_revised['Depth'], las_df_revised[column], label=column)
    
        # Set labels and title
        ax.set_xlabel('Depth')
        ax.set_ylabel('Sonic Porosity')  # You can customize the label as needed
        ax.set_title('')
    
        # Add a legend
        ax.legend()
    
        # Show the plot
        st.pyplot(fig2)
    
    
        st.subheader('Sonic Log Reading vs Sonic Porosity')
        columns_to_plot = [col for col in las_df_revised.columns if col not in ["Depth", "Sonic Log Reading"]]
    
        # Create a figure and axis object
        fig3, ax = plt.subplots()
    
        # Plot the selected columns against 'Depth' in a line graph
        for column in columns_to_plot:
            ax.plot(las_df_revised['Sonic Log Reading'], las_df_revised[column], label=column)
    
        # Set labels and title
        ax.set_xlabel('Sonic Log Reading')
        ax.set_ylabel('Sonic Porosity')  # You can customize the label as needed
        ax.set_title('')
    
        # Add a legend
        ax.legend()
    
        # Show the plot
        st.pyplot(fig3)
        
        formeval_mode = st.sidebar.checkbox("Formation Evaluation")
        need_calibration = False
        have_anomaly = False
        need_correction = False
        no_error = False
    
        def result_calibration():
            st.markdown('''**Negative porosity value. Porosity should range between 0 to 1.**
                        \nPossible reason:
                        \n
                        \n
                            ''')
    
        def result_anomaly():
            st.markdown('''**More than 1 porosity value. Reading anomalies detected.**
                        \nPossible reason:
                        \n
                        \n
                        ''')
    
        def result_correction():
            st.markdown('''**Overestimate porosity value. Correction should be applied.**
                        \nPossible reason:
                        \n
                        \n
                        ''')
    
        def result_good():
            st.markdown('''**Normal sonic porosity reading.**''')
    
    
        if formeval_mode:
          st.subheader('Findings:')
        
          for max_value in max_values_df['Max Value']:
              if max_value < 0 and not need_calibration:
                  need_calibration = True
                  result_calibration()
              elif max_value > 1 and not have_anomaly:
                  have_anomaly = True
                  result_anomaly()
              elif 0.467 < max_value < 1 and not need_correction:
                  need_correction = True
                  result_correction()
              elif 0 < max_value < 0.467 and not need_calibration and not have_anomaly and not need_correction and not no_error:
                  no_error = True
                  result_good()
                  
          st.subheader('Recommendations:')
          if need_calibration == True:
            st.markdown('The log should be calibrated by changing the interval transit time of the matrix.')
          if have_anomaly == True:
            st.markdown('May anomaly reading. Ano gagawin mo?')
          if need_correction == True:
            st.markdown('Need ng correction sa values. Ano gagawin mo?')
          if no_error == True:
            st.markdown('Congrats! Walang mali')

