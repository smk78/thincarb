# THINCARB_py27_math.py
#
# (c)2015 S. King, H Jarvie & C Neal
#
# Calculates CO2 & CO3 saturation indices, CO2 partial pressures, and total dissolved inorganic carbon
# concentrations from hydrochemical data
#
# For the detail behind the calculations, see C. Neal, A. House & K. Down, Sci. Tot. Env. 211 (1998) 173-185  
#
# This version of THINCARB replaces the Python '**' operator for exponentiation & square root with math.pow() & math.sqrt()

import math

def MainRoutineMath(fileout,targetvalue,tolerance,SITE,A,B,C,D,E,F,G):
# INPUTS:
#       fileout = Name of text file to contain results
#   targetvalue = Desired value of M (usually 0.0 !)
#     tolerance = Acceptable deviation from targetvalue; ie, M +/- tolerance

# SITE = Location
#    A = Date
#    B = Time
#
#    C = Altitude (m)
#    D = pH
#    E = Alkalinity (uEq/L)
#    F = Temperature (degC)
#    G = [Ca] (mg/L)
#
# OUTPUTS:
#    Ep is the excess partial pressure
#    k is an equilibrum constant
#    DIC is dissolved inorganic carbon
#
#    H = EpCO2 rough
#    I = EpCO2 less rough
#    J = EpCO2 less rough including CO3
#    K = EpCO2 accurate {NB: this returned by optimisation}
#    L = EpCO2 accurate {corrected for altitude}
#    M = Charge balance
#    N = Total [Ca] (M/L)
#    O = CaCO3 saturation (Log)
#    P = k0 pCO2-H2CO3
#    Q = k1 H2CO3-HCO3
#    R = k2 HCO3-CO3
#    S = k3 CaHCO3
#    T = k4 CaCO3(0)
#    U = k5 Ca(OH)
#    V = k6 H2O
#    W = k7 CaCO3(SO)
#    X = OH activity
#    Y = H2CO3 activity
#    Z = HCO3 activity
#   AA = CO3 activity
#   AB = Ca2+ activity
#   AC = CaHCO3 activity
#   AD = CaCO3 activity
#   AE = CaOH activity
#   AF = root(ionic strength)
#   AG = gamma1 (1-) activity coefficient
#   AH = gamma2 (2-) activity coefficient
#   AI = (HCO3)- concentration (mM)
#   AJ = (CO3)2- concentration (mM)
#   AK = (H2CO3) concentration (mM)
#   AL = (HCO3)- concentration (mg/L)
#   AM = (CO3)2- concentration (mg/L)
#   AN = (H2CO3) concentration (mg/L)
#   AO = concentration of C in (HCO3)- (mg/L)
#   AP = concentration of C in (CO3)2- (mg/L)
#   AQ = concentration of C in (H2CO3) (mg/L)
#   AR = Total DIC (mg/L)
#   AS = DIC as HCO3 (%)
#   AT = DIC as CO3 (%)
#   AU = DIC as H2CO3 (%)
#   AV = Total DIC (%)

# Initialising value for M
	M=1000.0

# The following hydrochemical estimates are dependent only on the given inputs
#	H =(E+(10.0**(6.0-D)))*(10.0**(6.0-D))/5.25
	H =(E+math.pow(10.0,(6.0-D)))*math.pow(10.0,(6.0-D))/5.25
#	I =((0.95*E)+(10.0**(6.0-D)))*(10.0**(6.0-D))/(6.46-(0.0636*F))
	I =((0.95*E)+math.pow(10.0,(6.0-D)))*math.pow(10.0,(6.0-D))/(6.46-(0.0636*F))
	N =(G/40000.0)
#	P =10.0**-(13.417-(2299.6/(273.0+F))-(0.01422*(273.0+F)))
	P =math.pow(10.0,-(13.417-(2299.6/(273.0+F))-(0.01422*(273.0+F))))
#	Q =10.0**(-(-14.8345+(3404.71/(273.0+F))+(0.03279*(273.0+F))))
	Q =math.pow(10.0,(-(-14.8345+(3404.71/(273.0+F))+(0.03279*(273.0+F)))))
#	R =10.0**(-(-6.498+(2902.39/(273.0+F))+(0.02379*(273.0+F))))
	R =math.pow(10.0,(-(-6.498+(2902.39/(273.0+F))+(0.02379*(273.0+F)))))
