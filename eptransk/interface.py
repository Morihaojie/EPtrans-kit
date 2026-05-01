import h5py
import os
import math
import numpy as np
import itertools

def __init__(self):
    self.filepath = os.path.abspath('./')

def get_force_constants_arrays_from_frc_gulp(self):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find('.frc') > 0:
            filedir.append(filename)
    for frcfile in filedir:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            startline = 0
            endline = 0
            for line in f_ck:
                if line.find('force_constants cart-cart') >= 0:
                    startline = f_ck.index(line) +1
                elif line.find('force_constants cart-strain') >= 0:
                    endline = f_ck.index(line) -1
            fc_list=f_ck[startline:endline+1]
            for i in range(len(fc_list)):
                fc_list[i] = fc_list[i].split()
            fc_arrays=np.array(fc_list)
            return fc_arrays

def get_force_constants_arrays_from_fc(self):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find('FORCE_CONSTANTS') >= 0:
            filedir.append(filename)
    for frcfile in filedir:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            startline = 1
            fc_list=f_ck[startline:]             
            for i in range(int(len(fc_list)/4)):
                fc_list[3*i] = fc_list[4*i+1].split()
                fc_list[3*i+1] = fc_list[4*i+2].split()
                fc_list[3*i+2] = fc_list[4*i+3].split()
            fc_arrays=np.array(fc_list[0:int(len(fc_list)/4)*3],dtype=str)
            return fc_arrays

def get_force_constants_arrays_from_sym_fc(self):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find('FORCE_CONSTANTS_SPG') >= 0:
            filedir.append(filename)
    for frcfile in filedir:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            startline = 1
            fc_list=f_ck[startline:]             
            for i in range(int(len(fc_list)/4)):
                fc_list[3*i] = fc_list[4*i+1].split()
                fc_list[3*i+1] = fc_list[4*i+2].split()
                fc_list[3*i+2] = fc_list[4*i+3].split()
            fc_arrays=np.array(fc_list[0:int(len(fc_list)/4)*3],dtype=str)
            return fc_arrays

def get_coordinates_arrays_from_frc_gulp(self):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find('.frc') > 0:
            filedir.append(filename)
    for frcfile in filedir:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            startline = 0
            endline = 0
            for line in f_ck:
                if line.find('coordinates cartesian Angstroms') >= 0:
                    startline = f_ck.index(line) +1
                elif line.find('gradients cartesian eV/Ang') >= 0:
                    endline = f_ck.index(line) -1
            coordinates_list=f_ck[startline:endline+1]
            for i in range(len(coordinates_list)):
                coordinates_list[i] = coordinates_list[i].split()
            coordinates_arrays=np.array(coordinates_list)
    elements_arrays = coordinates_arrays[:,1]
    elements = []
    for i in range(len(elements_arrays)):
        elements.append(self.trans_relative_atomic_mass_or_element_full_name_to_element(str(elements_arrays[i])))
    elements = np.array(elements)
    coordinates_arrays = coordinates_arrays[:,2:].astype(str)
    coordinates_arrays = np.insert(coordinates_arrays, 0, elements, axis=1)  
    return coordinates_arrays

def get_coordinates_arrays_from_pos(self):
    f0 = os.listdir('./')
    self.pos_file=[]
    for filename in f0:
        if filename.find('POSCAR') >= 0 and filename.find('.frc') < 0: 
            self.pos_file.append(filename)
    for frcfile in self.pos_file:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            for line in f_ck:
                if line.find('Direct') >= 0 or line.find('Cartesian') >= 0:
                    startline = f_ck.index(line) +1                          
            coordinates_list=f_ck[startline:]
            element_type = f_ck[5].split()
            element_num = f_ck[6].split()
            elements = []
            for j in range(len(element_type)):
                for k in range(int(element_num[j])):
                    elements.append(element_type[j])
            for i in range(len(coordinates_list)):
                coordinates_list[i] = coordinates_list[i].split()
                coordinates_list[i].insert(0,elements[i])
            coordinates_arrays = np.array(coordinates_list)
            return coordinates_arrays    

def get_coordinates_arrays_from_spos(self):
    f0 = os.listdir('./')
    self.pos_file=[]
    for filename in f0:
        if filename.find('SPOSCAR') >= 0 and filename.find('.frc') < 0: 
            self.pos_file.append(filename)
    for frcfile in self.pos_file:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            for line in f_ck:
                if line.find('Direct') >= 0 or line.find('Cartesian') >= 0:
                    startline = f_ck.index(line) +1                          
            coordinates_list=f_ck[startline:]
            element_type = f_ck[5].split()
            element_num = f_ck[6].split()
            elements = []
            for j in range(len(element_type)):
                for k in range(int(element_num[j])):
                    elements.append(element_type[j])
            for i in range(len(coordinates_list)):
                coordinates_list[i] = coordinates_list[i].split()
                coordinates_list[i].insert(0,elements[i])
            coordinates_arrays = np.array(coordinates_list)
            return coordinates_arrays 

