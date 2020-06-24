#--------------------------------------------------------------
#Python file for the generation of the configuration.ini file
#--------------------------------------------------------------

from configparser import ConfigParser

config = ConfigParser()

config['General_Variables'] = {    
    'number_of_layers' : '51',
    'top_of_Atmopshere' : '50',
    'scale_height_gas_1' : '5',
    'scale_height_gas_2' : '5',
    'wp_profile_gas_1' : '2',
    'wp_profile_gas_2' : '1',
    'presence_of_ozone' : '1',
    'abs_coefficient_gas_1' : '0.7',
    'abs_coefficient_gas_2' : '0.0002',
    'abs_coefficient_ozone' : '0.000005'}

config['Clouds_Variables'] = {    
    'presence_of_clouds' : '1',
    'cloud_bottom' : '8',
    'cloud_top' : '10',
    'cloud_IR_abs_coeff' : '0.0001',
    'cloud_SW_abs_coeff' : '0.0001'}

config['Output_Path'] = {
    'output_path_graph' : './OUTPUT/'}

with open('./Atmosphere_T_Configuration.ini','w') as file:
    config.write(file)