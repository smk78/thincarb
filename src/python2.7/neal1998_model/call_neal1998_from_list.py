# call_neal1998_from_list.py
#
# (c)2015 S. King, STFC RAL
#
# Example of how to run neal1998.py using input values stored in Python lists
# Run this module from the Python command shell or IDLE.
#
# A text file will be created containing all the input data and the computed values from the model


##### ENTER YOUR OBSERVATIONS/READINGS HERE #####
# All inputs are required; NB: use dummy values for missing data (eg, set the Altitude to 0 m if unknown)
# Use comma-separated lists of input values; NB: use floating point values, not integers!
# Ensure each list has the same number of values!
#
# As a minimum the model requires pH (D) and Alkalinity (E) to compute anything of use!
#
# INPUTS:
#    A = Date
#    B = Time
#    C = Altitude (m)
#    D = pH
#    E = Alkalinity (uEq/L)
#    F = Temperature (degC)
#    G = [Ca] (mg/L)

# These test data are from Neal et al (see above), Table 5. A, B, C and G are dummy values.
inputA=['09/09/14','09/09/14','09/09/14','09/09/14','09/09/14','09/09/14','09/09/14','09/09/14','09/09/14','09/09/14']
inputB=['09:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00','17:00','18:00']
inputC=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
inputD=[8.29,8.38,8.21,8.31,8.24,8.42,8.32,8.17,8.01,8.20]
inputE=[3930.0,3880.0,3970.0,4010.0,3850.0,3890.0,3940.0,3930.0,3680.0,3970.0]
inputF=[12.2,10.6,13.6,18.0,16.6,15.2,17.0,17.8,16.6,15.3]
inputG=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

######### END OF OBSERVATIONS/READINGS ##########

# File to contain the model calculations
OutputFilename="neal1998_model_results_from_calculation_LIST.txt"

# Required charge balance (usually 0.0 !)
targetvalue=0.0

# Acceptable deviation from required charge balance (ie, targetvalue +/- tolerance)
# NB: The model can become unreliable if tolerance is set too small - say <1.0E-08 - but it is unlikely that M would ever need to be 
# determined with that precision!
tolerance=1.0E-8


#### DO NOT CHANGE ANYTHING BELOW HERE ####
from neal1998 import MainRoutine

# Create the output file and write the column headings
fileout=open(OutputFilename,"w")
fileout.write('Date Time Alt_(m) pH Alk_(uEq/L) Temp_(degC) [Ca]_(mg/L) EpCO2_rough EpCO2_less_rough EpCO2_less_rough_incl_CO3 EpCO2_accurate EpCO2_accurate_corr_alt Charge_balance Total_[Ca]_(M/L) CaCO3_sat_(Log) k0_pCO2-H2CO3 k1_H2CO3-HCO3 k2_HCO3-CO3 k3_CaHCO3 k4_CaCO3(0) k5_Ca(OH) k6_H2O k7_CaCO3(SO) OH H2CO3 HCO3 CO3 Ca2+ CaHCO3 CaCO3 CaOH root(I) gamma1 gamma2'+'\n')

# Loop as many times as there are input values for D (chosen because D & E are the minimum inputs that must be
# supplied for the calculation to do anything useful)
for row in range(0,len(inputD)):
	A=inputA[row]
	B=inputB[row]
	C=inputC[row]
	D=inputD[row]
	E=inputE[row]
	F=inputF[row]
	G=inputG[row]
	MainRoutine(fileout,targetvalue,tolerance,A,B,C,D,E,F,G)

# Close the output file
fileout.close()

print ' '
print 'Done!'
print 'Processed',len(inputD),'readings in total'
print ' '

# END
