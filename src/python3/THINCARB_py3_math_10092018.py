# THINCARB_py3_math.py
#
# (c)2015 S. King, H Jarvie & C Neal (Sci. Tot. Env. 575 (2017) 496-512)
#
# Calculates CO2 & CO3 saturation indices, CO2 partial pressures, and total dissolved inorganic carbon
# concentrations from hydrochemical data
#
# For the detail behind the calculations, see C. Neal, A. House & K. Down, Sci. Tot. Env. 211 (1998) 173-185  
#
# This version of THINCARB replaces the Python '**' operator for exponentiation & square root with math.pow() & math.sqrt()
#
# This version of THINCARB includes the DIC contribution from CaHCO3+ and CaCO3
#
# 14-Jul-2017: Altitude-corrected EpCO2 now properly applied to calculation of H2CO3 activity
#
# 13-Mar-2018: Trap AX=0 by catching ever decreasing M when alkalinity is near zero

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
#    U = k5 CaOH
#    V = k6 H2O
#    W = k7 CaCO3(SO)
#    X = OH activity
#    Y = H2CO3 activity
#    Z = HCO3 activity
#   AA = CO3 activity
#   AB = Ca2+ activity
#   AC = CaHCO3+ activity
#   AD = CaCO3 activity
#   AE = CaOH- activity
#   AF = root(ionic strength)
#   AG = gamma1 (1-) activity coefficient
#   AH = gamma2 (2-) activity coefficient
#   AI = (HCO3)- concentration (mM)
#   AJ = (CO3)2- concentration (mM)
#   AK = (H2CO3) concentration (mM)
#   AL = (HCO3)- concentration (mM) in (CaHCO3)+ 
#   AM = (CO3)2- concentration (mM) in (CaCO3)
#   AN = (HCO3)- concentration (mg/L)
#   AO = (CO3)2- concentration (mg/L)
#   AP = (H2CO3) concentration (mg/L)
#   AQ = (HCO3)- concentration (mg/L) in (CaHCO3)+ 
#   AR = (CO3)2- concentration (mg/L) in (CaCO3)
#   AS = concentration of C in (HCO3)- (mg/L)
#   AT = concentration of C in (CO3)2- (mg/L)
#   AU = concentration of C in (H2CO3) (mg/L)
#   AV = concentration of C in (HCO3)- (mg/L) in (CaHCO3)+
#   AW = concentration of C in (CO3)2- (mg/L) in (CaCO3)
#   AX = Total DIC (mg/L)
#   AY = DIC as HCO3 (%)
#   AZ = DIC as CO3 (%)
#   BA = DIC as H2CO3 (%)
#   BB = DIC as HCO3 (%) in (CaHCO3)+
#   BC = DIC as CO3 (%) in (CaCO3)
#   BD = Total DIC (%)

# Initialising value for M
	M=1000.0
	lastM=999.0

# The following hydrochemical estimates are dependent only on the given inputs
	H =(E+math.pow(10.0,(6.0-D)))*math.pow(10.0,(6.0-D))/5.25
	I =((0.95*E)+math.pow(10.0,(6.0-D)))*math.pow(10.0,(6.0-D))/(6.46-(0.0636*F))
	N =(G/40000.0)
	P =math.pow(10.0,-(13.417-(2299.6/(273.0+F))-(0.01422*(273.0+F))))
	Q =math.pow(10.0,(-(-14.8345+(3404.71/(273.0+F))+(0.03279*(273.0+F)))))
	R =math.pow(10.0,(-(-6.498+(2902.39/(273.0+F))+(0.02379*(273.0+F)))))
	S =math.pow(10.0,-(-2.95+(0.0133*(273.0+F))))
	T =math.pow(10.0,(-(-27.393+(4114.0/(273.0+F))+(0.0561*(273.0+F)))))
	U =math.pow(10.0,-1.4)
	V =math.pow(10.0,-(-6.0846+(4471.33/(273.0+F))+(0.017053*(273.0+F))))
	W =math.pow(10.0,-(-13.543+(3000.0/(273.0+F))+0.0401*(273.0+F)))
	X =V/math.pow(10.0,-D)
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

#	while ((M>(targetvalue+tolerance)) or (M<(targetvalue-tolerance))):
	while (((M>(targetvalue+tolerance)) or (M<(targetvalue-tolerance))) and (M!=lastM)):
		deltaK=(targetvalue+K)/2.0

# Correct K for altitude (Note: this is a correction of the original correction in Neal 1998 from xPs/P0 to xP0/Ps)
		L =K*math.pow(((288.0-0.0065*C)/288.0),-5.256)

# The following hydrochemical estimates are dependent on K
#		Y =P*math.pow(10.0,-3.5)*K
		Y =P*math.pow(10.0,-3.5)*L
		Z =Q*Y/math.pow(10.0,-D)
		AA=R*Z/math.pow(10.0,-D)
		AF=math.sqrt(((20.0/35450.0)+X+Z+math.pow(10.0,-D)+(4.0*(AA+N)))/2.0)
		AG=math.pow(10.0,-(0.5*((AF/(1+AF))-(0.3*AF))))
		AH=math.pow(10.0,-(0.5*4.0*((AF/(1.0+AF))-(0.3*AF))))
		AB=N/((1.0+(Z*S/AG)+(AA*T/AG)+(U*X/AG)))
		AC=S*AB*Z
		AD=T*AB*AA
		AE=U*X*AB