def get_lattice_parameters_from_pos(self):
    f0 = os.listdir('./')
    self.pos_file=[]
    for filename in f0:
        if filename.find('POSCAR') >= 0 and filename.find('.frc') < 0: 
            self.pos_file.append(filename)
    for frcfile in self.pos_file:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()             
            lattice_parameters_list=f_ck[2:5]
            for i in range(len(lattice_parameters_list)):
                lattice_parameters_list[i] = lattice_parameters_list[i].split()
            lattice_parameters = np.array(lattice_parameters_list,dtype =str)
            return lattice_parameters  

def get_reorder_coordinates_arrays_from_xyz(self):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find('.xyz') > 0:
            filedir.append(filename)
    for frcfile in filedir:
        path = os.path.join(self.filepath, frcfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            startline = 2
            coordinates_list=f_ck[startline:]
            for i in range(len(coordinates_list)):
                coordinates_list[i] = coordinates_list[i].split()
            coordinates_arrays=np.array(coordinates_list)
            return coordinates_arrays

def get_item_from_force_constants_arrays(m,n,force_constants_arrays):
    lines_num = len(force_constants_arrays)
    atoms_num = int(math.sqrt(lines_num/3))
    item = force_constants_arrays[3*atoms_num*(m-1)+3*(n-1):3*atoms_num*(m-1)+3*(n-1)+3]
    return item

def get_item_from_numpy_matrix(m,n,force_constants_numpy_matrix):
    lines_num = len(force_constants_numpy_matrix)
    atoms_num = int(math.sqrt(lines_num/3))
    item = force_constants_numpy_matrix[3*(m-1):3*(m-1)+3,3*(n-1):3*(n-1)+3]
    return item       

def get_coordinates_arrays_and_lattice_parameters_from_py(self,pyfilename):
    f0 = os.listdir('./')
    filedir=[]
    for filename in f0:
        if filename.find(pyfilename) >= 0: 
            filedir.append(filename)
    for pyfile in filedir:
        path = os.path.join(self.filepath, pyfile)
        with open(path,'r') as a:
            f_ck = a.readlines()
            for line in f_ck:
                if line.find('# Set up lattice') >= 0:
                    lattice_startline = f_ck.index(line) +1
                elif line.find('# Define elements') >= 0:
                    elements_startline = f_ck.index(line) +1
                elif line.find('# Define coordinates') >= 0:
                    coordinates_startline = f_ck.index(line) +1
                elif line.find('# Set up configuration') >= 0:
                    endline = f_ck.index(line) +1
            latticeslines = f_ck[lattice_startline:elements_startline-2]
            latticestr = ''
            for latticesline in latticeslines:
                if latticesline.find('Hexagonal') >= 0:
                    latticestr = latticesline.replace('\n','').replace(' ','').replace('*Angstrom','')
                    lattices = latticestr[latticestr.find('(')+1:-1].split(',')
                    lattice_parameters = [float(lattices[0])/2,-float(lattices[0])/2*3 ** 0.5,0,float(lattices[0])/2,float(lattices[0])/2*3 ** 0.5,0,0,0,float(lattices[1])]
                    lattice_parameters = np.array(lattice_parameters)
                    lattice_parameters = lattice_parameters.reshape(int(len(lattice_parameters)/3),3)
                    break
                elif latticesline.find('vector') >= 0:
                    lattice_a = latticeslines[0].replace('\n','').replace(' ','').replace('*Angstrom','').replace('vector_a','').replace('=[','').replace(']','').split(',')
                    lattice_b = latticeslines[1].replace('\n','').replace(' ','').replace('*Angstrom','').replace('vector_b','').replace('=[','').replace(']','').split(',')
                    lattice_c = latticeslines[2].replace('\n','').replace(' ','').replace('*Angstrom','').replace('vector_c','').replace('=[','').replace(']','').split(',')
                    lattice_parameters = [lattice_a, lattice_b, lattice_c]
                    lattice_parameters = np.array(lattice_parameters)
                    lattice_parameters = lattice_parameters.astype(float)
                    break
            elementslines = f_ck[elements_startline:coordinates_startline-2]
            elementstr = ''
            for element in elementslines:
                elementstr = elementstr + element.replace('\n','').replace(' ','')
            elements = elementstr[elementstr.find('[')+1:-1].split(',')
            for i in range(len(elements)):
                elements[i] = self.trans_relative_atomic_mass_or_element_full_name_to_element(str(elements[i]))                
            elements = np.array(elements)
            coordinateslines = f_ck[coordinates_startline:endline-2]
            coordinatestr = ''
            for coordinate in coordinateslines:                
                coordinatestr = coordinatestr + coordinate.replace('\n','').replace(' ','').replace('[','').replace(']','')
            coordinates = coordinatestr[coordinatestr.find('=')+1:-1].split(',')
            coordinates = np.array(coordinates)
            coordinates = coordinates.reshape(int(len(coordinates)/3),3)
            coordinates_arrays = np.insert(coordinates, 0, elements, axis=1)
    return coordinates_arrays,lattice_parameters

def get_coordinates_arrays_and_lattice_parameters_from_hdf5(self,wanted_data_name,read_hdf5filename):
    wanted_data_name = '/'+ wanted_data_name
    filepath = os.path.join(self.filepath, read_hdf5filename)
    f = h5py.File(filepath, 'r')
    coordinates_arrays = f[wanted_data_name+'/Analysis/configuration/AtomicConfiguration/cartesian_coordinates/array/data'][:]
    lattice_parameters = f[wanted_data_name+'/Analysis/configuration/bravais_lattice/BravaisLattice/convential_vectors/array/data'][:]
    elements_arrays = f[wanted_data_name+'/Analysis/configuration/AtomicConfiguration/elements/atomic_numbers/data'][:]
    f.close()
    elements = []
    for i in range(len(elements_arrays)):
        elements.append(self.trans_relative_atomic_mass_or_element_full_name_to_element(str(elements_arrays[i])))
    elements = np.array(elements)
    coordinates_arrays = coordinates_arrays.astype(str)
    coordinates_arrays = np.insert(coordinates_arrays, 0, elements, axis=1)  
    return coordinates_arrays,lattice_parameters 

def get_coordinates_arrays_and_lattice_parameters_from_hdf5_bulk(self,wanted_data_name,read_hdf5filename):
    wanted_data_name = '/'+ wanted_data_name
    filepath = os.path.join(self.filepath, read_hdf5filename)
    f = h5py.File(filepath, 'r')
    coordinates_arrays = f[wanted_data_name+'/AtomicConfiguration/cartesian_coordinates/array/data'][:]
    lattice_parameters = f[wanted_data_name+'/bravais_lattice/BravaisLattice/convential_vectors/array/data'][:]
    elements_arrays = f[wanted_data_name+'/AtomicConfiguration/elements/atomic_numbers/data'][:]
    f.close()
    elements = []
    for i in range(len(elements_arrays)):
        elements.append(self.trans_relative_atomic_mass_or_element_full_name_to_element(str(elements_arrays[i])))
    elements = np.array(elements)
    coordinates_arrays = coordinates_arrays.astype(str)
    coordinates_arrays = np.insert(coordinates_arrays, 0, elements, axis=1)  
    return coordinates_arrays,lattice_parameters

def get_coordinates_arrays_and_lattice_parameters_from_hdf5_device(self,wanted_data_name,read_hdf5filename):
    wanted_data_name = '/'+ wanted_data_name
    filepath = os.path.join(self.filepath, read_hdf5filename)
    f = h5py.File(filepath, 'r')
    coordinates_arrays = f[wanted_data_name+'/central_region/AtomicConfiguration/cartesian_coordinates/array/data'][:]
    lattice_parameters = f[wanted_data_name+'/central_region/bravais_lattice/BravaisLattice/convential_vectors/array/data'][:]
    elements_arrays = f[wanted_data_name+'/central_region/AtomicConfiguration/elements/atomic_numbers/data'][:]
    f.close()
    elements = []
    for i in range(len(elements_arrays)):
        elements.append(self.trans_relative_atomic_mass_or_element_full_name_to_element(str(elements_arrays[i])))
    elements = np.array(elements)
    coordinates_arrays = coordinates_arrays.astype(str)
    coordinates_arrays = np.insert(coordinates_arrays, 0, elements, axis=1)  
    return elements,coordinates_arrays,lattice_parameters

def get_symmetrize_matrix_abandon(input_matrix):
    input_matrix = input_matrix.astype(float)
    symmetrize_matrix = np.zeros((len(input_matrix),len(input_matrix)))
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix)):
            symmetrize_matrix[i,j]=(input_matrix[i,j]+input_matrix[j,i])/2
    return symmetrize_matrix

