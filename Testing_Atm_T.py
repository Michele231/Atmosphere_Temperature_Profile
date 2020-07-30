#Testing section of Atm_Temperature functions

import numpy as np
import Atm_T_Functions as at
import pytest
from hypothesis.strategies import tuples
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given

#Test for the function "mixing_ratio_profile"
types = ['costant','exponential'] #definition of the two types of profile used

@given(st.integers(0,1), st.integers(1,10), st.floats(1,10),
       st.floats(1,10))
@settings(max_examples = 5)
def test_mixing_ratio_profile(profile, nlayer, z_top_a, scale_height):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #This vector contains the heights of each layer       
    z = np.zeros(nlayer)
    if nlayer > 1:
        dzs = z_top_a/(nlayer-1)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i
    
    #check if the output length is the correct
    assert(len(at.mixing_ratio_profile(types[profile], z, 
                                       scale_height)) == nlayer)
    
    with pytest.raises(ValueError):
        
        #check if ValueError arise if the scale_height is negative
        at.mixing_ratio_profile('costant',np.array([1]),-1)  
 
        #check if ValueError arise if the profile input is wrong
        at.mixing_ratio_profile('costan',np.array([1]),-1) 

    
#Test for the function "mixing_ratio_profile"    
@given(st.integers(0,1), st.integers(1,10), st.floats(10,50))
@settings(max_examples = 5)
def test_ozone_mixing_ratio(flag, nlayer, z_top_a):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #This vector contains the heights of each layer       
    z = np.zeros(nlayer)
    if nlayer > 1:
        dzs = z_top_a/(nlayer-1)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i
    
    #trasform the km in meters
    z = z*1000
    #check if the output length is the correct
    assert(len(at.ozone_mixing_ratio(flag, z)) == nlayer)
    
    #check that if the atmosphere height is lower than 20km the ozone vector
    #profile should contain only zeros
    if z_top_a < 20:
        assert(np.count_nonzero(at.ozone_mixing_ratio(flag, z)) == 0)
    
    with pytest.raises(ValueError):
        
        #check that if the flag is different from 0 or 1 a ValueError arrises
        at.ozone_mixing_ratio(3,np.array([1]))         



#Test for the function "gasses_optical_depth"
@given(st.integers(0,50))
@settings(max_examples = 5)
def test_gasses_optical_depth(nlayer):
    
    #definition of 3 random POSIVIVE vector to simulate dz, k, density_abs
    dz = np.random.rand(nlayer)
    k = np.random.rand(nlayer)
    density_abs = np.random.rand(nlayer)
    
    ch = at.gasses_optical_depth(dz, k, density_abs)
    
    
    assert(len(ch[ch < 0]) == 0)



#Test for the function "optical_depth"
@given(nlayer = st.integers(1,51), z_top_a = st.floats(20,50),
       scale_height_1 = st.floats(1,5), scale_height_2 = st.floats(1,5),
       wp_1 = st.integers(0,1), wp_2 = st.integers(0,1), ozone = st.integers(0,1),
       k_1_a = st.floats(0,5), k_2_a = st.floats(0,5), k_ozone_a = st.floats(0,5),
       clouds = st.integers(0,1), cloud_pos = tuples(st.floats(0,9), st.floats(10,20)),
       k_cloud_LW = st.floats(0,5), k_cloud_SW = st.floats(0,5))       
@settings(max_examples = 5)
def test_optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2, wp_1,
                       wp_2, ozone, k_1_a, k_2_a, k_ozone_a, clouds, cloud_pos,
                       k_cloud_LW, k_cloud_SW):
    
    #ch_ir and ch_sw are the output
    ch_ir, ch_sw, z = at.optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2,
                                    types[wp_1], types[wp_2], ozone, k_1_a, k_2_a, 
                                    k_ozone_a, clouds, cloud_pos, k_cloud_LW, k_cloud_SW)
    
    #check if the outputs have the correct length
    assert(len(ch_ir) == len(ch_ir) == len(z) == nlayer)
        
    #check that outputs do not contain negative elements
    assert(len(ch_ir[ch_ir < 0]) == 0)
    assert(len(ch_sw[ch_sw < 0]) == 0)
    
    #check that the last element of z is zero and the first z_top_a
    assert(z[nlayer-1] == 0)
    #if nlayer = 1 we are considering only the surface
    if nlayer != 1:
        assert(z[0] == z_top_a*1000)
        
    #check that if all the absorption coefficents are zero, the outputs must to
    #be two zeros vectors
    ch_ir, ch_sw, z = at.optical_depth(k_1_a = 0, k_2_a = 0, k_ozone_a = 0,
                                       k_cloud_LW = 0, k_cloud_SW = 0)
    assert(np.count_nonzero(ch_ir) == 0)
    assert(np.count_nonzero(ch_sw) == 0)
    
    with pytest.raises(ValueError):
        #check that when the bottom of the cloud is => of the top an error arise
        at.optical_depth(cloud_position = (5,4))

        #check the error for a negative input     
        at.optical_depth(k_2_a = -1)
                
        #check when the top of the cloud is higher than the atmosphere  
        at.optical_depth(z_top_a = 10, cloud_position = (8,11))

        #check when cloud != 0 and 1 
        at.optical_depth(clouds = 3)
  
#Test for the function "temperature_profile" 
@given(nlayer = st.integers(1,51))
@settings(max_examples = 5)
def test_temperature_profile(nlayer):
    
    #definition of two random positive vectors of length = nlayer
    ch_ir = np.random.rand(nlayer)
    ch_sw = np.random.rand(nlayer)
    
    T = at.temperature_profile(ch_ir, ch_sw)
    
    #check if the output length is the correct
    assert(len(T) == nlayer)
    
    #check that outputs do not contain negative elements
    assert(len(T[T < 0]) == 0)
    
    
    with pytest.raises(ValueError):
        #check that when there is a negative element on the input an error arise
        at.temperature_profile(ch_ir - np.ones(nlayer), ch_sw)
        
        #check that when ch_ir and ch_sw have differen len. a ValueError arises
        at.temperature_profile(np.array([1,2]), np.array([1]))
    


if __name__ == '__main__':
    pass

