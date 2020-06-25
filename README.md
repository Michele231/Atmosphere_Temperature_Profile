# ATMOSPHERIC TEMPERATURE PROFILE.

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

The ***concentration*** (or the mixing ratio if I considering the masses) of the of Nitrogen, Oxigen, Argon, and Carbon Dioxide tend 
to be quite uniform and indipendent from height due to the turbolent mixing. Gasses like water has a very high variability, and generally 
for this type of gasses the concentration profile tends to be exponential decreasing.

The vertical profile of the temperature for the typical condition, as shown in the figure above, provides a basis for dividing the atmosphere
into four layer:

* ***Troposhere***: marked by a generally decreasing temperatures with height.

* ***Stratosphere***: where the vertical mixing is strongly inhibited by the increasing temperature with the height (due to the ozone layer).

* ***Mesosphere***: characterized by a decrease in temperature with the altitude.

* ***Thermosphere***: where there is an increasing in temperature due to the absorption of the solar radiation by the oxigen and nitrogen.

## Atm_T_Profile Model


The system is assumed to be in a stationary state with energy transfer occurring only by means of radiation. 
Each layer is in radiative energy balance. The equations that describe the energy balance for each layer have this simple structure:

