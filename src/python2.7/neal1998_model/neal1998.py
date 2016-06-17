# neal1998.py
#
# (c)2015 S. King, H Jarvie & C Neal
#
# Calculates CO2 & CO3 saturation indices and CO2 partial pressures from hydrochemical data
#
# For the detail behind the calculations, see C. Neal, A. House & K. Down, Sci. Tot. Env. 211 (1998) 173-185  


import math

def MainRoutine(fileout,targetvalue,tolerance,A,B,C,D,E,F,G):
# INPUTS:
#       fileout = Name of text file to contain results
#   targetvalue = Desired value of M (usually 0.0 !)
#     tolerance = Acceptable deviation from targetvalue; ie, M +/- tolerance

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
#    H = EpCO2 rough
#    I = EpCO2 less rough
#    J = EpCO2 less rough including CO3
#    K = EpCO2 accurate {NB: this returned by optimisation}
#    L = EpCO2 accurate corrected for altitude
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
#    X = OH
#    Y = H2CO3
#    Z = HCO3
#   AA = CO3
#   AB = Ca2+
#   AC = CaHCO3
#   AD = CaCO3
#   AE = CaOH
#   AF = root(I)
#   AG = gamma1
#   AH = gamma2

# Initialising value for M
	M=1000.0

# The following hydrochemical estimates are dependent only on the given inputs
	H =(E+(10.0**(6.0-D)))*(10.0**(6.0-D))/5.25
	I =((0.95*E)+(10.0**(6.0-D)))*(10.0**(6.0-D))/(6.46-(0.0636*F))
	N =(G/40000.0)
	P =10.0**-(13.417-(2299.6/(273.0+F))-(0.01422*(273.0+F)))
	Q =10.0**(-(-14.8345+(3404.71/(273.0+F))+(0.03279*(273.0+F))))
	R =10.0**(-(-6.498+(2902.39/(273.0+F))+(0.02379*(273.0+F))))
	S =10.0**-(-2.95+(0.0133*(273.0+F)))
	T =10.0**(-(-27.393+(4114.0/(273.0+F))+(0.0561*(273.0+F))))
	U =10.0**-1.4
	V =10.0**-(-6.0846+(4471.33/(273.0+F)+(0.017053*(273.0+F))))
	W =10.0**-(-13.543+(3000.0/(273.0+F)+0.0401*(273.0+F)))
	X =V/10.0**-D
	J =((0.95*E)+((10.0**(6.0-D))/0.95)+((10.0**(D+6.0+math.log10(V)))/0.95))*(10.0**(6.0-D))/((6.46-(0.0636*F))*(1.0+(2.0* \
       (0.95/0.8)*10.0**(D+math.log10(R)))))

# Initialise K
	K=J

# Now iterate on K to minimise M
# Uses a simple brute-force bisection algorithm which changes K by deltaK on each iteration
# NB: This can become unreliable if tolerance is set too small - say <1.0E-08 - but it is unlikely that M would ever need to be 
# determined with that precision!
	while ((M>(targetvalue+tolerance)) or (M<(targetvalue-tolerance))):
		deltaK=(targetvalue+K)/2.0

# The following hydrochemical estimates are dependent on K
		Y =P*(10.0**-3.5)*K
		Z =Q*Y/(10.0**-D)
		AA=R*Z/(10.0**-D)
		AF=(((20.0/35450.0)+X+Z+(10.0**-D)+(4.0*(AA+N)))/2.0)**0.5
		AG=10.0**-(0.5*((AF/(1+AF))-(0.3*AF)))
		AH=10.0**-(0.5*4.0*((AF/(1.0+AF))-(0.3*AF)))
		AB=N/((1.0+(Z*S/AG)+(AA*T/AG)+(U*X/AG)))
		AC=S*AB*Z
		AD=T*AB*AA
		AE=U*X*AB
# Trap cases where N=0
		if (N==0.0):
			O=float('NaN')
		else:
			O=math.log10(AA*AB)-math.log10(W)

		M =(E*(10.0**-6.0))+((10.0**-D)/AG)-(Z/AG)-(2.0*AA/AH)-(AC/AG)-(2.0*AD/1.0)-(X/AG)-(AE/AG)

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

# Correct K for altitude (Note: this is the original correction in Neal 1998, see Equations A-1a - A-1c)
	L =K*((288.0-0.0065*C)/288.0)**5.256

#	print A,B,'%.1f'%C,'%.1f'%D,'%.1f'%E,'%.1f'%F,'%.2f'%G,'%.3f'%H,'%.3f'%I,'%.3f'%J,'%.3f'%K,'%.3f'%L,'%.1e'%M,'%.3e'%N, \
#    '%.3f'%O,'%.3e'%P,'%.3e'%Q,'%.3e'%R,'%.3e'%S,'%.3e'%T,'%.3e'%U,'%.3e'%V,'%.3e'%W,'%.3e'%X,'%.3e'%Y,'%.3e'%Z,'%.3e'%AA, \
#    '%.3e'%AB,'%.3e'%AC,'%.3e'%AD,'%.2e'%AE,'%.2e'%AF,'%.3f'%AG,'%.3f'%AH
#	print ' '

# Output the original input data AND the computed hydrochemical estimates to a file
	fileout.write(str(A)+' '+str(B)+' '+str('%.1f'%C)+' '+str('%.1f'%D)+' '+str('%.1f'%E)+' '+str('%.1f'%F)+' '+str('%.2f'%G)+' '+ \
    str('%.3f'%H)+' '+str('%.3f'%I)+' '+str('%.3f'%J)+' '+str('%.3f'%K)+' '+str('%.3f'%L)+' '+str('%.1e'%M)+' '+str('%.3e'%N)+' '+ \
    str('%.3f'%O)+' '+str('%.3e'%P)+' '+str('%.3e'%Q)+' '+str('%.3e'%R)+' '+str('%.3e'%S)+' '+str('%.3e'%T)+' '+str('%.3e'%U)+' '+ \
    str('%.3e'%V)+' '+str('%.3e'%W)+' '+str('%.3e'%X)+' '+str('%.3e'%Y)+' '+str('%.3e'%Z)+' '+str('%.3e'%AA)+' '+ \
    str('%.3e'%AB)+' '+str('%.3e'%AC)+' '+str('%.3e'%AD)+' '+str('%.3e'%AE)+' '+str('%.2e'%AF)+' '+str('%.3f'%AG)+' '+ \
    str('%.3f'%AH)+'\n')

# END
