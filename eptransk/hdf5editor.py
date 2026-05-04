import h5py
import os
import numpy as np

class HDF5_Editor():
    def __init__(self):
        f0 = os.listdir('./')
        self.h5_file=[]
        for filename in f0:
            if filename.find('.hdf5') > 0:
                self.h5_file.append(filename)
        self.filepath = os.path.abspath('./')

    def hdf5_append(self,input):    
        self.hdf5_index.append(input)

    def read_hdf5_index_structure(self,hdf5filename):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'r')
        self.hdf5_index=[]
        f.visit(self.hdf5_append)
        f.close()
        return self.hdf5_index

    def read_hdf5_group_structure(self,wanted_data_path,hdf5filename):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'r')
        hdf5_group_structure = []
        for key_index in f[wanted_data_path].keys():
            hdf5_group_structure.append(key_index)
        f.close()
        return hdf5_group_structure

    def read_hdf5_wanted_data(self,wanted_data_path,wanted_data,hdf5filename):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'r')
        hdf5_group_index = []
        for key_index in f[wanted_data_path].keys():
            hdf5_group_index.append(key_index)
        f.close()
        wanted_datas = []      
        for dataset_index in hdf5_group_index:
            if dataset_index.find(wanted_data) >= 0:
                wanted_datas.append(dataset_index)
            else:
                continue
        return wanted_datas
    
    def read_hdf5(self,wanted_data_path,hdf5filename):
        if os.path.isabs(hdf5filename) or os.path.sep in hdf5filename:
            filepath = hdf5filename
        else:
            filepath = os.path.join(self.filepath,hdf5filename)        
        with h5py.File(filepath, 'r') as f:
            return f[wanted_data_path][()]

    def read_numpy_data_from_hdf5(self,hdf5filename):
        filestr = '/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/'
        indice = self.read_hdf5(filestr+'indices',hdf5filename)
        row_start = self.read_hdf5(filestr+'row_starts',hdf5filename)
        shape = self.read_hdf5(filestr+'shape',hdf5filename)
        value = self.read_hdf5(filestr+'values',hdf5filename)
        return indice,row_start,shape,value

    def read_numpy_data_from_hdf5_by_filestr(self,filestr,hdf5filename):
        if not filestr.endswith('/'):
            filestr = filestr + '/'        
        indice = self.read_hdf5(filestr+'indices',hdf5filename)
        row_start = self.read_hdf5(filestr+'row_starts',hdf5filename)
        shape = self.read_hdf5(filestr+'shape',hdf5filename)
        value = self.read_hdf5(filestr+'values',hdf5filename)
        return indice,row_start,shape,value
        
    def read_complex_data_from_hdf5_by_filestr(self,filestr,hdf5filename):
        if not filestr.endswith('/'):
            filestr = filestr + '/'
        data = self.read_data_from_hdf5_complex(filestr+'data', hdf5filename)
        indices = self.read_data_from_hdf5_complex(filestr+'indices', hdf5filename)
        indptr = self.read_data_from_hdf5_complex(filestr+'indptr', hdf5filename)
        shape = self.read_data_from_hdf5_complex(filestr+'shape', hdf5filename)
        return data,indices,indptr,shape
    
    def copy_hdf5(self,read_hdf5filename,read_data_path,write_hdf5filename,write_data_path):             
        read_filepath = os.path.join(self.filepath, read_hdf5filename)
        write_filepath = os.path.join(self.filepath, write_hdf5filename)
        f_read = h5py.File(read_filepath, 'r')
        f_write = h5py.File(write_filepath, 'a')
        write_group_id = f_write.require_group(write_data_path)
        f_read.copy(read_data_path,write_group_id)
        f_read.close()
        f_write.close()

    def copy_same_element_in_hdf5(self,read_hdf5filename,read_data_path,write_hdf5filename,write_data_path,same_element):
        read_filepath = os.path.join(self.filepath, read_hdf5filename)
        write_filepath = os.path.join(self.filepath, write_hdf5filename)
        f_read = h5py.File(read_filepath, 'r')
        f_write = h5py.File(write_filepath, 'a')
        read_data_path = read_data_path + same_element
        write_data_path = write_data_path
        write_group_id = f_write.require_group(write_data_path)           
        f_read.copy(read_data_path,write_group_id)
        f_read.close()
        f_write.close() 

    def copy_same_data_in_hdf5(self,read_hdf5filename,read_data_path,write_hdf5filename,write_data_path,same_data_name):
        read_data_path = read_data_path + same_data_name
        write_data_path = write_data_path + same_data_name
        same_data = self.read_hdf5(read_data_path,read_hdf5filename)
        if str(type(same_data)).find('float') >= 0:
            self.write_hdf5(write_data_path,same_data,write_hdf5filename,'',1)
        elif  str(type(same_data)).find('int32') >= 0:
            self.write_hdf5(write_data_path,same_data,write_hdf5filename,'int32',1)
        elif str(type(same_data)).find('bytes') >= 0:
            self.write_hdf5(write_data_path,same_data,write_hdf5filename,'str',1)
        else:
            print('复制data出现其他情况：'+str(type(same_data))) 

    def write_hdf5(self,input_data_path,store_data,hdf5filename,input_format,enforce_flag):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'a')
        file_groups = list(f.keys())        
        data_path_list = [s for s in input_data_path.split('/') if s]
        if enforce_flag != 1:
            replace_str=[]
            for file_group in file_groups:
                if data_path_list[0] == file_group:
                    replace_str = data_path_list[0][0:-1]+str(int(data_path_list[0][-1])+1)
            data_path = ''
            if replace_str == []:            
                data_path = input_data_path + '/'
            elif replace_str != []:
                data_path = '/'+ replace_str + '/'
                for i in range(1,len(data_path_list)):
                    data_path = data_path + data_path_list[i] + '/'
        else:
            data_path = input_data_path + '/'
        data_path = data_path[:-1]
        if input_format == '':
            format_type = 'float64'
            f.create_dataset(data_path,data=store_data,dtype=format_type)
        elif input_format == 'str':
            format_type = h5py.special_dtype(vlen=str)
            f.create_dataset(data_path,data=store_data,dtype=format_type)
        else:
            format_type = input_format
            f.create_dataset(data_path,data=store_data,dtype=format_type)
        f.close()

    def write_empty_group_to_hdf5(self,input_data_path,hdf5filename):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'a')
        file_groups = list(f.keys())
        data_path_list = [s for s in input_data_path.split('/') if s]
        replace_str=[]
        for file_group in file_groups:
            if data_path_list[0] == file_group:
                print(data_path_list[0][-1])
                replace_str = data_path_list[0][0:-1]+str(int(data_path_list[0][-1])+1)
        data_path = ''
        if replace_str == []:            
            data_path = input_data_path
        elif replace_str != []:
            data_path = '/'+ replace_str + '/'
            for i in range(1,len(data_path_list)):
                data_path = data_path + data_path_list[i] + '/'
        f.create_group(data_path)
        f.close()

    def write_empty_group_to_hdf5_direct(self,input_data_path,hdf5filename):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'a')
        data_path_list = [s for s in input_data_path.split('/') if s]
        replace_str=[]
        data_path = ''
        if replace_str == []:            
            data_path = input_data_path
        elif replace_str != []:
            data_path = '/'+ replace_str + '/'
            for i in range(1,len(data_path_list)):
                data_path = data_path + data_path_list[i] + '/'
        f.create_group(data_path)
        f.close()

    def write_attribute_to_hdf5(self,hdf5filename,write_path,attrs_name,attrs_data):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'a')
        f[write_path].attrs[attrs_name] = attrs_data
        f.close()

    def write_fingerprint_attribute_to_hdf5(self,hdf5filename,write_path,attrs_data):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'a')
        f[write_path].attrs['fingerprint'] = attrs_data
        f.close()

    def read_attribute_from_hdf5(self,hdf5filename,read_path,attrs_name):
        filepath = os.path.join(self.filepath, hdf5filename)
        f = h5py.File(filepath, 'r')
        attrs_data = f[read_path].attrs[attrs_name]
        _type = type(f[read_path].attrs[attrs_name])
        f.close()
        return attrs_data,_type

    def obtian_hdf5_attrs_from_hdf5(self,filename):
        filepath = os.path.join(os.path.abspath('./'), filename)        
        hdf5_index_structures = self.read_hdf5_index_structure(filename)
        f = h5py.File(filepath, 'r')
        hdf5_attrs = {}
        for hdf5_index_structure in hdf5_index_structures:
            group ={}
            for attr_key in f[hdf5_index_structure].attrs.keys(): 
                group[attr_key] = f[hdf5_index_structure].attrs[attr_key]
                group[str(attr_key)+'_Type'] = type(f[hdf5_index_structure].attrs[attr_key])
            hdf5_attrs[hdf5_index_structure] = group
        return hdf5_attrs

    def copy_hdf5_attrs(self,read_filename,read_path,write_filename,write_path,attrs_name):
        hdf5_attrs,_type = self.read_attribute_from_hdf5(read_filename,read_path,attrs_name)                    
        if str(_type).find('numpy.float64') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, float(hdf5_attrs))
        elif str(_type).find('numpy.int64') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, np.array([hdf5_attrs]).astype('int64')[0])
        elif str(_type).find('numpy.bool_') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, bool(hdf5_attrs))
        elif str(_type).find('str') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, hdf5_attrs)
        elif str(_type).find('numpy.int32') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, int(hdf5_attrs))
        elif str(attrs_name).find('class') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, hdf5_attrs)    
        elif str(attrs_name).find('module') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, hdf5_attrs)     
        elif str(attrs_name).find('fingerprint') >= 0:
            self.write_attribute_to_hdf5(write_filename, write_path, attrs_name, hdf5_attrs)                                   
        else:
            print('未收录attr格式:'+str(attrs_name))  

    def add_hdf5_attrs_to_hdf5(self,read_filename,add_filename):
        add_filepath = os.path.join(os.path.abspath('./'), read_filename)  
        f_read = h5py.File(add_filepath, 'a')            
        group_names =[]    
        for group_name in f_read.keys():
            if group_name.find('__metadata__') < 0:
                group_names.append(group_name)
        add_hdf5_index_structures = self.read_hdf5_index_structure(add_filename)        
        hdf5_attrs = self.obtian_hdf5_attrs_from_hdf5(read_filename)
        for add_hdf5_index_structure in add_hdf5_index_structures:                    
            try:
                fixed_add_hdf5_index_structure = add_hdf5_index_structure
                if add_hdf5_index_structure not in hdf5_attrs.keys():
                    for group_name in group_names:
                        if group_name[:-1] == add_hdf5_index_structures[:fixed_add_hdf5_index_structure.find('/')-1]:
                            print('1')
                            fixed_add_hdf5_index_structure = group_name + fixed_add_hdf5_index_structure[fixed_add_hdf5_index_structure.find('/'):]
                            print(fixed_add_hdf5_index_structure)
                if hdf5_attrs[fixed_add_hdf5_index_structure] != {}:
                    for name,key in hdf5_attrs[fixed_add_hdf5_index_structure].items():
                        if name.find('_Type') < 0:                       
                            if str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('numpy.float64') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, float(key))
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('numpy.int64') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, np.array([key]).astype('int64')[0])
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('numpy.bool_') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, bool(key))
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('str') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, key)
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('numpy.int32') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, int(key))
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('bytes') >= 0 and str(name).find('fingerprint') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, '679477713289265416993459035469055')                                        
                            elif str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']).find('bytes') >= 0:
                                self.write_attribute_to_hdf5(add_filename, add_hdf5_index_structure, name, key)                            
                            else:
                                print('未收录格式：'+str(fixed_add_hdf5_index_structure)+':'+str(hdf5_attrs[fixed_add_hdf5_index_structure][str(name)+'_Type']))
                else:
                    print(str(add_hdf5_index_structure)+' is empty')
            except:
                print('有key不存在,请查看'+add_hdf5_index_structure)

    def write_dynamical_matrix_sparse_data_to_hdf5(self,hdf5filename,input_symmetrized_numpy_matrix):
        from .matrixeditor import Matrix_Editor
        ME = Matrix_Editor()
        indice,row_start,shape,value = ME.change_symmetrized_numpy_matrix_to_dynamical_matrix_sparse_data(input_symmetrized_numpy_matrix)
        filestr = '/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/'
        self.write_hdf5(filestr+'indices',indice,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'row_starts',row_start,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'shape',shape,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'values',value,hdf5filename,'',1)

    def write_dynamical_matrix_sparse_data_to_hdf5_by_filename(self,hdf5filename,indice,row_start,shape,value):
        filestr = '/DynamicalMatrix_0/dynamical_matrix/matrix_vector/0/'
        self.write_hdf5(filestr+'indices',indice,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'row_starts',row_start,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'shape',shape,hdf5filename,'int32',1)
        self.write_hdf5(filestr+'values',value,hdf5filename,'',1)

    def write_sparse_data_to_hdf5(self,read_filestr,read_hdf5filename,write_filestr,write_hdf5filename):
        from .matrixeditor import Matrix_Editor
        ME=Matrix_Editor()
        if not read_filestr.endswith('/'):
            read_filestr = read_filestr + '/'
        if not write_filestr.endswith('/'):
            write_filestr = write_filestr + '/'                          
        indice,row_start,shape,value = ME.trans_new_numpy_data_to_numpy_data_by_filestr(read_filestr,read_hdf5filename)
        self.write_hdf5(write_filestr+'indices',indice,write_hdf5filename,'int32',1)
        self.write_hdf5(write_filestr+'row_starts',row_start,write_hdf5filename,'int32',1)
        self.write_hdf5(write_filestr+'shape',shape,write_hdf5filename,'int32',1)
        self.write_hdf5(write_filestr+'values',value,write_hdf5filename,'',1)

    def write_essential_data_for_dynamical_matrix(self,hdf5filename,read_hdf5filename,repeat_times):
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','cartesian_coordinates')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','dielectric_regions')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','elements')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','ghost_atoms')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','metallic_regions')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','restart_initial_spin')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/AtomicConfiguration/','tag_data')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/','/MetatextObject')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/DynamicalMatrix_0/Analysis/configuration/','/bravais_lattice')
        atoms_num = len(self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/cartesian_coordinates/array/data',read_hdf5filename))
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/spin',hdf5filename,1)
        self.write_hdf5('/DynamicalMatrix_0/AnalysisSpin/spin_type/data',np.array([1]),hdf5filename,'int64',1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/0',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/1',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/2',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/3',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/4',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/AnalysisSpin/supported_spins/5',hdf5filename,1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/MetatextObject',hdf5filename,1)
        self.write_hdf5('/DynamicalMatrix_0/acoustic_sum_rule/data',np.array([1]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/atomic_displacement/array/data',np.array([0.01]),hdf5filename,'',1)
        self.write_hdf5('/DynamicalMatrix_0/atomic_displacement/unit/data','Ang',hdf5filename,'str',1)
        self.write_hdf5('/DynamicalMatrix_0/constrain_electrodes/data',np.array([0]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/constraints/data',np.array([]),hdf5filename,'',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/compact',np.array([1]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/ni',np.array([int(repeat_times[0])]),hdf5filename,'int32',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/nj',np.array([int(repeat_times[1])]),hdf5filename,'int32',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/nk',np.array([int(repeat_times[2])]),hdf5filename,'int32',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/number_of_orbitals',np.array([int(atoms_num*3)]),hdf5filename,'int32',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/spin_type',np.array([1]),hdf5filename,'int32',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/unit_cell/origo/data',np.array([0.0,0.0,0.0]),hdf5filename,'',1)
        u_data = self.read_hdf5('/BulkConfiguration_0/bravais_lattice/BravaisLattice/convential_vectors/array/data',read_hdf5filename)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/unit_cell/u0/data',np.array([u_data[0].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/unit_cell/u1/data',np.array([u_data[1].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
        self.write_hdf5('/DynamicalMatrix_0/dynamical_matrix/unit_cell/u2/data',np.array([u_data[2].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
        self.write_empty_group_to_hdf5('/DynamicalMatrix_0/finite_difference_method',hdf5filename,1)
        self.write_hdf5('/DynamicalMatrix_0/force_tolerance/array/data',np.array([1.0E-8]),hdf5filename,'',1)
        self.write_hdf5('/DynamicalMatrix_0/force_tolerance/unit/data' ,'Hartree/Bohr**2',hdf5filename,'str',1)
        self.write_hdf5('/DynamicalMatrix_0/processes_per_displacement/data',np.array([1]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/repetitions/0/data',np.array([int(repeat_times[0])]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/repetitions/1/data',np.array([int(repeat_times[1])]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/repetitions/2/data',np.array([int(repeat_times[2])]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/symmetrize/data',np.array([1]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/use_equivalent_bulk/data',np.array([1]),hdf5filename,'int64',1)
        self.write_hdf5('/DynamicalMatrix_0/wigner_seitz/data',np.array([0]),hdf5filename,'int64',1)

    def write_essential_data_for_hamiltonian_derivatives(self,hdf5filename,read_hdf5filename,repeat_times):
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','cartesian_coordinates')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','dielectric_regions')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','elements')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','ghost_atoms')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','metallic_regions')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','restart_initial_spin')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/AtomicConfiguration/','tag_data')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/','/MetatextObject')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/HamiltonianDerivatives_0/Analysis/configuration/','/bravais_lattice')
        atoms_num = len(self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/cartesian_coordinates/array/data',read_hdf5filename))
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/spin',hdf5filename,1)
        self.write_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/spin_type/data',np.array([1]),hdf5filename,'int64',1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/0',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/1',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/2',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/3',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/4',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/AnalysisSpin/supported_spins/5',hdf5filename,1)
        self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/MetatextObject',hdf5filename,1)
        self.write_hdf5('/HamiltonianDerivatives_0/atomic_displacement/array/data',np.array([0.01]),hdf5filename,'',1)
        self.write_hdf5('/HamiltonianDerivatives_0/atomic_displacement/unit/data','Ang',hdf5filename,'str',1)
        self.write_hdf5('/HamiltonianDerivatives_0/constraints/data',np.array([]),hdf5filename,'',1)
        fermi_level = self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/fermi_energy',read_hdf5filename)
        self.write_hdf5('/HamiltonianDerivatives_0/fermi_level/array/data',fermi_level,hdf5filename,'',1)
        self.write_hdf5('/HamiltonianDerivatives_0/fermi_level/unit/data','Hartree',hdf5filename,'str',1)
        electrons_num = self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/number_of_electrons',read_hdf5filename)
        u_data = self.read_hdf5('/BulkConfiguration_0/bravais_lattice/BravaisLattice/convential_vectors/array/data',read_hdf5filename)
        for ij in range(atoms_num*3):
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/compact',np.array([1]),hdf5filename,'int64',1)
            self.write_empty_group_to_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/matrix_vector/0',hdf5filename,1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/ni',np.array([1]),hdf5filename,'int32',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/nj',np.array([1]),hdf5filename,'int32',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/nk',np.array([1]),hdf5filename,'int32',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/number_of_orbitals',np.array([int(electrons_num)*int(repeat_times[0])*int(repeat_times[1])*int(repeat_times[2])]),hdf5filename,'int32',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/spin_type',np.array([1]),hdf5filename,'int32',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/unit_cell/origo/data',np.array([0.0,0.0,0.0]),hdf5filename,'',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/unit_cell/u0/data',np.array([u_data[0].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/unit_cell/u1/data',np.array([u_data[1].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
            self.write_hdf5('/HamiltonianDerivatives_0/hamiltonian_derivative/'+str(ij)+'/unit_cell/u2/data',np.array([u_data[2].astype(float)*1.8897261245650623]).T,hdf5filename,'',1)
        self.write_hdf5('/HamiltonianDerivatives_0/repetitions/0/data',np.array([int(repeat_times[0])]),hdf5filename,'int64',1)
        self.write_hdf5('/HamiltonianDerivatives_0/repetitions/1/data',np.array([int(repeat_times[1])]),hdf5filename,'int64',1)
        self.write_hdf5('/HamiltonianDerivatives_0/repetitions/2/data',np.array([int(repeat_times[2])]),hdf5filename,'int64',1)

    def write_essential_data_for_bulk_configuration(self,hdf5filename,read_hdf5filename,read_new_hdf5filename):
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/Calculator/script/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/Calculator/script/','data')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/','convergence_information') 
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/','kbT')             
        for data_str in ['degeneracy','entropy','entropy_correction','number_of_electrons','spin']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/',data_str)             
        fermi_energy = self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/fermi_levels',read_new_hdf5filename)
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/fermi_energy',fermi_energy[0],hdf5filename,'',1)           
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','configuration')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','matrix_vector')
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','compact')
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','unit_cell')
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/compact',1,hdf5filename,'int32',1)
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/','unit_cell')
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','has_energy_density_matrix_set')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','neighbourlist')        
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','orbital_map')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','matrix_vector')
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','compact')
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','unit_cell')        
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/compact',1,hdf5filename,'int32',1)
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian_container/distributed_hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian_container/distributed_hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/','unit_cell')
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','spin')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/','update_required')      
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/','MetatextObject')      
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/','Parameters')      
        for group_str in ['cartesian_coordinates','dielectric_regions','elements','ghost_atoms','last_updated_bravais_lattice','last_updated_positions','metallic_regions','restart_initial_spin','tag_data']:
            self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',group_str) 
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/BulkConfiguration_0/','MetatextObject')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/',hdf5filename,'/BulkConfiguration_0/','bravais_lattice')

    def write_essential_data_for_bulk_configuration_for_rotate(self,hdf5filename,read_hdf5filename,read_new_hdf5filename,read_rotate_hdf5filename):
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/Calculator/script/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/Calculator/script/','data')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/','convergence_information') 
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/','kbT')             
        for data_str in ['degeneracy','entropy','entropy_correction','number_of_electrons','spin']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/',data_str)             
        fermi_energy = self.read_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/fermi_levels',read_new_hdf5filename)
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/occupation_function/occupation_function/fermi_energy',fermi_energy[0],hdf5filename,'',1)           
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','configuration')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','matrix_vector')
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','compact')
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix_container/density_matrix/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/density_matrix/','unit_cell')
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/compact',1,hdf5filename,'int32',1)
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/hamiltonian/','unit_cell')
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','has_energy_density_matrix_set')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','neighbourlist')        
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','orbital_map')
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','matrix_vector')
        self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','compact')
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/overlap/','unit_cell')        
        self.write_hdf5('/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/compact',1,hdf5filename,'int32',1)
        for data_str in ['ni','nj','nk','number_of_orbitals','spin_type']:
            self.copy_same_data_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian_container/distributed_hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/',data_str)
        self.copy_same_element_in_hdf5(read_new_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian_container/distributed_hamiltonian/sparse_spin_matrix_skeleton/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/selfconsistent_hamiltonian/','unit_cell')
        self.copy_same_data_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/density_matrix_calculator/periodic_schroedinger_container/schroedinger_container/','spin')
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/CalculatorInterface/','update_required')      
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/','MetatextObject')      
        self.copy_same_element_in_hdf5(read_hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/calculator/','Parameters')      
        for group_str in ['cartesian_coordinates','dielectric_regions','elements','ghost_atoms','last_updated_bravais_lattice','last_updated_positions','metallic_regions','restart_initial_spin','tag_data']:
            self.copy_same_element_in_hdf5(read_rotate_hdf5filename,'/BulkConfiguration_1/AtomicConfiguration/',hdf5filename,'/BulkConfiguration_0/AtomicConfiguration/',group_str) 
        self.copy_same_element_in_hdf5(read_rotate_hdf5filename,'/BulkConfiguration_1/',hdf5filename,'/BulkConfiguration_0/','MetatextObject')
        self.copy_same_element_in_hdf5(read_rotate_hdf5filename,'/BulkConfiguration_1/',hdf5filename,'/BulkConfiguration_0/','bravais_lattice')

    def read_mtp_calculate_task_num_from_hdf5(self,read_hdf5filename):
        wanted_data_path = '/mtp/Study/workflow/graph/task_instances/'
        group_structure = self.read_hdf5_group_structure(wanted_data_path,read_hdf5filename)
        GenerateRandomDisplacements_list = []
        for item in group_structure:
            if self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/WorkflowTask/task_id/data',read_hdf5filename).find("GenerateRandomDisplacements") >= 0:
                GenerateRandomDisplacements_list.append(self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/WorkflowTask/task_id/data',read_hdf5filename))
        task_num = 0
        for item in group_structure:
            if self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/WorkflowTask/task_id/data',read_hdf5filename).find("CalculateEnergyForcesStres") >= 0:
                task_num = task_num + (1+self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/bundle_index/data',read_hdf5filename))/self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/number_of_bundles/data',read_hdf5filename)
        task_num =task_num *2-len(GenerateRandomDisplacements_list)-1
        return task_num

    def read_mtp_gen_task_num_from_hdf5(self,read_hdf5filename):
        wanted_data_path = '/mtp/Study/workflow/graph/task_instances/'
        group_structure = self.read_hdf5_group_structure(wanted_data_path,read_hdf5filename)
        GenerateRandomDisplacements_list = []
        for item in group_structure:
            if self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/WorkflowTask/task_id/data',read_hdf5filename).find("GenerateRandomDisplacements") >= 0:
                GenerateRandomDisplacements_list.append(self.read_hdf5('/mtp/Study/workflow/graph/task_instances/'+item+'/WorkflowTask/task_id/data',read_hdf5filename))
        return len(GenerateRandomDisplacements_list)

    def write_essential_data_for_hdf5(self,hdf5filename):
        f_read = h5py.File(os.path.join(os.path.abspath('./'), hdf5filename)  , 'a')            
        group_names =[]    
        for group_name in f_read.keys():
            if group_name.find('__metadata__') < 0:
                group_names.append(group_name)
        essential_data = np.array((group_names), dtype=object)
        self.write_hdf5('/__metadata__/contents',essential_data,hdf5filename,'str',1)

    def gen_hdf5_file_name_by_fix_atoms_list(self,prefix,fix_atoms_list):
        hdf5filename = ''+str(prefix)+'_'
        for item in fix_atoms_list:
            hdf5filename = hdf5filename +str(item) +'_'
        hdf5filename = hdf5filename + '.hdf5'    
        return hdf5filename

    def gen_hdf5_file_name_by_replaced_atoms_list(self,prefix,replaced_atoms_list):
        hdf5filename = ''+str(prefix)+'_'
        for item in replaced_atoms_list:
            hdf5filename = hdf5filename +str(item) +'_'
        hdf5filename = hdf5filename + '.hdf5'    
        return hdf5filename

    def find_repeat_times(self,hdf5filename):
        filestr = '/DynamicalMatrix_0/dynamical_matrix/'
        ni = self.read_hdf5(filestr+'ni',hdf5filename)
        nj = self.read_hdf5(filestr+'nj',hdf5filename)
        nk = self.read_hdf5(filestr+'nk',hdf5filename)
        repeat_times=str(ni)+str(nj)+str(nk)
        return ni,nj,nk,repeat_times

    def find_translation_vectors(self,repeat_times):
        ni = repeat_times[0]
        nj = repeat_times[1]
        nk = repeat_times[2]
        translation_vectors=[]
        for i in range(int(ni)):
            for j in range(int(nj)):
                for k in range(int(nk)):
                    if ni-1 > 0:
                        ii =  i-1                      
                    else:
                        ii = i
                    if nj-1 > 0:
                        jj =  j-1
                    else:
                        jj = j
                    if nk-1 > 0:
                        kk =  k-1
                    else:
                        kk = k
                    translation_vectors.append([ii, jj, kk])
        return translation_vectors

    def find_translation_vectors_index(self,x_index,y_index,z_index,repeat_times):
        full_index = [x_index, y_index, z_index]
        translation_vectors=self.find_translation_vectors(repeat_times)
        obtain_index=0
        for i in range(len(translation_vectors)):
            if full_index == translation_vectors[i]:
                obtain_index = i+1
        return obtain_index
    