def reshape(reordered_coordinates_arrays,coordinates_arrays):
    reordered_coordinates_arrays = reordered_coordinates_arrays[:,1:].astype(float)
    coordinates_arrays = coordinates_arrays[:,1:].astype(float)
    reshape = []
    for i in range(len(reordered_coordinates_arrays)):
        for j in range(len(coordinates_arrays)):
            if abs(coordinates_arrays[j][0] - reordered_coordinates_arrays[i][0]) <= 0.01 and abs(coordinates_arrays[j][1] - reordered_coordinates_arrays[i][1]) <= 0.01 and abs(coordinates_arrays[j][2] - reordered_coordinates_arrays[i][2] <= 0.01):
                reshape.append(i+1)
            else:
                continue
    return reshape

def reshape_for_frc_gulp(reordered_coordinates_arrays,coordinates_arrays):
    reordered_coordinates_arrays = reordered_coordinates_arrays[:,1:].astype(float)
    coordinates_arrays = coordinates_arrays[:,2:].astype(float)
    reshape = []
    for i in range(len(reordered_coordinates_arrays)):
        for j in range(len(coordinates_arrays)):
            if abs(coordinates_arrays[j][0] - reordered_coordinates_arrays[i][0]) <= 0.01 and abs(coordinates_arrays[j][1] - reordered_coordinates_arrays[i][1]) <= 0.01 and abs(coordinates_arrays[j][2] - reordered_coordinates_arrays[i][2] <= 0.01):
                reshape.append(i+1)
            else:
                continue
    return reshape

