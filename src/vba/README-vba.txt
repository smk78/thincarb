THINCARB-excel2010.xlsm

This is a Microsoft Excel Version 14.0 (Excel 2010) **macro-enabled** spreadsheet workbook containing a re-write of the original Neal et al (1998) Lotus 1-2-3 macro (see [1]) in Microsoft Visual Basic (VBA). This spreadsheet also extends the calculations to provide Total Dissolved Inorganic Carbon (DIC) concentrations[2].  

The input values of pH, Alkalinity and Temperature provided in workbook correspond to those in Table 5 in [1]. Click the 'CommandB' button to activate the macro and thus optimise the value of EpCO2 by minimising the Charge Balance. You may then compare the estimates of EpCO2 with those shown in Table 5.



THINCARB-macro.vb

This is a Microsoft Visual Basic source file containing the macro found in THINCARB-excel2010.xlsm. This file is provided for reference purposes only. It can be opened and read using Microsoft Visual Studio or any ASCII-compatible text editor.



REFERENCES

[1] 'An assessment of excess carbon dioxide partial pressures in natural waters based on pH and alkalinity measurements'. Colin Neal, W Alan House, Kevin Down. Science of the Total Environment. 210/211 (1998) 173-185.

[2] 'Inorganic carbon dominates total dissolved carbon concentrations and fluxes in British rivers: Application of the THINCARB model – Thermodynamic modelling of inorganic carbon in freshwaters'. Helen Jarvie, Stephen King, Colin Neal. Science of the Total Environment. 575 (2017) 496-512.



RELEASE NOTES

14-Jul-2017: Versions of THINCARB-excel2010.xlsm **prior** to v8 (see the bottom right corner of the grey text box to check) were computing an altitude-compensated EpCO2 value (Column L) but not actually implementing it in the calculation of the H2CO3 activity (Column Y). This is now fixed.

