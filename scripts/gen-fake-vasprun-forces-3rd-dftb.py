import numpy as np
import os
import re
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
# 三阶
# job-xxxx
# 3RD.POSCAR.xxxx
start_num = 1
end_num = 1000
def find_max_suffix_digits():
    pattern = re.compile(r'^3RD\.POSCAR\.(\d+)$')
    max_num = -1

    for fname in os.listdir('.'):
        if os.path.isfile(fname):
            match = pattern.match(fname)
            if match:
                num = int(match.group(1))
                if num > max_num:
                    max_num = num

    if max_num == -1:
        print("未找到匹配的文件")
        return None
    else:
        digits = len(str(max_num))
        print(f"最大后缀: {max_num}, 位数: {digits}")
        return digits

digit_num = find_max_suffix_digits()
for i in range(start_num, end_num+1): 
    Filename= os.path.join(os.path.abspath('./'),'3RD.POSCAR.'+str(i).zfill(digit_num))
    with open(Filename, 'r') as file:
        lines = file.readlines()
    eighth_line = lines[7].strip()
    seventh_line = lines[6].strip()
    if 'Direct' in eighth_line or 'Cartesian' in eighth_line:
        matrix_data = [list(map(float, lines[i].strip().split())) for i in range(2, 5)]
        latticeconstant = np.array(matrix_data)
        element_symbols = lines[5].strip().split()
        element_counts = list(map(int, lines[6].strip().split()))
        coordinates = [list(map(float, line.strip().split())) for line in lines[8:]]
        coordinates_array = np.array(coordinates)        
    if 'Direct' in seventh_line or 'Cartesian' in seventh_line:
        matrix_data = [list(map(float, lines[i].strip().split())) for i in range(2, 5)]
        latticeconstant = np.array(matrix_data)
        element_symbols = lines[0].strip().split()
        element_counts = list(map(int, lines[5].strip().split()))
        coordinates = [list(map(float, line.strip().split())) for line in lines[7:]]
        coordinates_array = np.array(coordinates)        
    element_names = {
        'H': 'Hydrogen',
        'He': 'Helium',
        'Li': 'Lithium',
        'Be': 'Beryllium',
        'B': 'Boron',
        'C': 'Carbon',
        'N': 'Nitrogen',
        'O': 'Oxygen',
        'F': 'Fluorine',
        'Ne': 'Neon',
        'Na': 'Sodium',
        'Mg': 'Magnesium',
        'Al': 'Aluminum',
        'Si': 'Silicon',
        'P': 'Phosphorus',
        'S': 'PeriodicTable.Sulfur',
        'Cl': 'Chlorine',
        'Ar': 'Argon',
        'K': 'Potassium',
        'Ca': 'Calcium',
        'Sc': 'Scandium',
        'Ti': 'Titanium',
        'V': 'Vanadium',
        'Cr': 'Chromium',
        'Mn': 'Manganese',
        'Fe': 'Iron',
        'Co': 'Cobalt',
        'Ni': 'Nickel',
        'Cu': 'Copper',
        'Zn': 'Zinc',
    }
    elements_list = []
    for symbol, count in zip(element_symbols, element_counts):
        name = element_names.get(symbol, symbol)
        elements_list.extend([name] * count)
  
    # -*- coding: utf-8 -*-
    # -------------------------------------------------------------
    # Bulk Configuration
    # -------------------------------------------------------------

    # Set up lattice
    lattice = SimpleOrthorhombic(latticeconstant[0,0]*Angstrom, latticeconstant[1,1]*Angstrom, latticeconstant[2,2]*Angstrom)

    # Define elements
    elements = [eval(name) for name in elements_list]


    # Define coordinates
    fractional_coordinates = coordinates_array

    # Set up configuration
    bulk_configuration = BulkConfiguration(
        bravais_lattice=lattice,
        elements=elements,
        fractional_coordinates=fractional_coordinates
        )
   
    # -------------------------------------------------------------
    # Calculator
    # -------------------------------------------------------------
    #----------------------------------------
    # Basis Set
    #----------------------------------------
    basis_set = DFTBDirectory(r"dftb/magsil-1-1")

    #----------------------------------------
    # Pair Potentials
    #----------------------------------------
    pair_potentials = DFTBDirectory(r"dftb/magsil-1-1")

    k_point_sampling = MonkhorstPackGrid(
        na=11,
        nb=11,
        )
    numerical_accuracy_parameters = NumericalAccuracyParameters(
        k_point_sampling=k_point_sampling,
        density_mesh_cutoff=150.0*Rydberg,
        )

    iteration_control_parameters = IterationControlParameters()

    calculator = SlaterKosterCalculator(
        basis_set=basis_set,
        pair_potentials=pair_potentials,
        numerical_accuracy_parameters=numerical_accuracy_parameters,
        iteration_control_parameters=iteration_control_parameters,
        )

    bulk_configuration.setCalculator(calculator)
    bulk_configuration.update()

    # -------------------------------------------------------------
    # Forces
    # -------------------------------------------------------------
    forces = Forces(bulk_configuration)
    folder_name = 'job-'+str(i).zfill(digit_num)
    if rank == 0:
        if os.path.exists('job-'+str(i).zfill(digit_num)):
            print(f"文件夹 '{folder_name}' 已存在。")
        else:
            os.mkdir('job-'+str(i).zfill(digit_num))    
        file=open('./job-'+str(i).zfill(digit_num)+'/vasprun.xml','a')
        file.write('<?xml version="1.0" encoding="ISO-8859-1" ?>\n')
        file.write('<modeling>\n')
        file.write(' <generator>\n')
        file.write(' </generator>\n')
        file.write(' <incar>\n')
        file.write(' </incar>\n')
        file.write(' <kpoints>\n')
        file.write(' </kpoints>\n')
        file.write(' <parameters>\n')
        file.write(' </parameters>\n')
        file.write(' <atominfo>\n')
        file.write(' </atominfo>\n')
        file.write(' <structure name="initialpos" >\n')
        file.write(' </structure>\n')
        file.write(' <calculation>\n')
        file.write('  <varray name="forces" >\n')
        for j in range(len(forces.evaluate())):
            file.write('   <v>      '+str(forces.evaluate()[j,0])[0:-7]+'       '+str(forces.evaluate()[j,1])[0:-7]+'       '+str(forces.evaluate()[j,2])[0:-7]+' </v>\n');
        file.write('  </varray>\n')
        file.write(' </calculation>\n')
        file.write('<structure name="finalpos" >\n')
        file.write('</structure>  \n')
        file.write('</modeling>')
        file.close()   
