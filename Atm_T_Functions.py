#----------------------------------------
#ATMOSPHERE_TEMPERATURE_PROFILE FUNCTIONS
#----------------------------------------
import numpy as np

#Definition of the fixed value
albedo = 0.3                 #Planetary albedo
TSI = (1 - albedo) * 1370/4  #Total solar irradiance at the atmosphere top
mudif = 3/5                  # Clouds diffuse trasmittance
sigma = 5.6704e-8            # [W/(m^2k^4)] Stefan Boltzmann Costant     


def mixing_ratio_profile(profile, z, scale_height):
    """ This function generates the mixing ratio profile w of the gas.
        The mixing ratio is defined as the fraction of the gas over the
        total mass.
        
        This function can generates two different profile:
            1) constant mixing ratio
            2) exponential mixing ratio
    
        INPUT:
            profile      : profile type, if equal to 'costant' the function 
                           returns a constant profile, if equal to 'exponential'
                           it return an exponential profile
            z            : height vector
            scale_height : scale height H for the exp profile exp(-z/H)
            
        OUTPUT:
            w : mixing ratio profile vector
    
                                                                       """

    if scale_height <= 0:
        raise ValueError('The scale_height must to be greater than 0!')
    
    #Definition of the number of layer
    nlayer = len(z)
    
    if profile == 'costant':
        w = np.zeros(nlayer)
        w = np.full_like(w, 1)         #constant mix.ratio (example: CO2)
    elif profile == 'exponential':
        w = np.exp(-z/scale_height)   #exponential mix.ratio (example: H2O)
    else:
        raise ValueError('The profile flag must to be [costant] or [exponential]')
        
    return w


def ozone_mixing_ratio(flag, z):
    """ This function generates the mixing ratio profile for the ozone.
       
        The mixing ration will be gaussian shaped, 
        centered at 35 km of height.
        
        INPUT:
            flag   : flag to consider the presence of ozone. 1 == on, 0 == off.
            z      : height vector
            
        OUTPUT:
            w_ozone : mixing ratio profile vector       
    
                                                                      """
    
    #Definition of the number of layer    
    nlayer = len(z)
                                                                    
    if flag == 1:
        z_botton = 20000 #minimum level of stratospheric ozone
        z_top = 50000    #maximum level of stratospheric ozone
        def condition(x): return (x > z_botton) & (x < z_top)
        lay = np.where(condition(z))[0] #pos index height where there's ozone
        z0 = (z_botton + z_top)*0.5     #height maximum concentration
        sigma = (z_top - z_botton)/6   
        w_ozone = np.zeros(nlayer)
        for k in lay:
            w_ozone[k]=np.exp((-(z[k]-z0)**2)/(2*sigma**2))
    elif flag == 0:
        w_ozone = np.zeros(nlayer)
    else:
        raise ValueError('The flag for the ozone must to be 1 (on) or 0 (off)')
            
    return w_ozone


def gasses_optical_depth(dz, k, density_abs):
    """ This function computes the OD profile due to the gasses.
        It return the OD using the Lambert-Beer law.
        
        INPUT:
            dz           : vector containin the thickness of the layers.
            k            : absorption coefficient of the gasses.
            density_abs  : vector containing the density profile of the absorber.
        
        OUTPUT:
            ch           : optical depth profile vector.

                                                                       """
    #Calculation of the oprical depth                                                                   
    nlayer = len(k)                                                                   
    ch = np.zeros(nlayer)                                                                   
    
    #The calculation of the OD profile take the mean value of the layer
    #so it has been taken the average value between the two layers                                                                   
    for i in range(nlayer-1):
        ch[i] = dz[i]*0.5*(k[i]*density_abs[i] +
                           k[i+1]*density_abs[i+1])/mudif                                                                  
                                                                                                                                              
    return ch


    
