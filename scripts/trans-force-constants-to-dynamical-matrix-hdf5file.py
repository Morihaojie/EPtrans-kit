import os
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eptransk.interface import Interface
from eptransk.hdf5editor import HDF5_Editor

def frc_to_dynamical_numpy_matrix_gulp(repeat_times,**kwargs):
    IF = Interface()
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    coordinates_arrays = IF.get_coordinates_arrays_from_frc_gulp()
    force_constants_arrays = IF.get_force_constants_arrays_from_frc_gulp()
    reordered_coordinates_arrays = IF.get_reordered_coordinates()
    reshape = IF.reshape(reordered_coordinates_arrays,coordinates_arrays)
    reordered_force_constants_arrays = IF.reorder_force_constants_arrays(reshape,force_constants_arrays)
    force_constants_numpy_matrix = IF.trans_force_constants_arrays_to_force_constants_numpy_matrix(reordered_force_constants_arrays,repeat_times_num)
    dynamical_numpy_matrix = IF.trans_force_constants_numpy_matrix_to_dynamical_numpy_matrix(force_constants_numpy_matrix,reordered_coordinates_arrays)
    return dynamical_numpy_matrix

def fc_to_dynamical_numpy_matrix(repeat_times,**kwargs):
    IF = Interface()
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    force_constants_arrays = IF.get_force_constants_arrays_from_fc()
    coordinates_arrays = IF.get_coordinates_arrays_from_pos()
    reordered_coordinates_arrays = IF.get_reordered_coordinates()
    reshape = IF.reshape(reordered_coordinates_arrays,coordinates_arrays)
    reordered_force_constants_arrays = IF.reorder_force_constants_arrays(reshape,force_constants_arrays)
    force_constants_numpy_matrix = IF.trans_force_constants_arrays_to_force_constants_numpy_matrix(reordered_force_constants_arrays,repeat_times_num)
    dynamical_numpy_matrix = IF.trans_force_constants_numpy_matrix_to_dynamical_numpy_matrix(force_constants_numpy_matrix,reordered_coordinates_arrays)
    return dynamical_numpy_matrix

def frc_to_symmetrized_dynamical_numpy_matrix_gulp(pyfilename,repeat_times,**kwargs):
    IF = Interface()
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    repeat_times_str = '"'+repeat_times_num[0]+' '+repeat_times_num[1]+' '+repeat_times_num[2]+'"'
    force_constants_arrays = IF.get_force_constants_arrays_from_frc_gulp()
    coordinates_arrays = IF.get_coordinates_arrays_from_frc_gulp()
    lattice_parameters = IF.get_coordinates_arrays_and_lattice_parameters_from_py(pyfilename)
    IF.trans_coordinates_arrays_to_pos(coordinates_arrays,lattice_parameters,'POSCAR')
    os.popen('phonopy -d --dim='+repeat_times_str+' -c POSCAR')
    time.sleep(5)
    reordered_coordinates_arrays = IF.get_coordinates_arrays_from_spos()
    reshape = IF.reshape(reordered_coordinates_arrays,coordinates_arrays)
    reordered_force_constants_arrays = IF.reorder_force_constants_arrays(reshape,force_constants_arrays)
    IF.trans_force_constants_arrays_to_force_constants(reordered_force_constants_arrays)
    os.rename('FORCE_CONSTANTS.txt','FORCE_CONSTANTS')    
    os.popen('phonopy --dim='+repeat_times_str+' -c POSCAR --readfc --fc-symmetry --fc-spg-symmetry --full-fc')
    time.sleep(5)
    symmetrized_force_constants_arrays = IF.get_force_constants_arrays_from_sym_fc()
    coordinates_arrays = IF.get_coordinates_arrays_from_spos()
    reordered_coordinates_arrays = IF.get_coordinates_arrays_from_frc_gulp()
    reshape = IF.reshape(reordered_coordinates_arrays,coordinates_arrays)
    reordered_symmetrized_force_constants_arrays = IF.reorder_force_constants_arrays(reshape,symmetrized_force_constants_arrays)
    symmetrized_force_constants_numpy_matrix = IF.trans_force_constants_arrays_to_force_constants_numpy_matrix(reordered_symmetrized_force_constants_arrays,repeat_times_num)
    symmetrized_dynamical_numpy_matrix = IF.trans_force_constants_numpy_matrix_to_dynamical_numpy_matrix(symmetrized_force_constants_numpy_matrix,reordered_coordinates_arrays)
    return symmetrized_dynamical_numpy_matrix    