def reorder_force_constants_arrays(self,reshape,force_constants_arrays):
    reordered_force_constants_arrays = np.zeros(shape=(len(reshape)*len(reshape),3))
    for m in range(len(reshape)):
        for n in range(len(reshape)):
            reordered_force_constants_arrays[3*len(reshape)*(m)+3*(n):3*len(reshape)*(m)+3*(n)+3,0:3] = self.get_item_from_force_constants_arrays(reshape[m+1],reshape[n+1],force_constants_arrays)
    return reordered_force_constants_arrays


def get_repeated_relative_atomic_mass_numpy_matrix_by_fix_tag_list(self,read_hdf5filename,fix_tag_list):
    elements,coordinates_arrays,lattice_parameters = self.get_coordinates_arrays_and_lattice_parameters_from_hdf5_device('DeviceConfiguration_0',read_hdf5filename)
    relative_atomic_mass_arrays = []
    for element in elements:
        relative_atomic_mass_arrays.append(self.trans_element_full_name_or_element_to_accurate_relative_atomic_mass_atk(element))
    orginal_relative_atomic_mass_arrays = np.array(relative_atomic_mass_arrays)
    new_relative_atomic_mass_arrays = np.array([0]*len(orginal_relative_atomic_mass_arrays)).astype(float)
    for i in range(len(orginal_relative_atomic_mass_arrays)):
        new_relative_atomic_mass_arrays[i] = orginal_relative_atomic_mass_arrays[i]
    replaceable_list = self.gen_replaceable_list(fix_tag_list)
    replaced_list = itertools.combinations(replaceable_list,2)
    for list_item in replaced_list:
        for index in list_item:
            new_relative_atomic_mass_arrays[index] = self.trans_element_relative_atomic_mass_by_index(elements,index)
            relative_atomic_mass_numpy_matrix = np.zeros((len(new_relative_atomic_mass_arrays),len(new_relative_atomic_mass_arrays)))
            for i in range(len(new_relative_atomic_mass_arrays)):            
                for j in range(len(new_relative_atomic_mass_arrays)):
                    relative_atomic_mass_numpy_matrix[i][j] = (np.sqrt(orginal_relative_atomic_mass_arrays)[i]*np.sqrt(orginal_relative_atomic_mass_arrays)[j])/(np.sqrt(new_relative_atomic_mass_arrays)[i]*np.sqrt(new_relative_atomic_mass_arrays)[j])
            repeated_relative_atomic_mass_numpy_matrix = np.zeros((3*len(new_relative_atomic_mass_arrays),3*len(new_relative_atomic_mass_arrays)))
            for i in range(len(new_relative_atomic_mass_arrays)):            
                        for j in range(len(new_relative_atomic_mass_arrays)):
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
    return repeated_relative_atomic_mass_numpy_matrix

def get_repeated_relative_atomic_mass_numpy_matrix_by_fix_atoms_list(self,read_hdf5filename,fix_atoms_list,replaced_atoms_num):
    elements,coordinates_arrays,lattice_parameters = self.get_coordinates_arrays_and_lattice_parameters_from_hdf5_device('DeviceConfiguration_0',read_hdf5filename)
    relative_atomic_mass_arrays = []
    for element in elements:
        relative_atomic_mass_arrays.append(self.trans_element_full_name_or_element_to_accurate_relative_atomic_mass_atk(element))
    orginal_relative_atomic_mass_arrays = np.array(relative_atomic_mass_arrays)
    new_relative_atomic_mass_arrays = np.array([0]*len(orginal_relative_atomic_mass_arrays)).astype(float)
    for i in range(len(orginal_relative_atomic_mass_arrays)):
        new_relative_atomic_mass_arrays[i] = orginal_relative_atomic_mass_arrays[i]
    fix_tag_list = [0]*len(elements)
    for fix_atom in fix_atoms_list:
        fix_tag_list[fix_atom] = 1
    replaceable_list = self.gen_replaceable_list(fix_tag_list)
    replaced_list = itertools.combinations(replaceable_list,replaced_atoms_num)
    for list_item in replaced_list:
        for index in list_item:
            new_relative_atomic_mass_arrays[index] = self.trans_element_relative_atomic_mass_by_index(elements,index)
            relative_atomic_mass_numpy_matrix = np.zeros((len(new_relative_atomic_mass_arrays),len(new_relative_atomic_mass_arrays)))
            for i in range(len(new_relative_atomic_mass_arrays)):            
                for j in range(len(new_relative_atomic_mass_arrays)):
                    relative_atomic_mass_numpy_matrix[i][j] = (np.sqrt(orginal_relative_atomic_mass_arrays)[i]*np.sqrt(orginal_relative_atomic_mass_arrays)[j])/(np.sqrt(new_relative_atomic_mass_arrays)[i]*np.sqrt(new_relative_atomic_mass_arrays)[j])
            repeated_relative_atomic_mass_numpy_matrix = np.zeros((3*len(new_relative_atomic_mass_arrays),3*len(new_relative_atomic_mass_arrays)))
            for i in range(len(new_relative_atomic_mass_arrays)):            
                        for j in range(len(new_relative_atomic_mass_arrays)):
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                            repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
    return repeated_relative_atomic_mass_numpy_matrix

