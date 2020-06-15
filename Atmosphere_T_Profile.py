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


#Definition of the function that defines the mixing ratio profile w
def mixing_ratio_profile(flag, nlayer, z, scale_height):
    if flag == 1:
        w = np.zeros(nlayer)
        w = np.full_like(w, 1)         #constant mix.ratio (example: CO2)
    else:
        w = np.exp(-z/scale_height)   #exponential mix.ratio (example: H2O)
    return w

#definition of the ozone mixing ratio profile: if flag = 1, ozone will be 
#considered in the atmosphere (The profile will be gaussian)
def ozone_mixing_ratio(flag, z, nlayer):
    if flag == 1:
        z_botton = 20000 #minimum level of stratospheric ozone
        z_top = 50000    #maximum level of stratospheric ozone
        def condition(x): return (x > z_botton) & (x < z_top)
        lay = np.where(condition(z))[0] #pos index height where there's ozone
        z0 = (z_botton + z_top)*0.5     #height maximum concentration
        sigma = (z_top - z_botton)/10   
        w_ozone = np.zeros(nlayer)
        for k in lay:
            w_ozone[k]=np.exp((-(z[k]-z0)**2)/(2*sigma**2))
    else:
        w_ozone = np.zeros(nlayer)
            
    return w_ozone

#this function returns the optical depth (OD) vectors in the long wave (ir) 
#and short wave (sw) regions.       
def optical_depth():
    
    #Definition of the absorption coefficient vectors
    #This vectors contains the value of the absorption coefficient, since the
    #physical properties don't chanmge with height the vectors are constant
    
    k1 = np.zeros(nlayer)
    k2 = np.zeros(nlayer)
    k_ozone = np.zeros(nlayer)
    k1 = np.full_like(k1,k_1_a)
    k2 = np.full_like(k2,k_2_a)
    k_ozone = np.full_like(k_ozone,k_ozone_a)
    
    #Definition of the geometry of the single layer.
    
    if nlayer==1:           #The last layer is the surface                
        z = np.array([0])
        dz = np.array([0])
        dzs = 0
    else:
        dzs = (z_top_a)/(nlayer-1)     #Layer thickness 
        dz = np.full_like(np.zeros(nlayer), dzs)  #Layer thickness Vector 
        
        #definition of the mean height level and height level vector                                            
        dz[nlayer-1]=0
        #Creations of the height vector
        z = np.zeros(nlayer)
        zm = np.zeros(nlayer)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i  
            zm[i] = z_top_a - dzs*(0.5 + i)

    #Atmospheric Density Profile Calculation
    
    do = 1.225                   #Air density at the grond [Kg/m^3]
    H = 101325/(9.8*do)          #Scale height fot the density profile
    d = do*np.exp(-z/H)          #Density profile vector
    
    
    # Mixing ratio shape gas 1 (IR)
    w1 = mixing_ratio_profile(wp_1, nlayer, z, scale_height_1)
    
    # Mixing ratio shape gas 2 (SW)
    w2 = mixing_ratio_profile(wp_2, nlayer, z, scale_height_2)
    
    #Flag for the ozone
    w_ozone = ozone_mixing_ratio(ozone, z, nlayer)

    #Absorption gasses profile vector (Density_profile*Mixing_ratio_shape)
    #This gives me the quantity of absorption gasses in that layer
    density_abs1 = d*w1
    density_abs2 = d*w2
    density_ozone = d*w_ozone
       
    #Normalisation factors of the absorption gasses profile
    
    tot_a1 = np.trapz(density_abs1, dx = dzs)
    tot_a2 = np.trapz(density_abs2, dx = dzs)
    tot_ozone = np.trapz(density_ozone, dx = dzs)
      
    if nlayer == 1:
        density_abs1 = 0          
        density_abs2 = 0
    else:           
        density_abs1 = density_abs1*N_gas_1/tot_a1         #Normalized abs 1
        density_abs2 = density_abs2*N_gas_2/tot_a2         #Normalized abs 2
    
    #check if there is enough space for the ozone
    if tot_ozone == 0:
        density_ozone = np.zeros(nlayer)
    else:
        density_ozone = density_ozone*N_gas_ozone/tot_ozone   #Normalized ozone

    #Calculation of the oprical depth
    #ch_ir = Optical depth (OD) for the IR region (gas 1) 
    #ch_abs2 = OD from the 2° absorber gas (SW)
    #ch_oz = OD for the SW region due to ozone (SW)
    
    ch_ir = np.zeros(nlayer)
    ch_abs2 = np.zeros(nlayer)
    ch_oz = np.zeros(nlayer)
    
    #The calculation of the OD profile take the mean value of the layer
    #so it has been taken the average value between the two layers
    for i in range(nlayer-1):
        ch_ir[i] = dz[i]*0.5*(k1[i]*density_abs1[i] +
                              k1[i+1]*density_abs1[i+1])/mudif
        ch_abs2[i] = dz[i]*0.5*(k2[i]*density_abs2[i] +
                              k2[i+1]*density_abs2[i+1])/mudif
        ch_oz[i] = dz[i]*0.5*(k_ozone[i]*density_ozone[i] +
                              k_ozone[i+1]*density_ozone[i+1])/mudif
    
    #total OD in the SW region
    ch_sw = ch_abs2 + ch_oz
        
    #CLOUDS contribution to the total OD
    cloud_position[0] = cloud_position[0]*1000
    cloud_position[1] = cloud_position[1]*1000
    

    if clouds == 1:
        
        #cloud index position (Position index is counted from the top to bottom)
        bot_index_c = nlayer - int(cloud_position[0]/z_top_a*nlayer)
        top_index_c = nlayer - int(cloud_position[1]/z_top_a*nlayer)
                
        for i in range(nlayer - 1):
            
            if i > bot_index_c:
                continue

            elif i <= bot_index_c and i >= top_index_c:
                ch_ir[i] = ch_ir[i] + k_cloud_LW*dz[i]/mudif
                ch_sw[i] = ch_sw[i] + k_cloud_SW*dz[i]/mudif
                                
            elif i < top_index_c:
                continue
    
    return ch_ir, ch_sw
