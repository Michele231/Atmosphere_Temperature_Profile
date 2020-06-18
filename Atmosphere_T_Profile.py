#----------------------------------------
#ATMOSPHERE_TEMPERATURE_PROFILE FUNCTIONS
#----------------------------------------
import numpy as np


#Definition of the variables

nlayer = 51 #Number of total layer used for the plane-parallel approximation
                #The first layer is the surface
z_top_a = 50 #Height of the atmosphere in kilometers
scale_height_1 = 5 #Scale height of the first absorber gas
scale_height_2 = 5 #Scale height of the second absorber gas
wp_1 = 1 #Mixing ratio flag for gas one. 1 = constant, other = exponential
wp_2 = 2 #Mixing ratio flag for gas two. 1 = constant, other = exponential
ozone = 1 #Flag for the stratospheric ozone
N_gas_1 = 1 #Normalisation factor for the gas one
N_gas_2 = 1 #Normalisation factor for the gas two
N_gas_ozone = 1 #Normalisation factor for the ozone
k_1_a = 0.4 #absorption coefficient for the gas one (IR)
k_2_a = 0.01 #absorption coefficient for the gas two (SW)
k_ozone_a = 0.01 #absorption coefficient for the ozone (SW)
clouds = 0 #flag to consider the presence of the clouds
cloud_position = [8, 10] #bottom and top height in kilometer
k_cloud_LW = 0 #Absorption coefficient for the clouds in the long-wave
k_cloud_SW = 0 #Absorption coefficient for the clouds in the short-wave

#Definition of the fixed value

albedo = 0.3                 #Planetary albedo
TSI = (1 - albedo) * 1370/4  #Total solar irradiance at the atmosphere top
mudif = 3/5                  # Clouds diffuse trasmittance
sigma = 5.6704e-8            # [W/(m^2k^4)] Stefan Boltzmann Costant     



def mixing_ratio_profile(flag, nlayer, z, scale_height):
    """ This function generates the mixing ratio profile w of the gas.
        The mixing ratio is defined as the fraction of the gas over the
        total mass.
        
        This function can generates two different profile:
            1) constant mixing ratio
            2) exponential mixing ratio
    
        INPUT:
            flag         : profile type, if equal to 1 the function returns a 
                           constant profile, if other it return a exponential 
                           profile
            nlayer       : number of ayer of the atmosphere
            z            : height vector
            scale_height : scale height H for the exp profile exp(-z/H)
            
        OUTPUT:
            w : mixing ratio profile vector
    
                                                                       """
    if nlayer < 1:
        raise ValueError('The number of the layer must be at least 1')
        
    if len(z) != nlayer:
        raise ValueError('The length of z must to be equal to nlayer!')
    
    nlayer = int(nlayer)
    
    if flag == 1:
        w = np.zeros(nlayer)
        w = np.full_like(w, 1)         #constant mix.ratio (example: CO2)
    else:
        w = np.exp(-z/scale_height)   #exponential mix.ratio (example: H2O)
        
    return w


