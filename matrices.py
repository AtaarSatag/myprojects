class Matrix():
    
    class DataFormatError(Exception):
        pass

    def __init__(self, data):
        self.matrix = data 
        self.row_num = len(data)
        check_row = len(data[0])
        for row in data:
            if check_row == len(row):
                continue
            else:
                raise self.DataFormatError('Rows of the data are different.')
        self.col_num = len(data[0])
    
    def show(self):
        for row in self.matrix:
            for col in row:
                print(col, ' ', end='')
            print()
    
    def get_matrix_col(self, col_ind):
        if col_ind > len(self.matrix[0])-1:
            raise IndexError('Entered column index is out of column range') 
        else:
            column = []
            for row_ind in range(len(self.matrix)):
                column.append(self.matrix[row_ind][col_ind])
            return column
    
    def transpose(self):
        trans_matrix = []
        for col_ind in range(self.col_num):
            trans_matrix.append(self.get_matrix_col(col_ind))
        return Matrix(trans_matrix)

    def __calculate_matrix_element(self, first_matrix_row: list, second_matrix_col: list):
        element = 0
        for i in range(len(first_matrix_row)):
            element += first_matrix_row[i] * second_matrix_col[i]
        return element

    def __mul__(first, second):
        if type(first) == Matrix and type(second) == Matrix:
            if first.row_num == second.col_num:
                matrix = []
                for row_ind in range(first.row_num):
                    matrix.append([])
                    for col_ind in range(second.col_num):
                        second_matrix_col = second.get_matrix_col(col_ind)
                        element = first.__calculate_matrix_element(first.matrix[row_ind], second_matrix_col)
                        matrix[row_ind].append(element)
                return Matrix(matrix)
            else:
                raise self.DataFormatError('Your matrices are incompatible.')
        else:
            if type(first) == Matrix:
                for row_ind in range(first.row_num):
                    for col_ind in range(first.col_num):
                        first.matrix[row_ind][col_ind] = second * first.matrix[row_ind][col_ind]
                return Matrix(first.matrix)
            else:
                for row_ind in range(second.row_num):
                    for col_ind in range(second.col_num):
                        second.matrix[row_ind][col_ind] = first * second.matrix[row_ind][col_ind]
                return Matrix(second.matrix)

    def __truediv__(first, second):
        if type(first) == Matrix:
            for row_ind in range(first.row_num):
                for col_ind in range(first.col_num):
                    first.matrix[row_ind][col_ind] = first.matrix[row_ind][col_ind] / second
            return Matrix(first.matrix)
        else:
            for row_ind in range(second.row_num):
                for col_ind in range(second.col_num):
                    second.matrix[row_ind][col_ind] = second.matrix[row_ind][col_ind] / first
            return Matrix(second.matrix)

    def __add__(first, second):
        if (first.row_num == second.row_num
                         and first.col_num == second.col_num):
            matrix_sum = []
            for row_ind in range(first.row_num):
                matrix_sum.append([])
                for col_ind in range(first.col_num):
                    matrix_sum[row_ind].append(
                                               first.matrix[row_ind][col_ind]
                                               +second.matrix[row_ind][col_ind]
                                               )
            return Matrix(matrix_sum)
        else:
            raise self.DataFormatError('Your matrices have different shapes.')

    def __sub__(first, second):
        if (first.row_num == second.row_num
                         and first.col_num == second.col_num):
            matrix_sum = []
            for row_ind in range(first.row_num):
                matrix_sum.append([])
                for col_ind in range(first.col_num):
                    matrix_sum[row_ind].append(
                                               first.matrix[row_ind][col_ind]
                                               -second.matrix[row_ind][col_ind]
                                               )
            return Matrix(matrix_sum)
        else:
            raise self.DataFormatError('Your matrices have different shapes.')


#data_1 = [[2, 16, 0], [-4, 24, 3]]
#data_2 = [[2, 16], [3, 24], [13, 4]]
#data_3 = [[4, 20, 5], [-7, 11, 2]]
#num = 10
#
#mat_1 = Matrix(data_1)
#mat_2 = Matrix(data_2)
#mat_3 = Matrix(data_3)
#
#(mat_1 * mat_2).show()
#(mat_1 * 10).show()
#(mat_1 + mat_3).show()
#(mat_1 - mat_3).show()
#(mat_1 / 3).show()
#mat_1.transpose().show()
