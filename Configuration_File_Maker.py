#--------------------------------------------------------------
#Python file for the generation of the configuration.ini file
#--------------------------------------------------------------

from configparser import ConfigParser

config = ConfigParser()

config['General_Variables'] = {    
    'number_of_layers' : '101',
    'top_of_Atmopshere' : '50',
    'scale_height_gas_IR' : '10',
    'scale_height_gas_SW' : '5',
    'wp_profile_gas_IR' : 'costant',
    'wp_profile_gas_SW' : 'costant',
    'presence_of_ozone' : '1',
    'abs_coefficient_gas_IR' : '1.2',
    'abs_coefficient_gas_SW' : '0.005',
    'abs_coefficient_ozone' : '0.002'}

config['Clouds_Variables'] = {    
    'presence_of_clouds' : '0',
    'cloud_bottom' : '8',
    'cloud_top' : '10',
    'cloud_IR_abs_coeff' : '0.0001',
    'cloud_SW_abs_coeff' : '0.0001'}

config['Output_Path'] = {
    'output_path_graph' : './OUTPUT/'}

with open('./Atmosphere_T_Configuration.ini','w') as file:
    config.write(file)