def ozone_mixing_ratio(flag, z, nlayer):
    """ This function generates the mixing ratio profile for the ozone.
       
        The mixing ration will be gaussian shaped, 
        centered at 35 km of height.
        
        INPUT:
            flag   : profile type, if equal to 1 the function return a 
                     gaussian profile
            z      : height vector
            nlayer : number of ayer of the atmosphere
            
        OUTPUT:
            w_ozone : mixing ratio profile vector       
    
                                                                      """
    if nlayer < 1:
        raise ValueError('The number of the layer must be at least 1')
    
    if len(z) != nlayer:
        raise ValueError('The length of z must to be equal to nlayer!')
    
    nlayer = int(nlayer)
                                                                    
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

       
def optical_depth(nlayer = 51, z_top_a = 50, scale_height_1 = 5,
                  scale_height_2 = 5, wp_1 = 1, wp_2 = 1, ozone = 0,
                  N_gas_1 = 1, N_gas_2 = 1, N_gas_ozone = 1,
                  k_1_a = 0.4, k_2_a = 0, k_ozone_a = 0, clouds = 0,
                  cloud_position = [8, 10], k_cloud_LW = 0,
                  k_cloud_SW = 0):
    """ This function returns the optical depth (OD) vectors in the
        long wave (IR) and short wave (SW) regions.
        
        This function is able to compute the OD profile vectors in two
        spectral regions and in the situation of clear or cloudy sky.
    
        (The default values are in parentheses)
        
        INPUNT:
            nlayer         : number of layer of the atmosphere (51).           
            z_top_a        : Height of the atmosphere in kilometers (50).
            scale_height_1 : (gas 1) scale height H for the exp profile exp(-z/H)
                             for the gas assorbing in the long wave (5).
            scale_height_2 : (gas 2) scale height H for the exp profile exp(-z/H)
                             for the gas assorbing in the short wave gas 2 (5).
            wp_1           : profile flag for the mixing ration of gas 1 (1).
            wp_2           : profile flag for the mixing ration of gas 2 (1).
            ozone          : profile flag for the mixing ration of ozone (0).
            N_gas_1        : Normalisation factor for the gas 1 (1).
            N_gas_2        : Normalisation factor for the gas 2 (1).
            N_gas_ozone    : Normalisation factor for the ozone (1).
            k_1_a          : Absorption coefficient for the gas 1 (IR) (0.4).
            k_2_a          : Absorption coefficient for the gas 2 (SW) (0).
            k_ozone_a      : Absorption coefficient for the ozone (SW) (0).
            clouds         : Flag to consider the presence of the clouds (0).
            cloud_position : Bottom and top height in kilometer ([8, 10]).
            k_cloud_LW     : Absorption coefficient for the clouds in the IR.
            k_cloud_SW     : Absorption coefficient for the clouds in the SW.
            
        OUTPUT:
            ch_ir : Total optical vector depth in the IR region.
            ch_sw : Total optical vector depth in the SW region.
        
        RAISE:
            ValueError:
                If the one of the input value is negative
                If nlayer < 1
                If the bottom of the cloud is higher than the top
            
                                                                          """
    #Errors                                                                      
    try:
        if nlayer < 1:
            raise ValueError('The number of the layer must be at least 1')
        
        if (z_top_a <=0 or scale_height_1 <=0 or scale_height_2 <=0):
            raise ValueError("z_top_a, scale_height_1 and scale_height_2 must to be > 0")
        
        if (N_gas_1 <0 or N_gas_2 <0 or N_gas_ozone <0 or k_1_a <0 or k_2_a <0 or
             k_ozone_a <0 or k_cloud_LW <0 or k_cloud_SW <0):
            raise ValueError("All the input must to be positive!")
            
        if (cloud_position[0] >= cloud_position[1] or cloud_position[0] <0 or
            cloud_position[1] <0):
            raise ValueError("Check clouds parameters!")
            
    except TypeError:
        raise TypeError("The inputs must to be a number, not a string!")
        
    #nlayer must to be an intereg value
    nlayer = int(nlayer)
           
    #Definition of the absorption coefficient vectors k1 and k2
    #This vectors contains the value of the absorption coefficient, since the
    #physical properties don't change with height the vectors are constant    
    z_top_a = z_top_a*1000       # conversion Km to m of the atmosphere high
    scale_height_1 = scale_height_1*1000                   
    scale_height_2 = scale_height_2*1000 
    
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
    #This gives the quantity of absorption gasses in that layer
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
    cloud_position = np.array(cloud_position)
    cloud_position = cloud_position*1000

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

        
def temperature_profile(nlayer, ch_ir, ch_sw):
    """This function computes the atmospheric temperature vector in an
       equilibrium situation.
       
       INPUT:
           nlayer : number of ayer of the atmosphere.
           ch_ir  : Total optical vector depth in the IR region.
           ch_sw  : Total optical vector depth in the SW region.
           
       OUTPUT:
           T : Atmospheric temperature vector, gives the temperature at each
               level of the atmosphere.

                                                                        """
    
    if nlayer < 1:
        raise ValueError('The number of the layer must be at least 1')
        
    if (len(ch_ir) != nlayer) or (len(ch_sw) != nlayer):
        raise ValueError('The length of z must to be equal to nlayer!')
        
    if (len(ch_sw[ch_sw < 0]) != 0) or (len(ch_ir[ch_ir < 0]) != 0):
        raise ValueError('ch_ir or ch_sw contain negative elements!')
        
    #Calculation of the comulative optical depth (total OD) in the ir
    #and sw region. Total OD is evaluated as the comulative sum of the OD vectors        
    tot_ch_ir = np.zeros(nlayer)
    tot_ch_sw = np.zeros(nlayer)
    
    tot_ch_ir[1:nlayer] = np.cumsum(ch_ir[0:nlayer-1])
    tot_ch_sw[1:nlayer] = np.cumsum(ch_sw[0:nlayer-1])
    
    #Computation the the transmittance in the ir and sw regions
    #The trasmittance is defined as T=e^(-OD)    
    trans_ir = np.exp(-ch_ir)
    trans_sw = np.exp(-ch_sw)
    
    #The trasmittance of the last layer, which is associated withe the 
    #ground is set to 0, since the ground is considered a black body    
    trans_ir[nlayer - 1] = 0
    trans_sw[nlayer - 1] = 0
    
    #Computation of the absorbance and the emissivity of the layer 
    #The emissivity is equal to the absorbance (Kirchhoff's law)    
    abs_ir = 1 - trans_ir #absorbance
    abs_sw = 1 - trans_sw 
    
    emis_ir = abs_ir
    emis_sw = abs_sw
    
    #Computation of the trasmissivity symmetric matrix     
    trasm_m_ir = np.ones((nlayer,nlayer))
              
    for i in range(nlayer - 2):
        for j in range(i + 2, nlayer):
            trasm_m_ir[i][j] = trasm_m_ir[i][j-1]*trans_ir[j-1]
            trasm_m_ir[j][i] = trasm_m_ir[i][j]
            
    #Computation of the total comulative trasmittance in the sw    
    tot_trans_sw = np.exp(-tot_ch_sw)
    
    #Definition of the M matrix 
    M= np.ones((nlayer,nlayer))
    
    for i in range(nlayer):
        for j in range(nlayer):
            M[i][j] = trasm_m_ir[i][j]*emis_ir[j]*abs_ir[i]

    for i in range(nlayer - 1):
        M[i][i] = -2*emis_ir[i]
    
    M[nlayer-1][nlayer-1] = -emis_ir[nlayer-1]
    
    #Computation of the solar irradiance (sw) absorbed by the atmosphere
    irr_abs = np.zeros(nlayer)
    
    for i in range(nlayer):
        irr_abs[i] = -TSI*tot_trans_sw[i]*abs_sw[i]
    
    #The system that needs to be solved is:
    # irr_abs = M*(sigma*T^4) 
    #with sigma*T^4 (sT4) vector containing the Stefan–Boltzmann law emission
    sT4 = np.linalg.solve(M,irr_abs)
    
    #It is possible to found the vector describing the temperature profile T as
    
    T = (sT4/sigma)**0.25
    
    return T