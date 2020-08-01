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

@given(st.integers(0,1), st.integers(1,50), st.floats(15,50),
       st.floats(1,10))
@settings(max_examples = 5)
def test_mixing_ratio_profile(profile, nlayer, z_top_a, scale_height):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #z obtained from optical_depth function.  _ is used for useless parameter.      
    _, _, z = at.optical_depth(nlayer = nlayer, z_top_a = z_top_a)
    
    w = at.mixing_ratio_profile(types[profile], z, scale_height)
    
    #check if the output length is the correct
    assert(len(w) == nlayer)
    
    #check that w does not contain negative value
    assert(len(w[w < 0]) == 0)
    
    #check that the profile reproduce the correct behavior
    if types[profile] == 'costant':
        assert(w[0] == w[nlayer - 1])
    elif types[profile] == 'exponential':
        assert(w[0] <= w[nlayer - 1])
    
    with pytest.raises(ValueError):
        
        #check if ValueError arise if the scale_height is negative
        at.mixing_ratio_profile('costant',np.array([1]),-1)  
 
        #check if ValueError arise if the profile input is wrong
        at.mixing_ratio_profile('costan',np.array([1]),-1) 

    
#Test for the function "mixing_ratio_profile"    
@given(st.integers(0,1), st.integers(1,50), st.floats(15,50))
@settings(max_examples = 5)
def test_ozone_mixing_ratio(flag, nlayer, z_top_a):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #z obtained from optical_depth function. _ is used for useless parameter.     
    _, _, z = at.optical_depth(nlayer = nlayer, z_top_a = z_top_a)
    
    w_ozone = at.ozone_mixing_ratio(flag, z)
    
    #check if the output length is the correct
    assert(len(w_ozone) == nlayer)
    
    #check that w_ozone does not contain negative value
    assert(len(w_ozone[w_ozone < 0]) == 0)
    
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
    np.random.seed(30)
    dz = np.random.rand(nlayer)
    k = np.random.rand(nlayer)
    density_abs = np.random.rand(nlayer)
    
    ch = at.gasses_optical_depth(dz, k, density_abs)
    
    #check that ch does not contain negative value
    assert(len(ch[ch < 0]) == 0)
    #check that ch is nlayer length 
    assert(len(ch) == nlayer)


#Test for the function "optical_depth"
@given(nlayer = st.integers(1,51), z_top_a = st.floats(20,50),
       scale_height_1 = st.floats(1,5), scale_height_2 = st.floats(1,5),
       wp_1 = st.integers(0,1), wp_2 = st.integers(0,1), ozone = st.integers(0,1),
       k_1_a = st.floats(0,5), k_2_a = st.floats(0,5), k_ozone_a = st.floats(0,5))       
@settings(max_examples = 5)
def test_optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2, wp_1,
                       wp_2, ozone, k_1_a, k_2_a, k_ozone_a):
    
    #ch_ir and ch_sw are the output
    ch_ir, ch_sw, z = at.optical_depth(nlayer, z_top_a, scale_height_1, scale_height_2,
                                    types[wp_1], types[wp_2], ozone, k_1_a, k_2_a, 
                                    k_ozone_a)
    
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
    ch_ir, ch_sw, z = at.optical_depth(k_1_a = 0, k_2_a = 0, k_ozone_a = 0)
    assert(np.count_nonzero(ch_ir) == 0)
    assert(np.count_nonzero(ch_sw) == 0)
    
    with pytest.raises(ValueError):
        #check the error for a negative input     
        at.optical_depth(k_2_a = -1)
                


#Test for the function "clouds_optical_depth"
@given(z_top_a = st.floats(21,51), cloud_position = tuples(st.floats(0,9), st.floats(10,20)),
       k_cloud_LW = st.floats(0,1), k_cloud_SW = st.floats(0,1))
@settings(max_examples = 5)
def test_clouds_optical_depth(z_top_a, cloud_position, k_cloud_LW, k_cloud_SW):
    
    ch_ir_c, ch_sw_c = at.clouds_optical_depth(z_top_a = z_top_a,
                                            cloud_position = cloud_position,
                                            k_cloud_LW = k_cloud_LW,
                                            k_cloud_SW = k_cloud_SW)
    
    #check that the clouds increase the total OD. (the starting ch_ir/sw are zeros)
    assert(sum(ch_ir_c) >= 0)
    assert(sum(ch_sw_c) >= 0)
    #check that outputs do not contain negative elements
    assert(len(ch_ir_c[ch_ir_c < 0]) == 0)
    assert(len(ch_sw_c[ch_sw_c < 0]) == 0)
    
    with pytest.raises(ValueError):
    #check that when the bottom of the cloud is => of the top an error arise
        at.clouds_optical_depth(cloud_position = (5,4))
        #check when the top of the cloud is higher than the atmosphere  
        at.optical_depth(z_top_a = 10, cloud_position = (8,11))
        
        
        
#Test for the function "temperature_profile" 
@given(nlayer = st.integers(1,51))
@settings(max_examples = 5)
def test_temperature_profile(nlayer):
    
    #definition of two random positive vectors of length = nlayer
    np.random.seed(30)
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