#	S =10.0**-(-2.95+(0.0133*(273.0+F)))
	S =math.pow(10.0,-(-2.95+(0.0133*(273.0+F))))
#	T =10.0**(-(-27.393+(4114.0/(273.0+F))+(0.0561*(273.0+F))))
	T =math.pow(10.0,(-(-27.393+(4114.0/(273.0+F))+(0.0561*(273.0+F)))))
#	U =10.0**-1.4
	U =math.pow(10.0,-1.4)
#	V =10.0**-(-6.0846+(4471.33/(273.0+F))+(0.017053*(273.0+F)))
	V =math.pow(10.0,-(-6.0846+(4471.33/(273.0+F))+(0.017053*(273.0+F))))
#	W =10.0**-(-13.543+(3000.0/(273.0+F))+0.0401*(273.0+F))
	W =math.pow(10.0,-(-13.543+(3000.0/(273.0+F))+0.0401*(273.0+F)))
#	X =V/10.0**-D
	X =V/math.pow(10.0,-D)
#	J =( \
#       (0.95*E)+ \
#       ((10.0**(6.0-D))/0.95)+ \
#       ((10.0**(D+6.0+math.log10(V)))/0.95) \
#       )* \
#       (10.0**(6.0-D))/ \
#       ( \
#       (6.46-(0.0636*F))* \
#       (1.0+ \
#       (2.0*(0.95/0.8)*10.0**(D+math.log10(R)))) \
#       )
	J =( \
       (0.95*E)+ \
       (math.pow(10.0,(6.0-D))/0.95)+ \
       (math.pow(10.0,(D+6.0+math.log10(V)))/0.95) \
       )* \
       math.pow(10.0,(6.0-D))/ \
       ( \
       (6.46-(0.0636*F))* \
       (1.0+ \
       (2.0*(0.95/0.8)*math.pow(10.0,(D+math.log10(R))))) \
       )

# Initialise K
	K=J

# Now iterate on K to minimise M
# Uses a simple brute-force bisection algorithm which changes K by deltaK on each iteration
# NB: This can become unreliable if tolerance is set too small - say <1.0E-08 - but it is unlikely that M would ever need to be 
# determined with that precision!
	while ((M>(targetvalue+tolerance)) or (M<(targetvalue-tolerance))):
		deltaK=(targetvalue+K)/2.0

# The following hydrochemical estimates are dependent on K
#		Y =P*(10.0**-3.5)*K
		Y =P*math.pow(10.0,-3.5)*K
#		Z =Q*Y/(10.0**-D)
		Z =Q*Y/math.pow(10.0,-D)
#		AA=R*Z/(10.0**-D)
		AA=R*Z/math.pow(10.0,-D)
#		AF=(((20.0/35450.0)+X+Z+(10.0**-D)+(4.0*(AA+N)))/2.0)**0.5
		AF=math.sqrt(((20.0/35450.0)+X+Z+math.pow(10.0,-D)+(4.0*(AA+N)))/2.0)
#		AG=10.0**-(0.5*((AF/(1+AF))-(0.3*AF)))
		AG=math.pow(10.0,-(0.5*((AF/(1+AF))-(0.3*AF))))
#		AH=10.0**-(0.5*4.0*((AF/(1.0+AF))-(0.3*AF)))
		AH=math.pow(10.0,-(0.5*4.0*((AF/(1.0+AF))-(0.3*AF))))
		AB=N/((1.0+(Z*S/AG)+(AA*T/AG)+(U*X/AG)))
		AC=S*AB*Z
		AD=T*AB*AA
		AE=U*X*AB
# DIC calculations
		AI=1000.0*(Z/AG)
		AJ=1000.0*(AA/AH)
		AK=1000.0*Y
		AL=AI*61.0
		AM=AJ*60.0
		AN=AK*62.0
		AO=(12.0/61.0)*AL
		AP=(12.0/60.0)*AM
		AQ=(12.0/62.0)*AN
		AR=AO+AP+AQ
		AS=(AO/AR)*100.0
		AT=(AP/AR)*100.0
		AU=(AQ/AR)*100.0
		AV=AS+AT+AU

# Trap cases where N=0
		if (N==0.0):
			O=float('NaN')
		else:
			O=math.log10(AA*AB)-math.log10(W)

