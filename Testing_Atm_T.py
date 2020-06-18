#Testing section of Atm_Temperature functions

import numpy as np
import Atmosphere_T_Profile as at
import pytest
from hypothesis.strategies import tuples
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given

#Test for the function "mixing_ratio_profile"
@given(st.integers(1,2), st.integers(1,10), st.floats(1,10),
       st.floats(1,10))
@settings(max_examples = 5)
def test_mixing_ratio_profile(flag, nlayer, z_top_a, scale_height):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #This vector contains the heights of each layer       
    z = np.zeros(nlayer)
    if nlayer > 1:
        dzs = z_top_a/(nlayer-1)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i
    
    #check if the output length is the correct
    assert(len(at.mixing_ratio_profile(flag, nlayer, z, 
                                       scale_height)) == nlayer)
    
    #check if a ValueError arise if nlay is smaller than 1
    with pytest.raises(ValueError):
        at.mixing_ratio_profile(1,0,np.array([1]),1)
        
    #check if ValueError arise if the length of z is different from nlayer
    with pytest.raises(ValueError):
        at.mixing_ratio_profile(1,2,np.array([1]),1)  
    
#Test for the function "mixing_ratio_profile"    
@given(st.integers(1,2), st.integers(1,10), st.floats(10,50))
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
    assert(len(at.ozone_mixing_ratio(flag, z, nlayer)) == nlayer)
    
    #check that if the atmosphere height is lower than 20km the ozone vector
    #profile should contain only zeros
    if z_top_a < 20:
        assert(np.count_nonzero(at.ozone_mixing_ratio(flag, z, nlayer)) == 0)
    
    #check if a ValueError arise if nlay is smaller than 1
    with pytest.raises(ValueError):
        at.ozone_mixing_ratio(1,np.array([1]),0)        

    #check if ValueError arise if the length of z is different from nlayer
    with pytest.raises(ValueError):
        at.ozone_mixing_ratio(1,np.array([1]),2)         


#Test for the function "optical_depth"
@given(nlayer = st.integers(1,10), z_top_a = st.floats(10,50),
       scale_height_1 = st.floats(1,5), scale_height_2 = st.floats(1,5),
       wp_1 = st.integers(1,2), wp_2 = st.integers(1,2), ozone = st.integers(0,1),
       N_gas_1 = st.floats(0,10), N_gas_2 = st.floats(0,10), N_gas_ozone = st.floats(0,10),
       k_1_a = st.floats(0,5), k_2_a = st.floats(0,5), k_ozone_a = st.floats(0,5),
       clouds = st.integers(0,1), cloud_pos = tuples(st.floats(0,9), st.floats(10,60)),
       k_cloud_LW = st.floats(0,5), k_cloud_SW = st.floats(0,5))       
@settings(max_examples = 5)
def test_optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2, wp_1,
                       wp_2, ozone, N_gas_1, N_gas_2, N_gas_ozone, k_1_a,
                       k_2_a, k_ozone_a, clouds, cloud_pos,
                       k_cloud_LW, k_cloud_SW):
    
    #ch_ir and ch_sw are the output
    ch_ir, ch_sw = at.optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2,
                                    wp_1, wp_2, ozone, N_gas_1, N_gas_2,
                                    N_gas_ozone, k_1_a, k_2_a, k_ozone_a, clouds,
                                    cloud_pos, k_cloud_LW, k_cloud_SW)
    
    #check if the outputs have the correct length
    assert(len(ch_ir) == len(ch_ir) == nlayer)
    
    #check that if all the absorption coefficent are zero, the outputs must to
    #be two zeros vectors    
    assert(np.count_nonzero(at.optical_depth(k_1_a = 0, k_2_a = 0, k_ozone_a = 0,
                                             k_cloud_LW = 0, k_cloud_SW = 0)) == 0)
    
    #check that outputs do not contain negative elements
    assert(len(ch_ir[ch_ir < 0]) == 0)
    assert(len(ch_sw[ch_sw < 0]) == 0)
    
    #check that when the bottom of the cloud is => of the top an error arise
    with pytest.raises(ValueError):
        at.optical_depth(cloud_position = (5,4))

    #check the error for a negative input     
    with pytest.raises(ValueError):
        at.optical_depth(k_2_a = -1)
        
    #check the error for a string input     
    with pytest.raises(TypeError):
        at.optical_depth(nlayer = '1')
    
  
#Test for the function "temperature_profile" 
@given(nlayer = st.integers(1, 25))
@settings(max_examples = 5)
def test_temperature_profile(nlayer):
    
    #definition of two random positive vectors of length = nlayer
    ch_ir = np.random.rand(nlayer)
    ch_sw = np.random.rand(nlayer)
    
    T = at.temperature_profile(nlayer, ch_ir, ch_sw)
    
    #check if the output length is the correct
    assert(len(T) == nlayer)
    
    #check that outputs do not contain negative elements
    assert(len(T[T < 0]) == 0)
    
    #check that when there is a negative element on the input an error arise
    with pytest.raises(ValueError):
        at.temperature_profile(nlayer, ch_ir - np.ones(nlayer), ch_sw)
    

if __name__ == '__main__':
    pass