def optical_depth(nlayer = 51, z_top_a = 50, scale_height_1 = 5,
                  scale_height_2 = 5, wp_1 = 'costant', wp_2 = 'costant', ozone = 0,
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
            wp_1           : profile for the mixing ration of gas 1 ('costant').
            wp_2           : profile for the mixing ration of gas 2 ('costant').
            ozone          : flag for the mixing ration of ozone (0).
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
            z     : Height vectors in meters
        
        RAISE:
            ValueError:
                If the one of the input value is negative
                If nlayer < 1
                If the bottom of the cloud is higher than the top or if the
                top of the cloud is higher than the top of the atmosphere
            
                                                                          """
    #Errors                                                                      
    if nlayer < 1:
        raise ValueError('The number of the layer must be at least 1')
        
    if (z_top_a <=0 or scale_height_1 <=0 or scale_height_2 <=0):
        raise ValueError("z_top_a, scale_height_IR and scale_height_SW must to be > 0")
        
    if (k_1_a <0 or k_2_a <0 or k_ozone_a <0 or k_cloud_LW <0 or 
        k_cloud_SW <0):
        raise ValueError("All the input must to be positive!")
            
    if (cloud_position[0] >= cloud_position[1] or cloud_position[0] <0 or
        cloud_position[1] <0):
        raise ValueError("Check clouds parameters!")
            
    if cloud_position[1] > z_top_a:
        raise ValueError("The cloud top is higher than the top of the Atmosphere")
            
        
    #nlayer must to be an intereg value
    nlayer = int(nlayer)
           
    #Definition of the absorption coefficient vectors k1 and k2
    #This vectors contains the value of the absorption coefficient, since the
    #physical properties don't change with height the vectors are constant    
    z_top_a = z_top_a*1000       # conversion Km to m of the atmosphere high
    scale_height_1 = scale_height_1*1000                   
    scale_height_2 = scale_height_2*1000 
    
    k1 = np.full_like(np.zeros(nlayer),k_1_a)
    k2 = np.full_like(np.zeros(nlayer),k_2_a)
    k_ozone = np.full_like(np.zeros(nlayer),k_ozone_a)
    
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
        #Creations of the height vector z
        z = np.zeros(nlayer)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i
        z[nlayer-1] = 0

    #Atmospheric Density Profile Calculation    
    do = 1.225                   #Air density at the grond [Kg/m^3]
    H = 101325/(9.8*do)          #Scale height fot the density profile
    d = do*np.exp(-z/H)          #Density profile vector
    
    
    # Mixing ratio shape gas 1 (IR)
    w1 = mixing_ratio_profile(wp_1, z, scale_height_1)
    # Mixing ratio shape gas 2 (SW)
    w2 = mixing_ratio_profile(wp_2, z, scale_height_2)
    #Flag for the ozone
    w_ozone = ozone_mixing_ratio(ozone, z)

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
        density_abs1 = density_abs1/tot_a1         #Normalized abs 1
        density_abs2 = density_abs2/tot_a2         #Normalized abs 2
    
    #check if there is enough space for the ozone
    if tot_ozone == 0:
        density_ozone = np.zeros(nlayer)
    else:
        density_ozone = density_ozone/tot_ozone   #Normalized ozone

    #Calculation of the oprical depth
    #ch_ir = Optical depth (OD) for the IR region (gas 1) 
    #ch_abs2 = OD from the 2° absorber gas (SW)
    #ch_oz = OD for the SW region due to ozone (SW)
        
    ch_ir = gasses_optical_depth(dz, k1, density_abs1)
    ch_abs2 = gasses_optical_depth(dz, k2, density_abs2)
    ch_oz = gasses_optical_depth(dz, k_ozone, density_ozone)
        
    #total OD in the SW region
    ch_sw = ch_abs2 + ch_oz
        
    #CLOUDS contribution to the total OD
    cloud_position = np.array(cloud_position)
    cloud_position = cloud_position*1000

    if clouds == 1:
        
        #cloud index position (Position index is counted from the top to bottom)
        bot_index_c = nlayer - int((cloud_position[0]/z_top_a)*nlayer)
        top_index_c = nlayer - int((cloud_position[1]/z_top_a)*nlayer)
                
        for i in range(nlayer - 1):
            
            if i > bot_index_c:
                continue

            elif i <= bot_index_c and i >= top_index_c:
                ch_ir[i] = ch_ir[i] + k_cloud_LW*dz[i]/mudif
                ch_sw[i] = ch_sw[i] + k_cloud_SW*dz[i]/mudif
                                
            elif i < top_index_c:
                continue
    elif clouds == 0:
        pass
    else:
        raise ValueError("clouds flag must to be 0 (off) or 1(on)!")
    
    
    return ch_ir, ch_sw, z

        
def temperature_profile(ch_ir, ch_sw):
    """This function computes the atmospheric temperature vector in an
       equilibrium situation.
       
       INPUT:
           ch_ir  : Total optical vector depth in the IR region.
           ch_sw  : Total optical vector depth in the SW region.
           
       OUTPUT:
           T : Atmospheric temperature vector, gives the temperature at each
               level of the atmosphere.

                                                                        """
            
    if (len(ch_ir) != len(ch_sw)):
        raise ValueError('The length of ch_ir and ch_sw must to be equal!')
        
    if (len(ch_sw[ch_sw < 0]) != 0) or (len(ch_ir[ch_ir < 0]) != 0):
        raise ValueError('ch_ir or ch_sw contain negative elements!')
    
    #nlayer must to be an intereg value
    nlayer = len(ch_ir)
    
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
    emis_ir = abs_ir      #emissivity
    
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