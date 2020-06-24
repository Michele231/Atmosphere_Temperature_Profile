#-----------------------------------------------------------------
#Atmosphere Temperature Profile
#-----------------------------------------------------------------
#
#This program ....
#
#
#
#....
#
#
#
# Author: Michele Martinazzo
# e-mail : michele.martinazzo@studio.unibo.it
#-----------------------------------------------------------------
#
import numpy as np
import matplotlib.pyplot as plt
import Atm_T_Functions as at
from configparser import ConfigParser


# The foundamental parameters are obtained from the configuration file:
#   "Atmosphere_T_Configuration.ini"
parser = ConfigParser()
parser.read('Atmosphere_T_Configuration.ini')

#Definition of the variables
nlayer = parser.getfloat('General_Variables', 'number_of_layers',
                         fallback = 51) 
z_top_a = parser.getfloat('General_Variables', 'top_of_Atmopshere',
                          fallback = 50)
scale_height_1 = parser.getfloat('General_Variables', 'scale_height_gas_1',
                                 fallback = 5)
scale_height_2 = parser.getfloat('General_Variables', 'scale_height_gas_2',
                                 fallback = 5)
wp_1 = parser.getfloat('General_Variables', 'wp_profile_gas_1',
                       fallback = 1)
wp_2 = parser.getfloat('General_Variables', 'wp_profile_gas_2',
                       fallback = 1)
ozone = parser.getfloat('General_Variables', 'presence_of_ozone',
                        fallback = 0)
k_1_a = parser.getfloat('General_Variables', 'abs_coefficient_gas_1',
                        fallback = 0.4)
k_2_a = parser.getfloat('General_Variables', 'abs_coefficient_gas_2',
                        fallback = 0)
k_ozone_a = parser.getfloat('General_Variables', 'abs_coefficient_ozone',
                            fallback = 0)
clouds = parser.getfloat('Clouds_Variables', 'presence_of_clouds', 
                         fallback = 0)
k_cloud_LW = parser.getfloat('Clouds_Variables', 'cloud_IR_abs_coeff', 
                         fallback = 0)
k_cloud_SW = parser.getfloat('Clouds_Variables', 'cloud_SW_abs_coeff', 
                         fallback = 0)
cloud_top = parser.getfloat('Clouds_Variables', 'cloud_top', 
                         fallback = 10)
cloud_bottom = parser.getfloat('Clouds_Variables', 'cloud_bottom', 
                         fallback = 8)

cloud_position = np.array([cloud_bottom, cloud_top])

#generation of the optical depth starting from the data
ch_ir, ch_sw, z = at.optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2,
                             wp_1, wp_2, ozone, k_1_a, k_2_a, k_ozone_a, clouds,
                             cloud_position, k_cloud_LW, k_cloud_SW)

#generation of the temperature profile vector from the OD 
T = at.temperature_profile(nlayer, ch_ir, ch_sw)

print(T)

output_path = parser.get('Output_Path', 'output_path_graph',
                         fallback = './OUTPUT/')
name_figure = 'Temperature_Profile'
output_path = output_path + name_figure

def plot_temperature():
    '''This method return the temperature profile of the atmosphere as a
       function of the height                                        '''
       
    figure = plt.figure()
    plt.plot(T,z)
    plt.show()
    figure.savefig(output_path)
    
    
plot_temperature()    
    