def get_repeated_relative_atomic_mass_numpy_matrix(self,read_hdf5filename,replaced_list):
    elements,coordinates_arrays,lattice_parameters = self.get_coordinates_arrays_and_lattice_parameters_from_hdf5_device('DeviceConfiguration_0',read_hdf5filename)
    relative_atomic_mass_arrays = []
    for element in elements:
        relative_atomic_mass_arrays.append(self.trans_element_full_name_or_element_to_accurate_relative_atomic_mass_atk(element))
    orginal_relative_atomic_mass_arrays = np.array(relative_atomic_mass_arrays)
    new_relative_atomic_mass_arrays = np.array([0]*len(orginal_relative_atomic_mass_arrays)).astype(float)
    for i in range(len(orginal_relative_atomic_mass_arrays)):
        new_relative_atomic_mass_arrays[i] = orginal_relative_atomic_mass_arrays[i]
    for index in replaced_list:
        new_relative_atomic_mass_arrays[index] = self.trans_element_relative_atomic_mass_by_index(elements,index)            
        relative_atomic_mass_numpy_matrix = np.zeros((len(new_relative_atomic_mass_arrays),len(new_relative_atomic_mass_arrays)))
        for i in range(len(new_relative_atomic_mass_arrays)):            
            for j in range(len(new_relative_atomic_mass_arrays)):
                relative_atomic_mass_numpy_matrix[i][j] = (np.sqrt(orginal_relative_atomic_mass_arrays)[i]*np.sqrt(orginal_relative_atomic_mass_arrays)[j])/(np.sqrt(new_relative_atomic_mass_arrays)[i]*np.sqrt(new_relative_atomic_mass_arrays)[j])
        repeated_relative_atomic_mass_numpy_matrix = np.zeros((3*len(new_relative_atomic_mass_arrays),3*len(new_relative_atomic_mass_arrays)))
    for i in range(len(new_relative_atomic_mass_arrays)):            
                for j in range(len(new_relative_atomic_mass_arrays)):
                    repeated_relative_atomic_mass_numpy_matrix[3*i][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+1][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+1] = relative_atomic_mass_numpy_matrix[i][j]
                    repeated_relative_atomic_mass_numpy_matrix[3*i+2][3*j+2] = relative_atomic_mass_numpy_matrix[i][j]
    return repeated_relative_atomic_mass_numpy_matrix

def repeat_coordinates_arrays(repeat_times,coordinates_arrays,lattice_parameters):
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    reordered_coordinates_arrays = np.zeros((len(coordinates_arrays)*repeat_times_num,3))
    elements = []
    atoms_num = len(coordinates_arrays) 
    for i in range(int(repeat_times[0])):
        for j in range(int(repeat_times[1])):
            for k in range(int(repeat_times[2])):
                for l in range(atoms_num*(k)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i,atoms_num*(k+1)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i):
                    lent = atoms_num*(k)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i
                    lattice = np.array(i*lattice_parameters[0]+j*lattice_parameters[1]+k*lattice_parameters[2])
                    reordered_coordinates_arrays[l] = coordinates_arrays[l-lent,1:4]
                    reordered_coordinates_arrays[l] = reordered_coordinates_arrays[l] + lattice
                    elements.append(coordinates_arrays[l-lent,0])
    reordered_coordinates_arrays = reordered_coordinates_arrays.astype(str)
    elements = np.array(elements)
    reordered_coordinates_arrays = np.insert(reordered_coordinates_arrays, 0, elements, axis=1)        
    return reordered_coordinates_arrays

def repeat_coordinates_arrays_and_lattice_parameters_from_py(repeat_times,coordinates_arrays,lattice_parameters):
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    repeated_coordinates_arrays = np.zeros((len(coordinates_arrays)*repeat_times_num,3))
    elements = []
    atoms_num = len(coordinates_arrays)
    for i in range(int(repeat_times[0])):
        for j in range(int(repeat_times[1])):
            for k in range(int(repeat_times[2])):
                for l in range(atoms_num*(k)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i,atoms_num*(k+1)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i):
                    lent = atoms_num*(k)+atoms_num*int(repeat_times[2])*j+atoms_num*int(repeat_times[1])*int(repeat_times[2])*i
                    lattice = np.array(i*lattice_parameters[0]+j*lattice_parameters[1]+k*lattice_parameters[2])
                    repeated_coordinates_arrays[l] = coordinates_arrays[l-lent,1:4]
                    repeated_coordinates_arrays[l] = repeated_coordinates_arrays[l] + lattice
                    elements.append(coordinates_arrays[l-lent,0])
    repeated_coordinates_arrays = repeated_coordinates_arrays.astype(str)
    elements = np.array(elements)
    repeated_coordinates_arrays = np.insert(repeated_coordinates_arrays, 0, elements, axis=1)
    repeated_lattice_parameters = np.array([int(repeat_times[0])*lattice_parameters[0].astype(float),int(repeat_times[1])*lattice_parameters[1].astype(float),int(repeat_times[2])*lattice_parameters[2].astype(float)])
    return repeated_coordinates_arrays, repeated_lattice_parameters