# DIC calculations
		AI=1000.0*(Z/AG)
		AJ=1000.0*(AA/AH)
		AK=1000.0*Y
		AL=1000.0*(AC/AG)
		AM=1000.0*(AD/AH)
		AN=AI*61.0
		AO=AJ*60.0
		AP=AK*62.0
		AQ=AL*61.0
		AR=AM*60.0
		AS=(12.0/61.0)*AN
		AT=(12.0/60.0)*AO
		AU=(12.0/62.0)*AP
		AV=(12.0/61.0)*AQ
		AW=(12.0/60.0)*AR
		AX=AS+AT+AU+AV+AW
		AY=(AS/AX)*100.0
		AZ=(AT/AX)*100.0
		BA=(AU/AX)*100.0
		BB=(AV/AX)*100.0
		BC=(AW/AX)*100.0
		BD=AY+AZ+BA+BB+BC

# Trap cases where N=0
		if (N==0.0):
			O=float('NaN')
		else:
			O=math.log10(AA*AB)-math.log10(W)

		lastM=M
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

# Output the original input data AND the computed hydrochemical estimates to the terminal
#	print (SITE,A,B,'%.1f'%C,'%.1f'%D,'%.1f'%E,'%.1f'%F,'%.2f'%G,'%.3f'%H,'%.3f'%I,'%.3f'%J,'%.3f'%K,'%.3f'%L,'%.1e'%M,'%.3e'%N, \
#    '%.3f'%O,'%.3e'%P,'%.3e'%Q,'%.3e'%R,'%.3e'%S,'%.3e'%T,'%.3e'%U,'%.3e'%V,'%.3e'%W,'%.3e'%X,'%.3e'%Y,'%.3e'%Z,'%.3e'%AA, \
#    '%.3e'%AB,'%.3e'%AC,'%.3e'%AD,'%.2e'%AE,'%.2e'%AF,'%.3f'%AG,'%.3f'%AH,'%.2f'%AI,'%.2f'%AJ,'%.2f'%AK,'%.2f'%AL,'%.2f'%AM, \
#    '%.2f'%AN,'%.2f'%AO,'%.2f'%AP,'%.2f'%AQ,'%.2f'%AR,'%.2f'%AS,'%.2f'%AT,'%.2f'%AU,'%.2f'%AV,'%.2f'%AW,'%.2f'%AX,'%.1f'%AY, \
#    '%.1f'%AZ,'%.1f'%BA,'%.2f'%BB,'%.2f'%BC,'%.1f'%BD)
#	print (' ')

# Output the original input data AND the computed hydrochemical estimates to a file
	fileout.write(str(SITE)+' '+str(A)+' '+str(B)+' '+str('%.1f'%C)+' '+str('%.2f'%D)+' '+str('%.2f'%E)+' '+str('%.1f'%F)+' '+str('%.2f'%G)+' '+ \
    str('%.3f'%H)+' '+str('%.3f'%I)+' '+str('%.3f'%J)+' '+str('%.3f'%K)+' '+str('%.3f'%L)+' '+str('%.1e'%M)+' '+str('%.3e'%N)+' '+ \
    str('%.3f'%O)+' '+str('%.3e'%P)+' '+str('%.3e'%Q)+' '+str('%.3e'%R)+' '+str('%.3e'%S)+' '+str('%.3e'%T)+' '+str('%.3e'%U)+' '+ \
    str('%.3e'%V)+' '+str('%.3e'%W)+' '+str('%.3e'%X)+' '+str('%.3e'%Y)+' '+str('%.3e'%Z)+' '+str('%.3e'%AA)+' '+str('%.3e'%AB)+' '+ \
    str('%.3e'%AC)+' '+str('%.3e'%AD)+' '+str('%.3e'%AE)+' '+str('%.2e'%AF)+' '+str('%.3f'%AG)+' '+str('%.3f'%AH)+' '+ \
    str('%.2f'%AI)+' '+str('%.2f'%AJ)+' '+str('%.2f'%AK)+' '+str('%.2f'%AL)+' '+str('%.2f'%AM)+' '+str('%.2f'%AN)+' '+ \
    str('%.2f'%AO)+' '+str('%.2f'%AP)+' '+str('%.2f'%AQ)+' '+str('%.2f'%AR)+' '+str('%.2f'%AS)+' '+str('%.2f'%AT)+' '+ \
    str('%.2f'%AU)+' '+str('%.2f'%AV)+' '+str('%.2f'%AW)+' '+str('%.2f'%AX)+' '+str('%.1f'%AY)+' '+str('%.1f'%AZ)+' '+ \
    str('%.1f'%BA)+' '+str('%.2f'%BB)+' '+str('%.2f'%BC)+' '+str('%.1f'%BD)+'\n')

# END
