#----------------------------------------
#ATMOSPHERE_TEMPERATURE_PROFILE
#----------------------------------------

import numpy as np


#Definition of the variables

nlayer = 23 #Number of total layer used for the plane-parallel approximation
                #The first layer is the surface
z_top_a = 50 #Height of the atmosphere in kilometers
scale_height_1 = 5 #Scale height of the first absorber gas
scale_height_2 = 5 #Scale height of the second absorber gas
wp_1 = 1 #Mixing ratio flag for gas one. 1 = constant, other = exponential
wp_2 = 1 #Mixing ratio flag for gas two. 1 = constant, other = exponential
ozone = 1 #Flag for the stratospheric ozone
N_gas_1 = 1 #Normalisation factor for the gas one
N_gas_2 = 1 #Normalisation factor for the gas two
N_gas_ozone = 1 #Normalisation factor for the ozone
k_1_a = 0.33 #absorption coefficient for the gas one (IR)
k_2_a = 0 #absorption coefficient for the gas two (SW)
k_ozone_a = 0 #absorption coefficient for the ozone (SW)
clouds = 0 #flag to consider the presence of the clouds
cloud_position = [8, 10] #bottom and top height in kilometer
k_cloud_LW = 0 #Absorption coefficient for the clouds in the long-wave
k_cloud_SW = 0 #Absorption coefficient for the clouds in the short-wave

#Definition of the fixed value

albedo = 0.3                 #Planetary albedo
TSI = (1 - albedo) * 1370/4  #Total solar irradiance at the atmosphere top
mudif = 3/5                  # Clouds diffuse trasmittance
sigma = 5.6704e-8            # [W/(m^2k^4)] Stefan Boltzmann Costant
z_top_a = z_top_a*1000       # conversion Km to m of the atmosphere high
scale_height_1 = scale_height_1*1000                   
scale_height_2 = scale_height_2*1000      