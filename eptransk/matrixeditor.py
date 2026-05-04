import numpy as np

class Matrix_Editor():
    def change_sparse_data_to_numpy_matrix(self,indice,row_start,shape,value):
        row_num = shape[0]
        column_num = shape[1]
        row_index=[]
        for i in range(len(row_start)-1):            
            row_index.append(row_start[i+1]-row_start[i])
        zero_numpy_matrix = np.zeros((row_num,column_num))
        for j in range(len(row_index)):            
            for k in range(row_index[j]):
                start_index = row_start[j]
                zero_numpy_matrix[j][indice[start_index+k]] = value[start_index+k]
        numpy_matrix = zero_numpy_matrix
        return numpy_matrix,shape

    def change_sparse_to_numpy_matrix_by_filestr(self,filestr,hdf5filename):
        from .hdf5editor import HDF5_Editor
        FC=HDF5_Editor()
        if not filestr.endswith('/'):
            filestr = filestr + '/'                
        indice,row_start,shape,value = FC.read_numpy_data_from_hdf5_by_filestr(filestr,hdf5filename)
        row_num = shape[0]
        column_num = shape[1]
        row_index=[]
        for i in range(len(row_start)-1):            
            row_index.append(row_start[i+1]-row_start[i])
        zero_numpy_matrix = np.zeros((row_num,column_num))
        for j in range(len(row_index)):            
            for k in range(row_index[j]):
                start_index = row_start[j]
                zero_numpy_matrix[j][indice[start_index+k]] = value[start_index+k]
        numpy_matrix = zero_numpy_matrix
        return numpy_matrix,shape

    def change_sparse_to_numpy_matrix(self,hdf5filename):
        from .hdf5editor import HDF5_Editor
        FC=HDF5_Editor()
        indice,row_start,shape,value = FC.read_numpy_data_from_hdf5(hdf5filename)
        row_num = shape[0]
        column_num = shape[1]
        row_index=[]
        for i in range(len(row_start)-1):            
            row_index.append(row_start[i+1]-row_start[i])
        zero_numpy_matrix = np.zeros((row_num,column_num))
        for j in range(len(row_index)):            
            for k in range(row_index[j]):
                start_index = row_start[j]
                zero_numpy_matrix[j][indice[start_index+k]] = value[start_index+k]
        numpy_matrix = zero_numpy_matrix
        return numpy_matrix,shape

    def change_symmetrized_numpy_matrix_to_dynamical_matrix_sparse_data(self,input_symmetrized_numpy_matrix):        
        symmetrized_numpy_matrix_row_num = len(input_symmetrized_numpy_matrix)
        symmetrized_numpy_matrix_column_num = len(input_symmetrized_numpy_matrix[0])
        symmetrized_numpy_matrix=np.zeros((symmetrized_numpy_matrix_row_num,symmetrized_numpy_matrix_column_num),dtype='float64')
        symmetrized_numpy_matrix[:,:] = input_symmetrized_numpy_matrix[:,:]
        total_blocks = int(symmetrized_numpy_matrix_column_num/symmetrized_numpy_matrix_row_num)
        mid_block_index = int((total_blocks+1)/2)
        mid_block = symmetrized_numpy_matrix[:,(mid_block_index-1)*symmetrized_numpy_matrix_row_num:(mid_block_index)*symmetrized_numpy_matrix_row_num]
        for i in range(1,symmetrized_numpy_matrix_row_num):
            for j in range(i):
                mid_block[i,j] = 0      
        for j in range(mid_block_index-1):
            original_left_block = symmetrized_numpy_matrix[:,j*symmetrized_numpy_matrix_row_num:(j+1)*symmetrized_numpy_matrix_row_num]
            original_right_block = symmetrized_numpy_matrix[:,(total_blocks-j-1)*symmetrized_numpy_matrix_row_num:(total_blocks-j)*symmetrized_numpy_matrix_row_num]
            for k in range(1,symmetrized_numpy_matrix_row_num):
                for l in range(k):
                    original_left_block[k,l] = 0
                    original_right_block[k,l] = 0                          
        sparse_numpy_matrix = symmetrized_numpy_matrix
        indice = []
        value = []
        row_start = []
        count_num = 0
        for i in range(len(sparse_numpy_matrix)):            
            row_start.append(count_num)
            for j in range(len(sparse_numpy_matrix[0])):
                if sparse_numpy_matrix[i,j] != 0:
                    indice.append(j)
                    value.append(sparse_numpy_matrix[i,j])
                    count_num=count_num+1
        row_start.append(len(indice))
        indice = np.array(indice)
        value = np.array(value)
        row_start = np.array(row_start)
        shape = np.array([symmetrized_numpy_matrix_row_num,symmetrized_numpy_matrix_column_num])
        return indice,row_start,shape,value

    def change_symmetrized_numpy_matrix_to_dynamical_matrix_sparse_data_atk(self,input_symmetrized_numpy_matrix):        
        symmetrized_numpy_matrix_row_num = len(input_symmetrized_numpy_matrix)
        symmetrized_numpy_matrix_column_num = len(input_symmetrized_numpy_matrix[0])
        symmetrized_numpy_matrix=np.zeros((symmetrized_numpy_matrix_row_num,symmetrized_numpy_matrix_column_num),dtype='float64')
        symmetrized_numpy_matrix[:,:] = input_symmetrized_numpy_matrix[:,:]
        total_blocks = int(symmetrized_numpy_matrix_column_num/symmetrized_numpy_matrix_row_num)
        mid_block_index = int((total_blocks+1)/2)
        mid_block = symmetrized_numpy_matrix[:,(mid_block_index-1)*symmetrized_numpy_matrix_row_num:(mid_block_index)*symmetrized_numpy_matrix_row_num]
        for i in range(1,symmetrized_numpy_matrix_row_num):
            for j in range(i):
                mid_block[i,j] = 0      
        for j in range(mid_block_index-1):
            original_left_block = symmetrized_numpy_matrix[:,j*symmetrized_numpy_matrix_row_num:(j+1)*symmetrized_numpy_matrix_row_num]
            original_right_block = symmetrized_numpy_matrix[:,(total_blocks-j-1)*symmetrized_numpy_matrix_row_num:(total_blocks-j)*symmetrized_numpy_matrix_row_num]
            for k in range(1,symmetrized_numpy_matrix_row_num):
                for l in range(k):
                    original_left_block[k,l] = 0
                    original_right_block[k,l] = 0               
        sparse_numpy_matrix = symmetrized_numpy_matrix
        indice = []
        value = []
        row_start = []
        count_num = 0
        for i in range(len(sparse_numpy_matrix)):            
            row_start.append(count_num)
            start_tag = 0
            for j in range(len(sparse_numpy_matrix[0])):
                if sparse_numpy_matrix[i,j] == 0 and start_tag == 1:
                    indice.append(j)
                    value.append(sparse_numpy_matrix[i,j])
                    count_num=count_num+1
                    start_tag = 0
                elif sparse_numpy_matrix[i,j] != 0 and start_tag == 0:        
                    indice.append(j)
                    value.append(sparse_numpy_matrix[i,j])
                    count_num=count_num+1
                    start_tag = 1
                elif sparse_numpy_matrix[i,j] != 0 and start_tag == 1:                    
                    indice.append(j)
                    value.append(sparse_numpy_matrix[i,j])
                    count_num=count_num+1
        row_start.append(len(indice))
        indice = np.array(indice)
        value = np.array(value)
        row_start = np.array(row_start)
        shape = np.array([symmetrized_numpy_matrix_row_num,symmetrized_numpy_matrix_column_num])
        return indice,row_start,shape,value

    def add_across_data_to_numpy_matrix_for_dynamical_matrix(self,numpy_matrix):
        numpy_matrix_row_num = len(numpy_matrix)
        numpy_matrix_column_num = len(numpy_matrix[0])        
        total_blocks = int(numpy_matrix_column_num/numpy_matrix_row_num)
        mid_block_index = int((total_blocks+1)/2)        
        mid_block = numpy_matrix[:,(mid_block_index-1)*numpy_matrix_row_num:(mid_block_index)*numpy_matrix_row_num]
        mid_block_T = mid_block.T
        completed_mid_block = mid_block + mid_block_T
        for k in range(len(completed_mid_block)):
            completed_mid_block[k,k] =completed_mid_block[k,k]/2
        numpy_matrix[:,(mid_block_index-1)*numpy_matrix_row_num:(mid_block_index)*numpy_matrix_row_num] = completed_mid_block
        for i in range(mid_block_index-1):
            original_left_block = numpy_matrix[:,i*numpy_matrix_row_num:(i+1)*numpy_matrix_row_num]
            original_right_block = numpy_matrix[:,(total_blocks-i-1)*numpy_matrix_row_num:(total_blocks-i)*numpy_matrix_row_num]
            original_left_block_T = original_left_block.T
            original_right_block_T = original_right_block.T
            completed_left_block = original_left_block + original_left_block_T
            completed_right_block = original_right_block + original_right_block_T
            for k in range(len(completed_left_block)):
                completed_left_block[k,k] =completed_left_block[k,k]/2
            for l in range(len(completed_right_block)):
                completed_right_block[l,l] =completed_right_block[l,l]/2
            numpy_matrix[:,i*numpy_matrix_row_num:(i+1)*numpy_matrix_row_num] = completed_left_block
            numpy_matrix[:,(total_blocks-i-1)*numpy_matrix_row_num:(total_blocks-i)*numpy_matrix_row_num] = completed_right_block
        completed_numpy_matrix = numpy_matrix
        return completed_numpy_matrix

    def add_across_data_to_numpy_matrix_for_hamiltonian(self,numpy_matrix):
        numpy_matrix_row_num = len(numpy_matrix)
        numpy_matrix_column_num = len(numpy_matrix[0])        
        total_blocks = int(numpy_matrix_column_num/numpy_matrix_row_num)
        mid_block_index = int((total_blocks+1)/2)
        mid_block = numpy_matrix[:,(mid_block_index-1)*numpy_matrix_row_num:(mid_block_index)*numpy_matrix_row_num]
        mid_block_T = mid_block.T
        completed_mid_block = mid_block + mid_block_T
        for k in range(len(completed_mid_block)):
            completed_mid_block[k,k] =completed_mid_block[k,k]/2
        numpy_matrix[:,(mid_block_index-1)*numpy_matrix_row_num:(mid_block_index)*numpy_matrix_row_num] = completed_mid_block
        return completed_mid_block

    def trans_new_numpy_data_to_numpy_data_by_filestr(self,filestr,read_hdf5filename):
        from .hdf5editor import HDF5_Editor
        FC=HDF5_Editor()
        if not filestr.endswith('/'):
            filestr = filestr + '/'                
        indices = FC.read_hdf5_wanted_data(filestr,'indices',read_hdf5filename)
        indice = []
        value = []
        row_start = [0]
        row_start_num = 0
        for i in range(len(indices)):
            row_start_num = row_start_num + len(FC.read_hdf5(filestr+'indices'+str(i),read_hdf5filename))
            indice.extend(FC.read_hdf5(filestr+'indices'+str(i),read_hdf5filename))
            value.extend(FC.read_hdf5(filestr+'values'+str(i),read_hdf5filename))
            row_start.append(row_start_num)
        shape = FC.read_hdf5(filestr+'shape',read_hdf5filename)
        indice = np.array(indice)
        value = np.array(value)
        row_start = np.array(row_start)
        return indice,row_start,shape,value
    
    def change_sparse_complex_data_to_numpy_matrix(self,data,indices,indptr,shape):
        rows_num, cols_num = shape
        completed_numpy_matrix = np.zeros(shape, dtype=data.dtype)
        for i in range(rows_num):
            start = indptr[i]
            end = indptr[i+1]
            for j in range(start, end):
                col = indices[j]
                completed_numpy_matrix[i, col] = data[j]
        return completed_numpy_matrix
