# THINCARB

##What is THINCARB?

THINCARB stands for THermodynamics of INorganic CARBon and is a computational 
model for estimating the excess partial pressure of CO2 (EpCO2), and the 
equilibrium constants, activities, concentrations, and fractionation, of the 
hydroxyl and principal carbon-containing ions present in natural waters (ie, 
rivers and lakes) from basic water quality determinands.

THINCARB is not suitable for marine environments.

At the heart of THINCARB are the equations developed by Neal et al (1998) [1] 
and which have proved to be extremely useful. However, in the intervening years 
some minor corrections became apparent, and the platform on which that original 
model was deployed became obsolete! In addition, it was noted that there was a 
straightforward extension of the model that would also provide estimates of 
Dissolved Inorganic Carbon (DIC) concentrations, something that is not routinely 
measured experimentally. So against this background it was decided to make a 
corrected, enhanced, model available to a new generation of water quality 
scientists. This enhanced model is THINCARB! [2]

The new DIC calculations have been validated using literature data and seem to 
provide quantitative agreement with experimental measurements except in samples 
having both low alkalinity and high levels of Dissolved Organic Carbon (DOC).


##What do I need to run THINCARB?

You can run THINCARB in one of two ways: as a macro embedded in a Microsoft 
Excel (Excel Version 14.0, 'Excel 2010') or later spreadsheet, or by using the 
Python language (Versions 2.7.x and 3.x.x are supported).


##What input data does THINCARB require?

The absolute minimum input data are the pH and Gran alkalinity of a water sample 
(in micro-equivalents/litre), though temperature (in degrees C) has a big effect 
on the calculations, so if this is not known then an ‘educated guess’ will be 
necessary! However, all three are usually routinely measured water quality 
determinands.

Optional additional inputs, which can be used to refine the calculations if 
available, are the altitude (in metres) at which the water sample was taken and 
the calcium ion concentration (in milligrams/litre).


##What does THINCARB calculate?

The full list of output values calculated is shown below.

* Excess partial pressure of dissolved CO2 (EpCO2) {5 successive approximations}
* CaCO3 saturation
* Equilibrium constants for:
  * Formation of H2CO3 from CO2 (k0)
  * Dissociation of H2CO3 (k1)
  * Dissociation of HCO3- (k2)
  * Formation of CaHCO3+ (k3)
  * Formation of CaCO3 (k4)
  * Formation of CaOH+ (k5)
  * Formation of H2O (k6)
  * Dissolution of solid CaCO3 (k7)
* Chemical activities of:
  * OH-
  * H2CO3
  * HCO3-
  * CO32-
  * Ca2+
  * CaHCO3+
  * CaCO3
  * CaOH+
* Concentrations of:
  * Total Ca
  * HCO3-
  * CO32-
  * H2CO3
  * C in HCO3-
  * C in CO32-
  * C in H2CO3
  * Total DIC
  * DIC as HCO3
  * DIC as CO3
  * DIC as H2CO3
* Ionic strength
* Monovalent activity coefficient
* Divalent activity coefficient


##How does THINCARB work?

For the physical chemistry behind the model the reader is referred to the 
references [1],[2].

The algorithmic approach of both the Excel and Python implementations of 
THINCARB is the same: an initial approximation for EpCO2 is gradually refined 
(optimised) by minimising the overall charge balance in the system. In Excel 
this optimisation is performed with the Goal Seek function. In Python a simple, 
but tenacious, bisection algorithm is used. The latter usually achieves a better 
residual charge balance, but both approaches will give essentially the same 
outputs for the same residual charge balance. For this reason care must be 
exercised if comparing results from the Excel implementation with results from 
the Python implementation!

*An interesting philosophical debate is whether a residual charge balance of, 
say, 10^-9 e is actually physically more important or realistic than, say, a 
residual charge balance of 10^-4 e. However, this difference is sufficient to 
produce variations in EpCO2, [HCO3-], and the total [DIC] of almost 4%! So 
beware!*


##Speed

How quickly THINCARB processes datasets depends on several factors: the 
specification of the computer, the acceptable residual charge balance, how 
close to that acceptable residual charge balance the initial estimate of EpCO2 
puts the starting charge balance, and the efficiency of the optimisation 
algorithm.

The Python implementation has been coded with human-readability (not speed) in 
mind, and the bisection algorithm is very robust but not particularly fast. 
Consequently there is undoubtedly scope for future speed improvements if needed. 
But as a guide, during real use of THINCARB on a harmonised dataset, the Python 
2.7 implementation processed 8300 readings from file in 88 mins (ie, roughly 
1.5/sec) on an Intel quad-core 3.2 GHz CPU based PC with 12 GB RAM running 
Python from a Windows 7 command line interface.


##References

[1] 'An assessment of excess carbon dioxide partial pressures in natural waters 
based on pH and alkalinity measurements'. Colin Neal, W Alan House, Kevin Down. 
*The Science of the Total Environment*. 210/211 (1998) 173-185.

[2] 'Inorganic Carbon Dominates Total Dissolved Carbon Concentrations and Fluxes 
in British Rivers: Application of the THINCARB Model - Thermodynamics of Inorganic 
Carbon'. Helen Jarvie, Stephen King, Colin Neal. *The Science of the Total 
Environment*. 575 (2016) 496-512. [10.1016/j.scitotenv.2016.08.201](http://dx.doi.org/10.1016/j.scitotenv.2016.08.201)


##Acknowledging THINCARB

If you use THINCARB in your work please acknowledge as much in your publications
/presentations! For example:

*This work benefitted from THINCARB, software developed by the NERC Centre for 
Ecology & Hydrology and the STFC. See http://smk78.github.io/thincarb/.*


##Legal Stuff

THINCARB has been developed to be used, and perhaps even enhanced, by the water 
quality community, be they academic, government, or commercial. For that reason 
it has been given a permissive licence. Basically the only thing you are 
prevented from doing with THINCARB is selling it!

Please see the file LICENSE.txt for more details.
