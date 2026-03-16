from itertools import permutations, combinations


def arrange(n: int) -> list:
    """Return all permutations of 1..n as a list."""
    return list(permutations(range(1, n + 1)))


def combine(n: int, m: int) -> list:
    """Return all m-length combinations of 1..n as a list."""
    return list(combinations(range(1, n + 1), m))


def solve(arg_mat, constant_vec) -> list:
    """Solve a linear system using Cramer's rule for the given matrix and constant vector."""
    result = []
    if not arg_mat.det:
        raise ValueError("Singular matrix")
    for n in range(len(arg_mat)):
        d_mat = []
        for i in range(len(arg_mat.transpose)):
            if i != n:
                d_mat.append(arg_mat.transpose[i])
            else:
                d_mat.extend(constant_vec.transpose.value)
        result.append(Matrix(d_mat).det / arg_mat.det)
    return result


def count_n(arrangement: list) -> int:
    """Count the number of inversions in a given permutation list."""
    result = 0
    for i in range(len(arrangement)):
        for j in range(i):
            result += 1 if arrangement[j] > arrangement[i] else 0
    return result


class Matrix(list):
    def __init__(self, value: list):
        """Create a matrix from a list of equal-length row lists."""
        if len({len(value[i]) for i in range(len(value))}) == 1:
            self.i, self.j = len(value), len(value[0])
            self.is_square = self.i == self.j
            self.value = value
            super().__init__(self.value)
        else:
            raise ValueError("This object cannot be as a matrix")

    def __str__(self) -> str:
        """Return a pretty-printed string representation with dimensions and values."""
        string = f'\n{self.__class__.__name__}({self.i}×{self.j})=\n'
        for i in range(self.i):
            for j in range(self.j):
                string += f'{self[i][j]:<20.4f}'
            string += '\n'
        return string

    def __neg__(self):
        return Matrix([[self[i][j] * (-1) for j in range(self.j)] for i in range(self.i)])

    def __add__(self, other):
        if type(other) not in [Vector, Matrix]:
            raise TypeError(f'Cannot add {type(self)} object and {type(other)} object')
        elif other.i != self.i or other.j != self.j:
            raise ValueError(f'Cannot add {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
        else:
            return Matrix([[self[i][j] + other[i][j] for j in range(self.j)] for i in range(self.i)])

    def __sub__(self, other):
        if type(other) not in [Vector, Matrix]:
            raise TypeError(f'Cannot sub {type(self)} object and {type(other)} object')
        elif other.i != self.i or other.j != self.j:
            raise ValueError(f'Cannot sub {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
        else:
            return Matrix([[self[i][j] - other[i][j] for j in range(self.j)] for i in range(self.i)])

    def __mul__(self, other):
        if type(other) in [float, int, complex]:
            return Matrix([[self[i][j] * other for j in range(self.j)] for i in range(self.i)])
        elif type(other) in [Matrix, Vector]:
            if self.j != other.i:
                raise ValueError(f'Cannot multiply {self.i}*{self.j} matrix and {other.i}*{other.j} matrix')
            else:
                array = []
                for i in range(self.i):
                    row = []
                    for j in range(other.j):
                        vector_r, vector_c = self[i], other.transpose[j]
                        row.append(sum([vector_r[a] * vector_c[a] for a in range(len(vector_r))]))
                    array.append(row)
                return Matrix(array)
        else:
            TypeError(f'Cannot multiply {type(self)} object and {type(other)} object')

    @property
    def det(self) -> int | float:
        """Compute the determinant of a square matrix using Gaussian elimination."""
        if not self.is_square:
            raise ValueError('Is not a square matrix')
        mat = [row[:] for row in self.value]
        n, det, sign = self.i, 1.0, 1
        for col in range(n):
            pivot_row = None
            for row in range(col, n):
                if abs(mat[row][col]) > 1e-12:
                    pivot_row = row
                    break
            if pivot_row is None:
                return 0.0
            if pivot_row != col:
                mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
                sign *= -1
            pivot = mat[col][col]
            det *= pivot
            for row in range(col + 1, n):
                factor = mat[row][col] / pivot
                for c in range(col + 1, n):
                    mat[row][c] -= factor * mat[col][c]
                mat[row][col] = 0.0
        return det * sign

    @property
    def rank(self) -> int:
        """Return the rank of the matrix by checking all sub-determinants."""
        n, rank = 1, 0
        while any(self.sub_determinant_list(n)) and n <= min(self.j, self.i):
            rank += 1
            n += 1
        return rank

    def sub_determinant_list(self, n) -> list:
        """Return the list of all n×n sub-determinants of the matrix."""
        all_possibilities = []
        sub_index_list_i = combine(self.i, n)
        sub_index_list_j = combine(self.j, n)
        for i_list in sub_index_list_i:
            for j_list in sub_index_list_j:
                all_possibilities.append(Matrix([[self[_i-1][_j-1] for _j in j_list] for _i in i_list]).det)
        return all_possibilities

    def algebraic_complement(self, i, j) -> int | float:
        """Compute the algebraic complement (cofactor) at position (i, j)."""
        i_list = [m for m in range(self.i) if m != i - 1]
        j_list = [n for n in range(self.j) if n != j - 1]
        return Matrix([[(-1) ** (_i + _j) * self[_i][_j] for _j in j_list] for _i in i_list]).det

    @property
    def transpose(self):
        """Return the transpose of the matrix as a new Matrix instance."""
        new_value = [[self[j][i] for j in range(self.i)] for i in range(self.j)]
        return Matrix(new_value)

    @property
    def adj(self):
        """Return the adjugate matrix (transpose of the cofactor matrix)."""
        return Matrix(
            [[self.algebraic_complement(i + 1, j + 1) for j in range(self.j)] for i in range(self.i)]).transpose

    @property
    def inv(self):
        """Return the inverse of the matrix if it is non-singular and square."""
        if not self.is_square:
            raise ValueError('Is not a square matrix')
        elif self.det == 0:
            raise ValueError('Singular matrix')
        else:
            return self.adj * (1 / self.det)

    def exchange(self, method, *tar) -> None:
        """Exchange two rows or columns in place based on method ('r' or 'c')."""
        if method == 'r':
            self[tar[0] - 1], self[tar[1] - 1] = self[tar[1] - 1], self[tar[0] - 1]
        elif method == 'c':
            mat_t = self.transpose
            mat_t[tar[0] - 1], mat_t[tar[1] - 1] = mat_t[tar[1] - 1], mat_t[tar[0] - 1]
            super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def mul_k(self, method, index, k) -> None:
        """Multiply a row or column by a scalar in place."""
        if method == 'r':
            for i in range(len(self[index-1])):
                self[index-1][i] *= k
        elif method == 'c':
            mat_t = self.transpose
            for i in range(len(mat_t[index-1])):
                mat_t[index-1][i] *= k
            super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def add_vector(self, method, i, j, k) -> None:
        """Add k times one row or column vector to another in place."""
        if method == 'r':
            for _i in range(self.j):
                self[i-1][_i] += k * self[j-1][_i]
        elif method == 'c':
            mat_t = self.transpose
            for _i in range(self.j):
                mat_t[i-1][_i] += k * mat_t[j-1][_i]
            super().__init__(mat_t.transpose)
        else:
            raise ValueError('Unsupported function')

    def mat_append(self, method, other):
        """Append another matrix or vector horizontally or vertically depending on method."""
        if type(other) in [Vector, Matrix]:
            if method == 'r' and self.i == other.i:
                return Matrix([self[_i] + other[_i] for _i in range(self.i)])
            if method == 'c' and self.j == other.j:
                return Matrix(self.value + other.value)
            else:
                raise ValueError('Unsupported opi')
        else:
            raise TypeError(f'Can not use {type(other)}')


class Vector(Matrix):
    def __init__(self, value, is_t=0):
        """Create a column or row vector based on the value and transpose flag."""
        if is_t:
            value = [list(value)]
        else:
            value = [[i] for i in value]
        super().__init__(value)
