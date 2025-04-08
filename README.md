# praca_inzynierska -> Bachelor Thesis:
### Abstract:
This thesis paper presents the creation of a stage design for an axial turbine using Python programming language, Ansys TurboGrid, Ansys Fluent and ParaView software. The mentioned processes included generating the geometry, preparing a domain mesh, conducting a numerical analysis, and visualising and studying the results. The geometry model has been based on the model created by L. J. Pritchard called Rapid Axial Turbine Desing (RATD). The original FORTRAN code has been rewritten into Python programming language, and some improvements have been incorporated to suit the project better. For all the prepared geometries structural grids have been generated using the TurboGrid software. Then, a CFD numerical analysis of the five most promising cases with different geometries based on the general assumptions has been performed to obtain the best result. Finally, the finest geometry model has been chosen, and its flow phenomena have been examined.

### Code Structure
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

### Code Flow and Conceptual Overview
![image](https://github.com/user-attachments/assets/5721288b-6523-40a5-b485-ffe32e31a4b3)

As mentioned, all the calculations and geometry generation have been written in a Python project. Beyond the Python standard library, it uses NumPy, Pandas, Matplotlib and SciPy. The general flow of the program can be seen in the figure above. This program has been based on the Fortran code from Pritchard’s article (https://doi.org/10.1115/85-GT-219). However, changes have been made to adapt the code flow to this project. The main additions include:
- thermodynamic calculation for the mean radius
- improved default values generation for eleven input parameters
- generation of multiple airfoils (using SRE equations) for one blade
- generation of both stator and rotor airfoils in one program run
- generation of TurboGrid input files
- generation of additional output files

From the user’s perspective, the program is straightforward. They’re given two files with initial settings for the turbine - one for thermodynamics calculations and one for the geometry. All of the data in there should be set for mean radius parameters. In the first one, the user can set the values of parameters for two essential classes: turbine_input and turbine_assum. The first one contains data for the engine, such as turbine inlet temperature and pressure, mass flow, total pressure ratio, isentropic efficiency, and rotational speed. Therefore, the part of input data that will not be changed in the project. The second one, turbine_assum, contains data like blade angles, flow coefficient, axial velocity or rotor blade loss.
That data can be changed to achieve a different blade geometry. The file with input geometry parameters allows the user to change some of the 11 parameters for geometry RATD modelling and the method by which the default value for tangential chord should be derived. The user can also set the number of profiles from which the 3D model is created, the number of points that generate each airfoil, or the values of the gap between the rotor and stator. There is also an option to omit the shift of the rotor in regard to the stator if the user wants to do that part in the simulation software. After all those parameters are set, the user only has to run the program. It will create output files that can be used for TurboGrid meshing software and to check if the geometry is satisfying in terms of flow parameters. 

However, the most crucial part is what happens during the program run. As shown in the figure above, the thermodynamic calculation for mean radius is first made. That way, tangential and axial velocity values and static temperatures and pressures are obtained for all stage stations at the mean radius. Next, the simple radial equilibrium is used on the rotor to obtain the inlet and outlet blade angles for each radius. The outlet blade angle for the stator is considered equal to the rotor inlet blade angle, while the inlet stator angle is considered constant and can be set in the initial settings file.

In the next stage, two CSV files are generated, each containing values for 11 parameters corresponding to different radii, with one file designated for the rotor and the other for the stator. Some of these values are the initial values, i.e., that would trigger the conditions to generate the default values of those parameters. The rest is considered equal to those parameters’ final values. Additionally, the first guess values of the
half wedge out angle are calculated, as they would be essential for creating geometry.

The following steps are placed inside a loop, ensuring that the stator and rotor will be generated in one program run. Inside that loop is an additional one that ensures the process will happen for all the radii so the 3D model can be created. The first step is to generate the values for 5 points and five slopes that make a profile. It is essential to mention that slopes are generated in the form of n number of points, including the five main points generated at the start. A check is conducted to see if there is a throat discontinuity. If so, the value of the half wedge angle is recalculated, and the points and slopes are generated again. That process happens until the throat discontinuity is removed. After that, the value of the tangential chord is recalculated based on the method chosen in the initial settings. Another check is conducted to see if the value of the tangential chord falls within the conditions. If not, the process comes back to the point of generating the 5 points and slopes. After the satisfying value is obtained, points and slopes are calculated for the last time. This would be the data that is saved in output files. This process executes for each radius of the rotor and stator.

The output data consists of many different types of files. The most important ones are init and curve files for TurboGrid software. They let the 
user open the model in TurboGrid and create a mesh from it. The program also creates text files with blade input data for the stator and rotor to simplify the process of generating the same geometry again. There are also plots with parameter distribution for different radii and plots with blade airfoil profiles for each radii of the stator and rotor. On top of that, the output data folder includes CSV files with values of dependent parameters that can be derived from 11 input parameters. To ensure that the output data will not be overwritten, the name of the output folder consists of the date and time the program was started and the word gap if the rotor is shifted in the axial direction. An example folder name would be turbine_stage_20231219_221409_gap.
