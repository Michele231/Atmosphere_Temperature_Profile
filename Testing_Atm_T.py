#Testing section of Atm_Temperature functions

import numpy as np
import Atmosphere_T_Profile as at
import pytest
from hypothesis import strategies as st
from hypothesis import settings
from hypothesis import given

#Test for the function "mixing_ratio_profile"
@given(st.integers(), st.integers(1,10), st.floats(1,10),
       st.floats(1,10))
@settings(max_examples = 2)
def test_mixing_ratio_profile(flag, nlayer, z_top_a, scale_height):
    
    #Defining a z vector associates with nlayer and z_top_a (atmosphere top height)
    #This vector contains the heights of each layer       
    z = np.zeros(nlayer)
    if nlayer > 1:
        dzs = z_top_a/(nlayer-1)
        for i in range(nlayer-1):
            z[i] = z_top_a - dzs*i
    
    #check if the output lenght is the correct
    assert(len(at.mixing_ratio_profile(flag, nlayer, z, 
                                       scale_height)) == nlayer)
    
    #check if a ValueError arise if nlay is smaller than 1
    with pytest.raises(ValueError):
        result = at.mixing_ratio_profile(1,0,np.array([1]),1)
        
    #check if 
  
    
#Test for the function "mixing_ratio_profile"    
@given(st.integers(), st.integers(1,10), st.floats(10,50))
@settings(max_examples = 2)
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
    #check if the output lenght is the correct
    assert(len(at.ozone_mixing_ratio(flag, z, nlayer)) == nlayer)
    
    #check that if the atmosphere height is lower than 20km the ozone vector
    #profile should contain only zeros
    if z_top_a < 20:
        assert(np.count_nonzero(at.ozone_mixing_ratio(flag, z, nlayer)) == 0)
    
    #check if a ValueError arise if nlay is smaller than 1
    with pytest.raises(ValueError):
        result = at.ozone_mixing_ratio(1,np.array([1]),0)        
        
    
#Test for the function "temperature_profile" 



if __name__ == '__main__':
    pass