#		M =(E*(10.0**-6.0))+((10.0**-D)/AG)-(Z/AG)-(2.0*AA/AH)-(AC/AG)-(2.0*AD/1.0)-(X/AG)-(AE/AG)
		M =(E*math.pow(10.0,-6.0))+(math.pow(10.0,-D)/AG)-(Z/AG)-(2.0*AA/AH)-(AC/AG)-(2.0*AD/1.0)-(X/AG)-(AE/AG)

# Decide which way to adjust K and set a flag to remember it
		lastchange=0
		if (M<(targetvalue-tolerance)):
			K=K-deltaK
			lastchange=-1
		else:
			K=K+deltaK
			lastchange=1

# Correct K for the adjustment made right before the While loop exited
	if (lastchange==-1):
		K=K+deltaK
	else:
		K=K-deltaK

# Correct K for altitude (Note: this is a correction of the original correction in Neal 1998 from xPs/P0 to xP0/Ps)
#	L =K*((288.0-0.0065*C)/288.0)**(-5.256)
	L =K*math.pow(((288.0-0.0065*C)/288.0),-5.256)

#	print SITE,A,B,'%.1f'%C,'%.1f'%D,'%.1f'%E,'%.1f'%F,'%.2f'%G,'%.3f'%H,'%.3f'%I,'%.3f'%J,'%.3f'%K,'%.3f'%L,'%.1e'%M,'%.3e'%N, \
#    '%.3f'%O,'%.3e'%P,'%.3e'%Q,'%.3e'%R,'%.3e'%S,'%.3e'%T,'%.3e'%U,'%.3e'%V,'%.3e'%W,'%.3e'%X,'%.3e'%Y,'%.3e'%Z,'%.3e'%AA, \
#    '%.3e'%AB,'%.3e'%AC,'%.3e'%AD,'%.2e'%AE,'%.2e'%AF,'%.3f'%AG,'%.3f'%AH,'%.2f'%AI,'%.2f'%AJ,'%.2f'%AK,'%.2f'%AL,'%.2f'%AM, \
#    '%.2f'%AN,'%.2f'%AO,'%.2f'%AP,'%.2f'%AQ,'%.2f'%AR,'%.1f'%AS,'%.1f'%AT,'%.1f'%AU,'%.1f'%AV
#	print ' '

# Output the original input data AND the computed hydrochemical estimates to a file
	fileout.write(str(SITE)+' '+str(A)+' '+str(B)+' '+str('%.1f'%C)+' '+str('%.2f'%D)+' '+str('%.2f'%E)+' '+str('%.1f'%F)+' '+str('%.2f'%G)+' '+ \
    str('%.3f'%H)+' '+str('%.3f'%I)+' '+str('%.3f'%J)+' '+str('%.3f'%K)+' '+str('%.3f'%L)+' '+str('%.1e'%M)+' '+str('%.3e'%N)+' '+ \
    str('%.3f'%O)+' '+str('%.3e'%P)+' '+str('%.3e'%Q)+' '+str('%.3e'%R)+' '+str('%.3e'%S)+' '+str('%.3e'%T)+' '+str('%.3e'%U)+' '+ \
    str('%.3e'%V)+' '+str('%.3e'%W)+' '+str('%.3e'%X)+' '+str('%.3e'%Y)+' '+str('%.3e'%Z)+' '+str('%.3e'%AA)+' '+str('%.3e'%AB)+' '+ \
    str('%.3e'%AC)+' '+str('%.3e'%AD)+' '+str('%.3e'%AE)+' '+str('%.2e'%AF)+' '+str('%.3f'%AG)+' '+str('%.3f'%AH)+' '+ \
    str('%.2f'%AI)+' '+str('%.2f'%AJ)+' '+str('%.2f'%AK)+' '+str('%.2f'%AL)+' '+str('%.2f'%AM)+' '+str('%.2f'%AN)+' '+ \
    str('%.2f'%AO)+' '+str('%.2f'%AP)+' '+str('%.2f'%AQ)+' '+str('%.2f'%AR)+' '+str('%.1f'%AS)+' '+str('%.1f'%AT)+' '+ \
    str('%.1f'%AU)+' '+str('%.1f'%AV)+'\n')

# END