def repeat_coordinates_arrays_and_lattice_parameters_from_pos(repeat_times,coordinates_arrays,lattice_parameters):
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    repeated_coordinates_arrays = np.zeros((len(coordinates_arrays)*repeat_times_num,3))
    elements = []
    atoms_num = len(coordinates_arrays)
    for l in range(atoms_num):
        for i in range(int(repeat_times[2])):
            for j in range(int(repeat_times[1])):
                for k in range(int(repeat_times[0])):
                    lattice = lattice_parameters.astype(float)
                    repeated_coordinates_arrays[repeat_times_num*l+repeat_times_num*i+int(repeat_times[1])*j+k] = coordinates_arrays[l,1:4]
                    repeated_coordinates_arrays[repeat_times_num*l+repeat_times_num*i+int(repeat_times[1])*j+k] = repeated_coordinates_arrays[repeat_times_num*l+repeat_times_num*i+int(repeat_times[1])*j+k]+k*lattice[0]+j*lattice[1]+i*lattice[2]
                    elements.append(coordinates_arrays[l,0])
    repeated_coordinates_arrays = repeated_coordinates_arrays.astype(str)
    elements = np.array(elements)
    repeated_coordinates_arrays = np.insert(repeated_coordinates_arrays, 0, elements, axis=1)
    repeated_lattice_parameters = np.array([int(repeat_times[0])*lattice_parameters[0].astype(float),int(repeat_times[1])*lattice_parameters[1].astype(float),int(repeat_times[2])*lattice_parameters[2].astype(float)])
    return repeated_coordinates_arrays, repeated_lattice_parameters

def trans_force_constants_arrays_to_force_constants(force_constants_arrays):
    force_constants_arrays = force_constants_arrays.astype(str)
    atoms_num = int((len(force_constants_arrays)/3)**0.5)
    filename = 'FORCE_CONSTANTS.txt'
    with open(filename, 'w') as file_object:
        file_object.write(str(atoms_num)+'\n')
        for i in range(atoms_num):
            for j in range(atoms_num):
                file_object.write(str(i+1)+' '+str(j+1)+'\n')
                file_object.write(force_constants_arrays[i*3*atoms_num+j*3][0]+'    '+force_constants_arrays[i*3*atoms_num+j*3][1]+'    '+force_constants_arrays[i*3*atoms_num+j*3][2]+'\n')
                file_object.write(force_constants_arrays[i*3*atoms_num+j*3+1][0]+'    '+force_constants_arrays[i*3*atoms_num+j*3+1][1]+'    '+force_constants_arrays[i*3*atoms_num+j*3+1][2]+'\n')
                file_object.write(force_constants_arrays[i*3*atoms_num+j*3+2][0]+'    '+force_constants_arrays[i*3*atoms_num+j*3+2][1]+'    '+force_constants_arrays[i*3*atoms_num+j*3+2][2]+'\n')

def trans_force_constants_arrays_to_force_constants_numpy_matrix(self,force_constants_arrays,repeat_times_num):
    lines_num = len(force_constants_arrays)
    atoms_num = int(math.sqrt(lines_num/3)/(repeat_times_num))        
    force_constants_numpy_matrix = np.zeros((atoms_num*3,3*atoms_num*repeat_times_num))
    for i in range(atoms_num):
        for j in range(repeat_times_num*atoms_num):
            force_constants_numpy_matrix[3*i:3*i+3,3*j:3*j+3]= self.get_item_from_force_constants_arrays(i+1,j+1,force_constants_arrays)
    return force_constants_numpy_matrix

def trans_element_to_relative_atomic_mass(element):
    if element == 'C':
        relative_atomic_mass = 12.0096
    elif element == 'H':
        relative_atomic_mass = 1.007
    elif element == 'B':
        relative_atomic_mass = 10.806           
    elif element == 'N':
        relative_atomic_mass = 14.006
    elif element == 'Si':
        relative_atomic_mass = 28.084
    elif element == 'Ge':
        relative_atomic_mass = 72.63  
    elif element == 'S':
        relative_atomic_mass = 32.065
    elif element == 'O':
        relative_atomic_mass = 15.999
    elif element == 'P':
        relative_atomic_mass = 30.973
    else:
        print('未收录元素：'+element)     
    return relative_atomic_mass

def trans_relative_atomic_mass_or_element_full_name_to_element(input_data):
    if input_data == 'Carbon' or input_data == '6':
        element  = 'C'
    elif input_data == 'Hydrogen' or input_data == '1':
        element  = 'H'
    elif input_data == 'Boron' or input_data == '5':
        element  = 'B'
    elif input_data == 'Nitrogen' or input_data == '7':
        element  = 'N'
    elif input_data == 'Silicon' or input_data == '14':
        element  = 'Si'
    elif input_data == 'Germanium' or input_data == '32':
        element  = 'Ge'
    elif input_data == 'Sulfur' or input_data == '16':
        element  = 'S'
    elif input_data == 'Oxygen' or input_data == '8':
        element  = 'O'
    elif input_data == 'Phosphorus' or input_data == '15':
        element  = 'P'
    elif input_data == 'Ruthenium' or input_data == '44': 
        element  = 'Ru' 
    elif input_data == 'Iron' or input_data == '26': 
        element  = 'Fe'                   
    else:
        print('结构中有未收录元素：'+ input_data + '，请添加')     
    return element        

def trans_element_full_name_or_element_to_accurate_relative_atomic_mass_atk(input_data):
    if input_data == 'C'or input_data == 'Carbon':
        relative_atomic_mass = 12.0107
    elif input_data == 'H' or input_data == 'Hydrogen':
        relative_atomic_mass = 1.00794
    elif input_data == 'B' or input_data == 'Boron':
        relative_atomic_mass = 10.811           
    elif input_data == 'N' or input_data == 'Nitrogen':
        relative_atomic_mass = 14.0067
    elif input_data == 'Si' or input_data == 'Silicon':
        relative_atomic_mass = 28.0855
    elif input_data == 'Ge' or input_data == 'Germanium':
        relative_atomic_mass = 72.64  
    elif input_data == 'S' or input_data == 'Sulfur':
        relative_atomic_mass = 32.065
    elif input_data == 'O' or input_data == 'Oxygen':
        relative_atomic_mass = 15.9994
    elif input_data == 'P' or input_data == 'Phosphorus':
        relative_atomic_mass = 30.9738
    elif input_data == 'Ru' or input_data == 'Ruthenium':
        relative_atomic_mass = 101.07
    elif input_data == 'Os' or input_data == 'Osmium':
        relative_atomic_mass = 190.23
    elif input_data == 'Fe' or input_data == 'Iron':
        relative_atomic_mass = 55.845            
    elif input_data == 'Mn' or input_data == 'Manganese':
        relative_atomic_mass = 54.938      
    elif input_data == 'Co' or input_data == 'Cobalt':
        relative_atomic_mass = 58.9332    
    elif input_data == 'Ni' or input_data == 'Nickel':
        relative_atomic_mass = 58.6934
    elif input_data == 'Cu' or input_data == 'Copper':
        relative_atomic_mass = 63.546                                       
    else:
        print('结构中有未收录元素：'+ input_data + '，请添加')     
    return relative_atomic_mass        

def gen_replaceable_tag_list(fix_tag_list):
    replaceable_tag_list = [0] * len(fix_tag_list)
    for i in range(len(fix_tag_list)):
        if fix_tag_list[i] != 1:

            replaceable_tag_list =[]

    return replaceable_tag_list
    
def gen_replaceable_list(fix_tag_list):
    replaceable_list= list(range(len(fix_tag_list)))
    remove_list=[]
    for i in range(len(replaceable_list)):
        if fix_tag_list[i] == 1:
            remove_list.append(i)
    for remove_item in remove_list:
        replaceable_list.remove(remove_item)
    return replaceable_list

def trans_element_relative_atomic_mass(element,replaceable_tag):
    if replaceable_tag == 0:
        pass
    elif replaceable_tag == 1:
        if element == 'C':   
            new_relative_atomic_mass = 14
        elif element == 'Ru':
            new_relative_atomic_mass = 100
        elif element == 'N':
            new_relative_atomic_mass = 14.0067
        elif element == 'H':
            new_relative_atomic_mass = 1.00794                               
        else:
            print('结构中有未收录元素：'+ element + '，请添加')     
    return new_relative_atomic_mass             

def trans_element_relative_atomic_mass_by_index(elements,index):
    element = elements[index]
    if element == 'C':   
        new_relative_atomic_mass = 14
    elif element == 'Ru':
        new_relative_atomic_mass = 104
    elif element == 'N':
        new_relative_atomic_mass = 14.0067
    elif element == 'H':
        new_relative_atomic_mass = 1.00794                               
    else:
        print('结构中有未收录元素：'+ element + '，请添加')     
    return new_relative_atomic_mass  

def trans_force_constants_numpy_matrix_to_dynamical_numpy_matrix(self,force_constants_numpy_matrix,reordered_coordinates_arrays):
    trans_xishu = 1/(1.9927e-26/12)/(1.6021766208e23/1.05457266)
    atoms_num = int(len(force_constants_numpy_matrix)/3)
    total_atoms_num = int(len(force_constants_numpy_matrix[0])/3)
    dynamical_numpy_matrix = np.zeros((atoms_num*3,total_atoms_num*3),dtype=float)
    for i in range(atoms_num):
        for j in range(total_atoms_num):
            MM = self.trans_element_to_relative_atomic_mass(reordered_coordinates_arrays[i][0])*self.trans_element_to_relative_atomic_mass(reordered_coordinates_arrays[j][0])
            dynamical_numpy_matrix[i:i+3,j:j+3] = self.get_item_from_numpy_matrix(i+1,j+1,force_constants_numpy_matrix)/(math.sqrt(MM))*trans_xishu
    return dynamical_numpy_matrix 

def trans_coordinates_arrays_to_pos(coordinates_arrays,lattice_parameters,filename):
    coordinates_arrays = coordinates_arrays.astype(str)
    lattice_parameters = lattice_parameters.astype(str)        
    with open(filename, 'w') as file_object:
        file_object.write('global'+'\n')
        file_object.write('1.0'+'\n')
        for i in range(len(lattice_parameters)):
            file_object.write('       '+lattice_parameters[i,0]+'         '+lattice_parameters[i,1]+'         '+lattice_parameters[i,2]+'\n')
        elements = {}
        elements_type = ''
        for j in range(len(coordinates_arrays)):
            if coordinates_arrays[j,0] != elements_type:
                elements[coordinates_arrays[j,0]] = 1
                elements_type = coordinates_arrays[j,0]
            elif coordinates_arrays[j,0] == elements_type:
                elements[coordinates_arrays[j,0]] = elements[coordinates_arrays[j,0]] + 1
        for element,num in elements.items():
            file_object.write('    '+element)
        file_object.write('\n')
        for element,num in elements.items():
            file_object.write('   '+str(num))
        file_object.write('\n')
        file_object.write('Cartesian\n')
        for k in range(len(coordinates_arrays)):
            file_object.write('     '+coordinates_arrays[k,1]+'         '+coordinates_arrays[k,2]+'         '+coordinates_arrays[k,3]+'\n') 

def trans_coordinates_arrays_from_py_to_pos(coordinates_arrays,lattice_parameters,filename):
    coordinates_arrays = coordinates_arrays.astype(str)
    lattice_parameters = lattice_parameters.astype(str)        
    with open(filename, 'w') as file_object:
        file_object.write('global'+'\n')
        file_object.write('1.0'+'\n')
        for i in range(len(lattice_parameters)):
            file_object.write('       '+lattice_parameters[i,0]+'         '+lattice_parameters[i,1]+'         '+lattice_parameters[i,2]+'\n')
        elements_types = [coordinates_arrays[0,0]]
        elements_nums = [1]
        elements_index = 0
        elements = {coordinates_arrays[0,0]:1}
        for j in range(1,len(coordinates_arrays)):
            if coordinates_arrays[j,0] != elements_types[elements_index]:
                elements_index = elements_index + 1
                elements[elements_index] = 1
                elements_nums.append(1)
                elements_types.append(coordinates_arrays[j,0])
            elif coordinates_arrays[j,0] == elements_types[elements_index]:
                elements_nums[elements_index] = elements_nums[elements_index] + 1
        for element in elements_types:
            file_object.write('    '+element)
        file_object.write('\n')
        for num in elements_nums:
            file_object.write('   '+str(num))
        file_object.write('\n')
        file_object.write('Cartesian\n')
        for k in range(len(coordinates_arrays)):
            file_object.write('     '+coordinates_arrays[k,1]+'         '+coordinates_arrays[k,2]+'         '+coordinates_arrays[k,3]+'\n')

def trans_coordinates_arrays_to_cif(coordinates_arrays,lattice_parameters,filename):
    fractional_coordinates_arrays = coordinates_arrays[:,1:].astype(float)
    fractional_coordinates_arrays = (np.mat(fractional_coordinates_arrays) * (np.mat(lattice_parameters).I)).A
    lattice_a = (lattice_parameters[0][0]*lattice_parameters[0][0] +lattice_parameters[0][1]*lattice_parameters[0][1])** 0.5
    lattice_b = (lattice_parameters[1][0]*lattice_parameters[1][0] +lattice_parameters[1][1]*lattice_parameters[1][1])** 0.5
    fractional_coordinates_arrays = fractional_coordinates_arrays.astype(str)
    lattice_parameters = lattice_parameters.astype(str)        
    with open(filename, 'w') as file_object:
        file_object.write('data_global'+'\n')
        file_object.write('_cell_length_a '+str(lattice_a)+'\n')
        file_object.write('_cell_length_b '+str(lattice_b)+'\n')
        file_object.write('_cell_length_c '+lattice_parameters[2][2]+'\n')
        file_object.write('_cell_angle_alpha 90'+'\n')
        file_object.write('_cell_angle_beta 90'+'\n')
        file_object.write('_cell_angle_gamma 120'+'\n')
        file_object.write("_symmetry_space_group_name_H-M 'P -1'"+'\n')
        file_object.write('loop_'+'\n')
        file_object.write('_symmetry_equiv_pos_as_xyz'+'\n')
        file_object.write("  'x,y,z'"+'\n')
        file_object.write('loop_'+'\n')
        file_object.write('_atom_site_label'+'\n')
        file_object.write('_atom_site_fract_x'+'\n')
        file_object.write('_atom_site_fract_y'+'\n')
        file_object.write('_atom_site_fract_z'+'\n')
        for k in range(len(coordinates_arrays)):
            file_object.write(coordinates_arrays[k,0]+' '+fractional_coordinates_arrays[k,0]+' '+fractional_coordinates_arrays[k,1]+' '+fractional_coordinates_arrays[k,2]+'\n')

def rotate_coordinates_arrays(coordinates_arrays,theta):
    rotate_angle = math.radians(theta)
    rotated_coordinates_arrays = coordinates_arrays[:,1:].astype(float)
    rotate_matrix = np.mat(np.array([[math.cos(rotate_angle),-math.sin(rotate_angle),0],[math.sin(rotate_angle),math.cos(rotate_angle),0],[0,0,1]]))
    rotated_coordinates_arrays = (np.mat(rotated_coordinates_arrays) * (rotate_matrix)).A.astype(str)
    elements = coordinates_arrays[:,0]
    rotated_coordinates_arrays = np.insert(rotated_coordinates_arrays, 0, elements, axis=1)        
    return rotated_coordinates_arrays
