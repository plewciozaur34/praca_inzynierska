#TODO update readme

# praca_inzynierska

Część projektowa z kodem znajduje się w folderze praca_inzynierska/scr/turbine. W celu dokonania obliczeń należy uruchmić plik main.py znajdujący się w tym folderze. 
W folderze turbine znajdują się foldery: 
- airfoil_geometry (zawierający pliki dotyczące obliczeń związanych z wygenerowaniem profili łopatek)       podzielony na podfoldery:
    - dep_geometry_parameters (zwirający pliki do obliczeń parametrów zalezych geometrii)
    - geom_parameters (zawierający pliki do obliczeń związanych z geometrią łopatki)
- combustion_params (zawierający obliczenia kappy, R oraz cp)
- helpers (zawierający funkcje pomocnicze)
- turbine_input_data (zawierający wstępne obliczenia 2D dla wektorów stanu)
- turbine_3D (zawierający obliczenia związane z simple radial equilibrium)

W folderze praca_inzynierska/data/csv znajdują się pliki csv z danymi wejściowymi oraz wyjściowymi. 
W folderze praca_inzynierska/data/airfoils znajdowac się będą gotowe wykresy z geometriami łopatek.

Kod opisujacy geometrię łopatki powstał na podstawie modelu RATD (Rapid Axial Turbine Design) autorstwa L. J. Pritcharda. Przyjmuje on wartości wartości 11 niezależnych parametrów oraz dla części z nich jest w stanie generować wartości domyślne/początkowe.
Wartości wejściowe:
- R - promień, na którym znajduje się profil łopatki
- chord_x
- chord_t
- ugt
- beta_in
- beta_out
- half_wedge_in
- Rle
- Rte
- Nb
- throat

Dodatkowy 12 parametr (zależny od pozostałych 11)
- half_wedge_out

!! UWAGA !!
Jeśli program zostanie odpalony w ciągu 1min od poprzedniego uruchomienia, może pojawic się problem z zapisem profili (zostaną zapisane do starego folderu z profilami). Jeśli zmieniane są dane wejściowe, musi minąć 1min między uruchomieniami programu.
