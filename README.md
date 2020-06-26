# ATMOSPHERIC TEMPERATURE PROFILE.

### Theoretical Background

The Earth's atmosphere is relatively trasparent to incoming solar radiation (short-wave radiation), and opaque to outgoing long-wave radiation 
emitted by the Earth's surface and by the atmosphere itself. For this reason part of the outgoing radiation is blocked. Populary this phenomena 
is known as ***greenhouse effect***.

Much of the absorption and reemission of outgoing radiation are due to air molecules, but cloud droplets and aerosol. The atmosphere also scatters
the radiation that passes through it, giving rise to a wide range of optical effects, including the blue color of the sky.

### The Vertical Structure
![alt text](https://github.com/Michele231/Esame_Software/blob/master/Figure/Atm_TEmperature_Profile.png "Atmosphere mean temperature profile")

The density at the sea level is  1.25 ![](http://www.sciweavers.org/upload/Tex2Img_1593036352/render.png). 
Density and pressure decrease nearly exponentially with the height:

![Pressure profile](https://latex.codecogs.com/gif.latex?p%20%3D%20p_0%5E%7B-z/H%7D)

where H is refered to as the scale height, which ranges, in the lowest 100km, roughly from 7 to 8km. Since the variation along the z direction
is much larger tham the correspondig horizontal and time variations, it is usefull to define a ***standard atmosphere*** wich represents the 
horizontally and temporally averaged structure of the atmosphere.

The atmosphere is composed of a mixture of gasses:


| Costituent     | Fractional Concentration         V/V |
|----------------|--------------------------------------|
| Nitrogen       |                78.08%                |
| Oxigen         |                20.95%                |
| Argon          |                 0.93%                |
| Water Vapor    |                 0-5%                 |
| Carbon Dioxide |                400ppm                |
| Methane        |                1.75ppm               |
| Nitrous Oxide  |                0.3ppm                |
| Ozone          |               0-0.1ppm               |

The ***concentration*** (or the mixing ratio if I'm considering the masses) of the of Nitrogen, Oxigen, Argon, and Carbon Dioxide tend 
to be quite uniform and indipendent from height due to the turbolent mixing. Gasses like water has a very high variability, and generally 
for this type of gasses the concentration profile tends to be exponential decreasing.

The vertical profile of the temperature for the typical condition, as shown in the figure above, provides a basis for dividing the atmosphere
into four layer:

* ***Troposhere***: marked by a generally decreasing temperatures with height.

* ***Stratosphere***: where the vertical mixing is strongly inhibited by the increasing temperature with the height (due to the ozone layer).

* ***Mesosphere***: characterized by a decrease in temperature with the altitude.

* ***Thermosphere***: where there is an increasing in temperature due to the absorption of the solar radiation by the oxigen and nitrogen.

## Getting Started: Atm_T_Profile Model

###Overview

Atm_T_Profile is a simple model for the solution of the radiative transfert problem (without scattering). For a given atmosphere, the model
outputs are the optical depth in two channel (short-wave and infrared) and the temperature profile of the atmosphere and the surface.

The system is assumed to be in a stationary state with energy transfer occurring only by means of radiation. The atmosphere is divided into
n parallel layers. Each layer is in radiative energy balance, meaning that all the energy that is absorbed by the layer is also emitted by 
it like a grey body at the temperature T with an emissivity coefficient equal to the absorption coefficient (Kirchhoff's law of 
thermal radiation).

The equations that describe the energy balance for each layer have this simple structure:

![Energy Equilibrium Equation](https://latex.codecogs.com/gif.latex?E_%7Babs%7D%20%3D%20E_%7Bem%7D)

The model uses two channels, a short-wave (SW) channel to decribe the sun's radiation (visible/near-IR radiation) and a long-wave channel
(IR) to decribe the Earth's radiation (mid-IR/far-IR radiation). Since the scattering is not considered, when the incoming radiation hits 
the layer a fraction of it will be absorbed and the other part will pass forward. Calling T the trasmissivity of the layer and A the 
absorptivity (in the long-wave region) we will have the conservation of the energy under the form:

![Energy Conservation](https://latex.codecogs.com/gif.latex?A_n&plus;T_n%20%3D%201)

The total radiation absorbed by the higher layer will be given by:

![Higher Layer Absorption](https://latex.codecogs.com/gif.latex?S%281-X_1%29&plus;E_2%5Csigma%5Ctheta_2%5E4A_1%20&plus;%20E_3%5Csigma%5Ctheta_3%5E4T_2A_1%20&plus;%20...%20&plus;E_n%5Csigma%5Ctheta_n%5E4T_2...T_%7Bn-1%7DA_1%20%3D%202E_1%5Csigma%5Ctheta_1%5E4)

Whrere X is the trasmissivity in the short-wave region and S is the total solar irradiance at the top of the atmosphere. Theta is the
temperature of the layer n-th and sigma is the Stefan–Boltzmann constant.

Knowing the absorptivity (from the gasses profile) it is possible to build a system of n equations (one for each layer) 
and n unknown variables, i. e. the theta temperatures of each layer. Solving it produces the result of interest.

###Installation 

In order to install the model clone the repository [Esame_Software](https://github.com/Michele231/Esame_Software):
```
git clone https://github.com/Michele231/Esame_Software
cd Esame_Software
```

###Parameters of the Model

Inside the repository there is the following files:

*[Figure](https://github.com/Michele231/Esame_Software/tree/master/Figure) where are stored the figure for the README.md file.

*[OUTPUT](https://github.com/Michele231/Esame_Software/tree/master/OUTPUT) that is the default folder of the output of the model.

*[Atm_T_Functions.py](https://github.com/Michele231/Esame_Software/blob/master/Atm_T_Functions.py) contains the functions used in the model.

*[Atm_T_Profile.py](https://github.com/Michele231/Esame_Software/blob/master/Atm_T_Profile.py) is the model that you want to run.

*[Atmosphere_T_Configuration.ini](https://github.com/Michele231/Esame_Software/blob/master/Atmosphere_T_Configuration.ini) is the configuration
file where you can modify the parameters describing the atmosphere.

*[Configuration_File_Maker.py](https://github.com/Michele231/Esame_Software/blob/master/Configuration_File_Maker.py) is the code used to generate
the Atmosphere_T_Configuration.ini file.

*[Testing_Atm_T.py](https://github.com/Michele231/Esame_Software/blob/master/Testing_Atm_T.py) contains the testing fot the Atm_T_Functions.py.

The model allows you to build an atmosphere by going to specify several parameters that describe it (within the configuration file).
The parameters that you can modify are:

####General Variable

* ***number_of_layers***: It is the number of layers into which the atmosphere is divided. It has to be greater than zero (Hint: put at least 51 layers).
The last layer is associated with the surface. 

* ***top_of_atmopshere***: It rappresents the height of the atmosphere. Since the model embodies the Kirchhoff law, which is valid only if is possible to
consider an local thermodynamic equilibrium situation, it is suggested not to exceed 50 km in height.

* ***scale_height_gas_ir***: It is the scale parameter for the exponential mixing ratio profile for the gasses in the IR channel.

* ***scale_height_gas_sw***: It is the scale parameter for the exponential mixing ratio profile for the gasses in the SW channel.

* ***wp_profile_gas_ir***: Flag for the type of mixing ratio profile of the gasses in the IR channel. If equal to 1 the mixing ratio profile will be 
constant with the height (exaple: CO2). Otherwise the profile will be exponential (exaple: H2O)

* ***wp_profile_gas_sw***: Flag for the type of mixing ratio profile of the gasses in the SW channel. If equal to 1 the mixing ratio profile will be 
constant with the height. Otherwise the profile will be exponential

* ***presence_of_ozone***: Flag for the presence of the ozone layer. If equal to 1 the ozone is considered, otherwise not.

* ***abs_coefficient_gas_ir***: Absorption coefficient for the gasses in the IR channel. The absorption coefficient is obtained as the product 
between the cross section of absorption and the mass concentration of the gas. Changing this parameter can have the double meaning of changing 
the cross section of the gas or changing its concentration

* ***abs_coefficient_gas_sw***: Absorption coefficient for the gasses in the SW channel.

* ***abs_coefficient_ozone***: Absorption coefficient for the gasses in the ozone.

####Clouds_Variables

* ***presence_of_clouds***: Flag for the presence of clouds. If equal to 1 clouds is considered, otherwise not.

* ***cloud_bottom***: Bottom level of the clouds.

* ***cloud_top***: Top level of the clouds.

* ***cloud_ir_abs_coeff***: Absorption coefficient for the clouds in the IR channel.

* ***cloud_sw_abs_coeff***: Absorption coefficient for the clouds in the SW channel.

####Output_Path

* ***output_path_graph***: Path for the outputs. The outputs of this program will be a the temperature and OD profile for the atmosphere.

###Usage and Examples

If you want to run the model, first use the file [Atmosphere_T_Configuration.ini](https://github.com/Michele231/Esame_Software/blob/master/Atmosphere_T_Configuration.ini)
in order to set the atmosphere parameters, then use (For the Windows user):
```
python Atm_T_Profile.py
```
The outputs will be found in the output path choosen in the configuration file. The outputs file will be:

* ***Temperature_Profile.txt***: It contains the temperature value as function of the height.

* ***Temperature_Profile.png***: It contains the temperature chart as function of the height.

* ***OD_Profile.png***: It contains the optical depth chart in function of the height for the two channel (Short-wave and IR).

#### Example: increase the concentration of greenhouse gases

Let's imagine increasing the concentration of greenhouse gases by 50%, letting the other parameters unchanged.

In the first case in figure ***wp_profile_gas_ir*** has been setted to 0.8, in the second case it has been setted to 1.2.

![Temperature profile changing with the increasing of the gasses concentrations](https://github.com/Michele231/Esame_Software/blob/master/Figure/p50_unite.PNG)








