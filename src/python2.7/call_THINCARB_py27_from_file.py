# call_THINCARB_py27_from_file.py
#
# (c)2015 S. King
#
# Example of how to run THINCARB_py27_math.py using input values stored in an external SPACE-DELIMITED file
# Run this module from the Python command shell or IDLE.
#
# A text file will be created containing all the input data and the computed values from the model
#
#NOTE: Remove all spaces from SITE names (if using SITE): convert to underscores.
#
# The length of time this script takes to process input records depends on the amount of optimisation
# required for each record; typically, however, a 64-bit quad-core 3GHz Windows PC should achieve
# between 1 and 20 records/second.

import time

# File containing the observations/readings
InputFilename="THINCARB_model_table5_test_data.txt"

# File to contain the model calculations
OutputFilename="THINCARB_model_results_from_calculation_FILE.txt"

# Required charge balance (usually 0.0 !)
targetvalue=0.0

# Acceptable deviation from required charge balance (ie, targetvalue +/- tolerance)
# NB: The model can become unreliable if tolerance is set too small - say <1.0E-08 - but it is unlikely that M would ever need to be
# determined with that precision!
tolerance=1.0E-8

#### NOW SCROLL DOWN TO THE SECTION 'NOW MATCH THE COLUMNS' ####

print 'Starting calculation at',(time.strftime("%d/%m/%Y")),(time.strftime("%H:%M:%S"))

from THINCARB_py27_math import MainRoutineMath

# Create the output file and write the column headings
fileout=open(OutputFilename,'w')
fileout.write('Site Date Time Alt_(m) pH Alk_(uEq/L) Temp_(degC) [Ca]_(mg/L) EpCO2_rough EpCO2_less_rough EpCO2_less_rough_incl_CO3 EpCO2_accurate EpCO2_accurate_corr_alt Charge_balance Total_[Ca]_(M/L) CaCO3_sat_(Log) k0_pCO2-H2CO3 k1_H2CO3-HCO3 k2_HCO3-CO3 k3_CaHCO3 k4_CaCO3(0) k5_Ca(OH) k6_H2O k7_CaCO3(SO) OH H2CO3 HCO3 CO3 Ca2+ CaHCO3 CaCO3 CaOH root(I) gamma1 gamma2 [HCO3-]_mM [CO32-]_mM [H2CO3]_mM [HCO3-]_mg/L [CO32-]_mg/L [H2CO3]_mg/L [C]_in_HCO3_mg/L [C]_in_CO3_mg/L [C]_in_H2CO3_mg/L Tot_DIC_mg/L DIC_HCO3_% DIC_CO3_% DIC_H2CO3_% Tot_DIC_%'+'\n')

numrows=0
# Open the input file
filein=open(InputFilename,'r')
# Loop as many times as there are rows of data in the input file, splitting each SPACE-DELIMITED value into a different column
for linein in filein:
	linein=linein.strip()
	columns=linein.split()


#### NOW MATCH THE COLUMNS ####
# INPUTS:
# SITE = Location
#    A = Date
#    B = Time
#    C = Altitude (m)
#    D = pH
#    E = Alkalinity (uEq/L)
#    F = Temperature (degC)
#    G = [Ca] (mg/L)
# Modify the variables on the LHS of the following statements to match the file contents (column ordering)
# Add or remove these statements as necessary
# NB: Beware! Python lists index at [0] and not [1]!
	SITE=columns[0]
	A=columns[1]
	B=columns[2]
	D=float(columns[3])
	E=float(columns[4])
	F=float(columns[5])
# And then insert any defaults for missing values; NB: use floating point numbers not integers!
	C=0.0
	G=0.0
#### END OF COLUMN MATCHING ####


#### DO NOT CHANGE ANYTHING BELOW HERE ####
# Whatever happens MainRoutineMath must be called with values for fileout, targetvalue, tolerance, A, B, C, D, E, F and G!
	MainRoutineMath(fileout,targetvalue,tolerance,SITE,A,B,C,D,E,F,G)
	numrows=numrows+1
# Report progress along the way! (% is the Python modulo operator)
	if (numrows%100==0):
		print 'Processed', numrows, 'readings so far at ', (time.strftime("%H:%M:%S"))

# Close the output file
fileout.close()
# Close the input file
filein.close()

print 'Processed',numrows,'readings in total'
print 'Finishing calculation at',(time.strftime("%d/%m/%Y")),(time.strftime("%H:%M:%S"))
print ' '
print 'Done!'
print ' '

# END