def frc_to_dynamical_numpy_matrix_py_gulp(pyfilename,repeat_times,**kwargs):
    IF = Interface()
    repeat_times_num = int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])
    force_constants_arrays = IF.get_force_constants_arrays_from_frc_gulp()
    coordinates_arrays = IF.get_coordinates_arrays_from_frc_gulp()
    reordered_coordinates_arrays,lattice_parameters = IF.get_coordinates_arrays_and_lattice_parameters_from_py(pyfilename)
    repeated_and_reordered_coordinates_arrays = IF.repeat_coordinates_arrays(repeat_times,reordered_coordinates_arrays,lattice_parameters)
    reshape = IF.reshape(repeated_and_reordered_coordinates_arrays,coordinates_arrays)
    reordered_force_constants_arrays = IF.reorder_force_constants_arrays(reshape,force_constants_arrays)
    force_constants_numpy_matrix = IF.trans_force_constants_arrays_to_force_constants_numpy_matrix(reordered_force_constants_arrays,repeat_times_num)
    dynamical_numpy_matrix = IF.trans_force_constants_numpy_matrix_to_dynamical_numpy_matrix(force_constants_numpy_matrix,reordered_coordinates_arrays)
    return dynamical_numpy_matrix  

def write_numpy_matrix_to_hdf5(hdf5filename,read_hdf5filename,dynamical_numpy_matrix,repeat_times):
    FC=HDF5_Editor()
    FC.write_dynamical_matrix_sparse_data_to_hdf5(hdf5filename,dynamical_numpy_matrix)
    FC.write_essential_data_for_dynamical_matrix(hdf5filename,read_hdf5filename,repeat_times)
    FC.write_essential_data_for_hdf5(hdf5filename)
    FC.add_hdf5_attrs_to_hdf5(read_hdf5filename,hdf5filename)

hdf5filename=r'C:\Users\name\Desktop\write_hdf5filename.hdf5'
read_hdf5filename=r'C:\Users\name\Desktop\read_hdf5filename.hdf5'
common_params = {
    "pyfilename": r'C:\Users\name\Desktop\filename.py',
    # "pyfilename": r'filename.py',   
    "repeat_times": '331'
}
methods = {
    "1": (frc_to_dynamical_numpy_matrix_gulp, "GULP计算结果转换动力学矩阵文件"),
    "2": (fc_to_dynamical_numpy_matrix, "二阶力常数文件转换动力学矩阵文件"),
    "3": (frc_to_symmetrized_dynamical_numpy_matrix_gulp, "GULP计算结果转换动力学矩阵文件（对称化）"),
    "4": (frc_to_dynamical_numpy_matrix_py_gulp, "GULP结果转换动力学矩阵文件（参考py文件）")
}
print("请选择要使用的方法：")
for key, (_, description) in methods.items():
    print(f"{key}. {description}")
choice = input("\n请输入数字 (1-4): ")
if choice in methods:
    func, desc = methods[choice]
    dynamical_numpy_matrix = func(**common_params)
    print(f"\n您选择了：{desc}")
else:
    print("无效输入，请运行程序并输入 1~4 之间的数字。")
write_numpy_matrix_to_hdf5(hdf5filename,read_hdf5filename,dynamical_numpy_matrix,common_params['repeat_times'])