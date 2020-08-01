#-----------------------------------------------------------------
#Atmosphere Temperature Profile
#-----------------------------------------------------------------
#
# Atm_T_Profile is a simple model for the solution of the radiative transfert 
# problem (without scattering).
# For a given atmosphere, the model outputs are the optical depth in two
# channel (short-wave and infrared) and the temperature profile of the 
# atmosphere and the surface.
#
#
#
# Author: Michele Martinazzo
# e-mail : michele.martinazzo@studio.unibo.it
#-----------------------------------------------------------------
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
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
scale_height_1 = parser.getfloat('General_Variables', 'scale_height_gas_IR',
                                 fallback = 10)
scale_height_2 = parser.getfloat('General_Variables', 'scale_height_gas_SW',
                                 fallback = 5)
wp_1 = parser.get('General_Variables', 'wp_profile_gas_IR',
                       fallback = 'exponential')
wp_2 = parser.get('General_Variables', 'wp_profile_gas_SW',
                       fallback = 'costant')
ozone = parser.getfloat('General_Variables', 'presence_of_ozone',
                        fallback = 1)
k_1_a = parser.getfloat('General_Variables', 'abs_coefficient_gas_IR',
                        fallback = 0.8)
k_2_a = parser.getfloat('General_Variables', 'abs_coefficient_gas_SW',
                        fallback = 0.005)
k_ozone_a = parser.getfloat('General_Variables', 'abs_coefficient_ozone',
                            fallback = 0.002)
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
                             wp_1, wp_2, ozone, k_1_a, k_2_a, k_ozone_a)

#if the cloud flag is equal to one it sum the cloud's contruìibute to OD
if clouds == 1:
    ch_ir, ch_sw = at.clouds_optical_depth(ch_ir, ch_sw, z_top_a, cloud_position,
                                    k_cloud_LW, k_cloud_SW)
elif clouds == 0:
    pass
else:
    raise ValueError("clouds flag must to be 0 (off) or 1(on)!")


#generation of the temperature profile vector from the OD 
T = at.temperature_profile(ch_ir, ch_sw)

#Definition of the output Path
output_path = parser.get('Output_Path', 'output_path_graph',
                         fallback = './OUTPUT/')


def plot_temperature():
    '''This method return the temperature profile of the atmosphere as a
       function of the height                                        '''
    
    name_figure = 'Temperature_Profile'
    output_path_temperature = output_path + name_figure
        
    fig = plt.figure()
    plt.plot(T,z)
    fig.suptitle(name_figure)
    plt.ylabel('Height [m]')
    plt.xlabel('Temperature [K]')
    
    fig.savefig(output_path_temperature)
    
def plot_OD():
    '''This method return the OD profile of the atmosphere as a
       function of the height for both the short wave region and IR region                                           
                                                                          '''
    name_figure = 'OD_Profile'
    output_path_OD = output_path + name_figure
    
    fig, (ax1, ax2) = plt.subplots(1, 2, sharex='col', sharey='row')    
    ax1.plot(ch_ir,z, color='r')
    ax2.plot(ch_sw,z, color='b')
    fig.suptitle(name_figure)
    ax1.set_ylabel('Height [m]')
    ax1.set_xlabel('Optical Depth OD')
    ax1.set_title('IR OD')
    ax2.set_xlabel('Optical Depth OD')
    ax2.set_title('SW OD')
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((-2,2)) 
    ax1.xaxis.set_major_formatter(formatter)
    ax2.xaxis.set_major_formatter(formatter)
    
    fig.savefig(output_path_OD)
    
def temperature_txt():
    '''This method generates a txt file with the temperature value of the 
       atmosphere in function of the height                         
                                                                    '''
    name_file = 'Temperature_Profile'
    output_path_txt = output_path + name_file
    header_file1 = 'In this file is presented the temperature in function of the height \n'
    header_file2 = 'Height[m]  Temperature[K]'
    header_file = header_file1 + header_file2
        
    np.savetxt(f'{output_path_txt}.txt',  np.c_[z, T], fmt="%f", 
               delimiter=" ", header = header_file)
    
    
    
#If the number of layer is 1 i'm considering only the surface. 
#For this reason the plotting process is bypassed
if nlayer > 1:    
    plot_temperature()    
    plot_OD()
else:
    pass

temperature_txt()




