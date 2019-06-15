import numpy as np 
import math

input_txt_path = "input.txt"
output_txt_path = "output.txt"
matricula = "16110640"


def set_matrices(aux, n, m, length):
    matrix = np.zeros((length, length))
    for i in range(n):
        for j in range(m):
            matrix[i][j] = aux[i][j]
    return matrix        
    		
    		
    		
    		
    		
    	

def set_submatrices(matrix_a, matrix_b, length):
    a11 =  np.empty([length, length], dtype="int"); a12 =  np.empty([length, length], dtype="int")
    a21 =  np.empty([length, length], dtype="int"); a22 =  np.empty([length, length], dtype="int")
   
    b11 =  np.empty([length, length], dtype="int"); b12 =  np.empty([length, length], dtype="int")
    b21 =  np.empty([length, length], dtype="int"); b22 =  np.empty([length, length], dtype="int")
    
    for i in range(length):
        for j in range(length):
        	
            a11[i][j] = matrix_a[i][j]
            a12[i][j] = matrix_a[i][j+length]
            a21[i][j] = matrix_a[i + length][j]
            a22[i][j] = matrix_a[i + length][j + length]
            
            b11[i][j] = matrix_b[i][j]
            b12[i][j] = matrix_b[i][j + length]
            b21[i][j] = matrix_b[i + length][j]
            b22[i][j] = matrix_b[i + length][j + length]

    return a11, a12, a21, a22, b11, b12, b21, b22




def set_c(c11, c12, c21, c22, length):
    C = np.empty([length*2, length*2], dtype ="int")
    for i in range(length):
        for j in range(length):
            C[i][j] = c11[i][j]
            C[i][j + length] = c12[i][j]
            C[i + length][j] = c21[i][j]
            C[i+length][i+length] = c22[i][j] 

    return C

def strassen(matrix_a, matrix_b, length):

    if length == 1:
        return [[matrix_a[0][0] * matrix_b[0][0]]]
    
    (a11, a12, a21, a22, b11, b12, b21, b22) = set_submatrices(matrix_a, matrix_b, int(length/2))

    s1 = np.subtract(b12, b22); s2 = np.add(a11, a12); s3 = np.add(a21, a22); s4 = np.subtract(b21, b11)
    s5 = np.add(a11, a22); s6 = np.add(b11, b22); s7 = np.subtract(a12, a22); s8 = np.add(b21, b22)
    s9 = np.subtract(a11, a21); s10 = np.add(b11, b12)

    p1 = strassen(a11, s1, length/2)
    p2 = strassen(s2, b22, length/2)
    p3 = strassen(s3, b11, length/2)
    p4 = strassen(a22, s4, length/2)
    p5 = strassen(s5, s6, length/2)
    p6 = strassen(s7, s8, length/2)
    p7 = strassen(s9, s10, length/2)
    
    c11 = np.add(np.subtract(p4, p2), np.add(p5, p6)); c12 = np.add(p1, p2); c21 = np.add(p3, p4)
    c22 = np.add(p5, np.subtract(np.subtract(p1, p3), p7))

    return set_c(c11, c12, c21, c22, int(length/2))  



input = open(input_txt_path, 'r')
n1, m1, n2, m2 = list(map(int, input.readline().split()))
A = []; B = []

if m1 != n2:
	print("Erro!\nAs matrizes não são multiplicáveis.")
	exit()
			
length = max(n1, m1, m2)
length = 2 ** math.ceil(math.log2(length))
A = []
B = []

for i in range(n1):
    A.append(list(map(int, input.readline().split())))

for i in range(n2):
    B.append(list(map(int, input.readline().split())))	

A = set_matrices(A, n1, m1, length)
B = set_matrices(B, n2, m2, length)

C = strassen(A, B, length)

output = open(output_txt_path, 'w')
output.write("{}".format(matricula))
output.write("\n  {} {}".format(n1, m2))

for i in range(n1):
    output.write("\n ")
    for j in range(m2):
        output.write(" {}".format(C[i][j]))

input.close

