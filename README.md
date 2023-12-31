﻿#TODO update readme

# praca_inzynierska

---------------------------------------------POLISH----------------------------------------------------

Część projektowa z kodem znajduje się w folderze praca_inzynierska/scr/turbine. W celu dokonania obliczeń należy uruchmić plik main.py znajdujący się w tym folderze. 
W folderze turbine znajdują się foldery: 
- initial_turbine_settings (zawierający pliki z danymi wejściowymi do obliczeń, które można zmienić)
- airfoil_geometry (zawierający pliki dotyczące obliczeń związanych z wygenerowaniem profili łopatek)       podzielony na podfoldery:
    - dep_geometry_parameters (zwirający pliki do obliczeń parametrów zależnych geometrii)
    - geom_parameters (zawierający pliki do obliczeń związanych z geometrią łopatki)
- combustion_params (zawierający obliczenia kappy, R oraz cp)
- helpers (zawierający funkcje pomocnicze)
- turbine_input_data (zawierający wstępne obliczenia 2D dla wektorów stanu)
- turbine_3D (zawierający obliczenia związane z simple radial equilibrium)

W folderze praca_inzynierska/data/csv znajdują się pliki csv z danymi wejściowymi oraz wyjściowymi. 
Zawiera on podfoldery:
- check (zawierający pliki z danymi sprawdzającymi dla modelu RATD oraz SRE)
- interpolate_data (zawierający pliki z danymi do interpolacji pierszej wartości chord_t)

Do folderu praca_inzynierska/data/airfoils zapisywane są katalogi oznaczone numer stopnia+rotor/stator_data_godzina (na przykład: 1r_20231109_102018), w których znajdują się pliki blade_data_sheet.txt (wszystkie dane wejścowe i wyjściowe dla łopatki), pliki png z profilami łopatki dla róznych promieni oraz pliki wejściowe do TurboGrida. Katalog check zawiera dane sprawdzające dla modelu RATD. 

Kod opisujacy geometrię łopatki powstał na podstawie modelu RATD (Rapid Axial Turbine Design) autorstwa L. J. Pritcharda. Przyjmuje on wartości wartości 11 niezależnych parametrów oraz dla części z nich jest w stanie generować wartości domyślne/początkowe.
Wartości wejściowe:
- R - promień, na którym znajduje się profil łopatki (bez wartości początkowej)
- chord_x - cięciwa w kierunku osiowym (wartośc początkowa równa 0, obliczane w def_values z założenia zweifel_coefficient=0.8)
- chord_t - cięciwa w kierunku obwodowym (generowanie wartości początkowej opisane poniżej*)
- ugt - unguided turning angle (wartość ustawiana w initial_turbine_settings, bez wartości początkowej)
- beta_in - kąt wlotowy łopatki (wartość na podstawie obliczeń termodynamicznych)
- beta_out - kąt wylotowy łopatki (wartość na podstawie obliczeń termodynamicznych)
- half_wedge_in - (wartość ustawiana w initial_turbine_settings, bez wartości początkowej)
- Rle - promień krawędzi natarcia (wartość początkowa to ułamek pitch, wartość ustawiana w initial_turbine_settings)
- Rte - promień krawędzi sływu (wartość początkowa to ułamek cięciwy, wartość ustawiana w initial_turbine_settings)
- Nb - liczba łopatek (wartość ustawiana w initial_turbine_settings, bez wartości początkowej)
- throat - (wartośc początkowa równa 0, obliczane w def_values)

Dodatkowy 12 parametr (zależny od pozostałych 11)
- half_wedge_out - (wartość początkowa ugt/2, przeliczana w remove_throat_discontinuity)

*Generowanie wartości początkowej dla chord_t: 

---------------------------------------------ENGLISH----------------------------------------------------

The part of project with the code can be found in the folder praca_inzynierska/scr/turbine. To perform calculations, run the main.py file located in this folder. 
The turbine folder contains the folders: 
- initial_turbine_settings (containing files with input data for calculations that can be changed)
- airfoil_geometry (containing files for calculations related to the generation of blade profiles) divided into subfolders:
    - dep_geometry_parameters (containing files for calculations of dependent geometry parameters)
    - geom_parameters (containing files for calculations related to blade geometry)
- combustion_params (containing kappa, R and cp calculations)
- helpers (containing helper functions)
- turbine_input_data (containing initial 2D calculations for state vectors)
- turbine_3D (containing calculations related to simple radial equilibrium)

The praca_inzynierska/data/csv folder contains csv files with input and output data. 
It contains subfolders:
- check (containing check data files for the RATD and SRE model)
- interpolate_data (containing data files for interpolating the first chord_t value)

Directories labeled degree number+rotor/stator_date_time (for example: 1r_20231109_102018) are written to the praca_inzynierska/data/airfoils folder, which contains blade_data_sheet.txt files (all input and output data for the blade), png files with blade profiles for different radii, and TurboGrid input files. The check directory contains check data for the RATD model. 

The code describing the blade geometry is based on the Rapid Axial Turbine Design (RATD) model by L. J. Pritchard. It accepts values of 11 independent parameters and for some of them is able to generate default/initial values.
Input values:
- R - the radius at which the blade profile is located (no initial value)
- chord_x - chord in the axial direction (initial value equal to 0, calculated in def_values with the assumption zweifel_coefficient=0.8)
- chord_t - chord in tangential direction (initial value generation described below*)
- ugt - unguided turning angle (value set in initial_turbine_settings, no initial value)
- beta_in - blade inlet angle (value based on thermodynamic calculations)
- beta_out - blade exit angle (value based on thermodynamic calculations)
- half_wedge_in - (value set in initial_turbine_settings, no initial value)
- Rle - leading edge radius (initial value is a fraction of pitch, value set in initial_turbine_settings)
- Rte - the radius of the edge of the slab (initial value is a fraction of the chord, value set in initial_turbine_settings)
- Nb - number of blades (value set in initial_turbine_settings, no initial value)
- throat - (initial value equal to 0, calculated in def_values)

Additional 12 parameter (dependent on the other 11)
- half_wedge_out - (initial value ugt/2, recalculated in remove_throat_discontinuity)

*Generates initial value for chord_t:
