import os
import time
import sys
import random
import threading
from pathlib import Path
script_abs = Path(__file__).resolve()
project_root = script_abs.parent.parent
sys.path.insert(0, str(project_root))
from eptransk.interface import Interface
from eptransk.hdf5editor import HDF5_Editor
from eptransk.matrixeditor import Matrix_Editor

def write_new_dynamical_matrix_sparse_data_to_hdf5file_device(read_hdf5filename,write_hdf5filename,indice,row_start,shape,value):
    FC=HDF5_Editor()
    FC.write_dynamical_matrix_sparse_data_to_hdf5_by_filename(write_hdf5filename,indice,row_start,shape,value)
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','Analysis')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','AnalysisSpin')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','MetatextObject')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','acoustic_sum_rule')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','atomic_displacement')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','constrain_electrodes')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','constraints')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','dynamical_matrix_left')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','dynamical_matrix_right')    
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/','unit_cell')
    for data_str in ['compact','ni','nj','nk','number_of_orbitals','spin_type']:
        FC.copy_same_data_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/',data_str)
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','finite_difference_method')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','force_tolerance')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','processes_per_displacement')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','repetitions')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','symmetrize')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','use_equivalent_bulk')
    FC.copy_same_element_in_hdf5(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','wigner_seitz')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','class')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','fingerprint')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','is_class')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','module')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','parent')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0//',write_hdf5filename,'/DynamicalMatrix_0/','unicode_name')
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/',write_hdf5filename,'/DynamicalMatrix_0/','version')
    FC.write_essential_data_for_hdf5(write_hdf5filename)
    FC.copy_hdf5_attrs(read_hdf5filename,'/__metadata__/',write_hdf5filename,'/__metadata__/','free_space')
    FC.copy_hdf5_attrs(read_hdf5filename,'/__metadata__/',write_hdf5filename,'/__metadata__/','version')
    for data_str in ['class','is_class','module','parent','type','unicode_name','version']:
        FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/',data_str)
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/','size')   
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/','type')  
    FC.copy_hdf5_attrs(read_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/',write_hdf5filename,'/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/','version')   

def random_gen_replaced_mass_dynamical_matrix_hdf5_by_replaceable_atoms_list(prefix,check_dir_strs,read_hdf5filename,replaceable_atoms_list,replaced_atoms_num,random_num,threads_num):
    IF = Interface()
    filestr = '/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/'
    hdf5filename = read_hdf5filename
    ME = Matrix_Editor()
    numpy_matrix,shape = ME.change_sparse_to_numpy_matrix_by_filestr(filestr,hdf5filename)
    completed_numpy_matrix = ME.add_across_data_to_numpy_matrix_for_dynamical_matrix(numpy_matrix)
    elements,coordinates_arrays,lattice_parameters = IF.get_coordinates_arrays_and_lattice_parameters_from_hdf5_device('DeviceConfiguration_0',read_hdf5filename)
    replace_tag_list = [1]*len(elements)
    for replaceable in replaceable_atoms_list:
        replace_tag_list[replaceable] = 0
    replaceable_list = IF.gen_replaceable_list(replace_tag_list)
    replaced_list_random0 = []
    replaced_list_random = []
    dirfilelist = os.listdir(os.path.abspath(os.curdir))
    for filename in dirfilelist:
        if filename.find('.hdf5') > 0:            
            filename_list = list(map(int, filename[filename.find("_")+1:filename.find(".hdf5")-1].split("_")))
            replaced_list_random0.append(filename_list)
    dirfilelists = []
    for dir_str in check_dir_strs:
        dirfilelist = os.listdir(os.path.abspath(dir_str))
        dirfilelists = dirfilelists + dirfilelist
    for filename in dirfilelists:
        if filename.find('.hdf5') > 0:            
            filename_list = list(map(int, filename[filename.find("_")+1:filename.find(".hdf5")-1].split("_")))
            replaced_list_random0.append(filename_list)        
    for i in range(random_num):
        c = random.sample(list(replaceable_list),replaced_atoms_num)
        c=sorted(c)
        if c in replaced_list_random or c in replaced_list_random0:
            pass
        else:
            replaced_list_random.append(c)  
    threads = []
    x=0
    for t in range(0,threads_num):
        t= threading.Thread(target=gen_one_hdf5file,args=(prefix,read_hdf5filename,completed_numpy_matrix,replaced_list_random,threads_num,x))
        threads.append(t)  
        x+=1
    for thr in threads:
        thr.start()
        time.sleep(3)

def gen_one_hdf5file(prefix,read_hdf5filename,completed_numpy_matrix,replaced_list_random,threads_num,x_index):
    IF = Interface()
    HDF5 = HDF5_Editor()
    ME = Matrix_Editor()
    slice_num = len(replaced_list_random)//threads_num
    if x_index != threads_num-1:
        list_items = replaced_list_random[x_index*slice_num:(x_index+1)*slice_num]
    else:
        list_items = replaced_list_random[x_index*slice_num:]
    for list_item in list_items:
        repeated_relative_atomic_mass_numpy_matrix = IF.get_repeated_relative_atomic_mass_numpy_matrix(read_hdf5filename,list_item)
        repalced_completed_numpy_matrix = repeated_relative_atomic_mass_numpy_matrix*completed_numpy_matrix
        indice1,row_start1,shape1,value1 = ME.change_symmetrized_numpy_matrix_to_dynamical_matrix_sparse_data(repalced_completed_numpy_matrix)
        hdf5filename = HDF5.gen_hdf5_file_name_by_replaced_atoms_list(prefix,list_item)
        time.sleep((int(x_index)+1))    
        write_new_dynamical_matrix_sparse_data_to_hdf5file_device(read_hdf5filename,hdf5filename,indice1,row_start1,shape1,value1)

replaceable_atoms_list = [16,  17,  18,  21,  22,  23,  24,  25,  26,  29,
                                              30,  31,  32,  33,  34,  37,  38,  39,  40,  43,
                                              44,  47,  48,  51,  52,  53,  54,  56,  57,  62,
                                              63,  67,  69,  70,  71,  73,  74,  75,  76,  81,
                                              82,  87,  88,  90,  91,  92,  93,  96,  97, 100,
                                             101, 104, 105, 106, 107, 110, 111, 112, 113, 114,
                                             115, 118, 119, 120, 121, 122, 123, 126, 127, 128]
read_hdf5filename=r'C:\Users\name\Desktop\read_hdf5filename.hdf5'
# check_dir_strs = []
common_params = {
    # 生成文件前缀
    "prefix": 'test1',
    "check_dir_strs": [],
    # 掺杂原子数目
    "replaced_atoms_num": 60,
    # 生成掺杂结构数目
    "random_num": 2000,
    # 并行线程数
    "threads_num": 10
}
print(read_hdf5filename)
random_gen_replaced_mass_dynamical_matrix_hdf5_by_replaceable_atoms_list(common_params['prefix'],common_params['check_dir_strs'],read_hdf5filename,replaceable_atoms_list,common_params['replaced_atoms_num'],common_params['random_num'],common_params['threads_num'])
