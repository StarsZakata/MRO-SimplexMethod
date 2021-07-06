import numpy as np
import sys

# Функция поиска базовых переменных и их Коэффициентов
def basis(m, n, source, C):
    pre_basis1 = []
    pre_basis2 = []
    basis = []                                   # Порядок базисных переменных
    for j in range(n):
        pre_basis1.append(0)
        pre_basis2.append(0)
        for i in range(m):
            pre_basis1[j] += abs(source[i][j])
            pre_basis2[j] += source[i][j]

    for j in range(len(pre_basis1)):
        if pre_basis2[j] == -1:
            pre_basis1[j] = -1
        if pre_basis1[j] == 1:
            basis.append(j)
    print("basis = ", basis)

    Cb = []                                      # Коэффициенты при базисных переменных в целевой функции
    for i in range(m):
        if basis[i] <= (len(C) - 1):
            Cb.append(C[basis[i]])
    print("Cb = ", Cb)
    return basis, Cb
# Функция, определяющая разрешающую строку
def teta_column(m, A, matrix, mainCol):
        teta = []  # Массив симплексных отношений
        mainRow = 0
        minValue = sys.maxsize
        for i in range(m):
            if matrix[:, mainCol][i] != 0:
                teta.append(round(A[i] / matrix[:, mainCol][i], 2))
            else:
                teta.append(-1)  # если делим на 0, то ставим -1, как бы прочерк
            if 0 < teta[i] < minValue:
                minValue = teta[i]
                mainRow = i
        print('teta = ', teta)
        print("mainRow = ", mainRow)
        return mainRow
#Функция проверки типа Задачи
def M_task(m, n, source, C):
    #поиск строки и столбца(Почему через 1?)
    column_with_one = []
    row_with_one = []
    for j in range(n):
        for i in range(m):
            if source[i][j] == 1:
                row_with_one.append(i) #строка
                column_with_one.append(j) #столбец
    #Поиск суммы столбцов
    sum_of_column = []
    for j in range(len(column_with_one)):
        sum_of_column.append(0)
        for i in range(m):
            sum_of_column[j] += abs(source[i][column_with_one[j]])
    #Поиск суммы строк и определение, есть-ли в уравнении добавочная переменная
    row_i = []
    for i in range(len(sum_of_column)):
        if (sum_of_column[i] != 1) or (sum_of_column[i]==1):
            row_i.append(i)
    if ((len(row_i) == 0)) and (len(row_i)!=m):
        print("Матрица имеет предпочтительный вид")
    else:
        print("Матрица не имеет предпочтительного вида, переходим к М-задаче")
        #новая матрица заполненная нулями и добавлением добавочной части к нашей исходной матрице
        M_z = np.zeros((m, m-len(row_i)))
        for j in range(m):
            k=0
            for i in range(n):
                if (source[j][i] <=0.9) and (source[j][i]>=1.1):
                 k=j
        print("Строка добавления М задачи = ", k)
# Функция, определяющая разрешающий столбец
def score_line(m, n, C, Cb, matrix, flag):
    f = []  # Массив значений оценочной строки
    f_M = []  # Массив значений дополнительной оценойчной строки для М - задачи

    for i in range(n):
        f.append(0)
        f_M.append(0)
        for j in range(m):
            if Cb[j] == M:
                f_M[i] += Cb[j] * matrix[:, i][j]
            else:
                f[i] += Cb[j] * matrix[:, i][j]
        if C[i] == M:
            f_M[i] -= C[i]
        else:
            f[i] -= C[i]
    print("f = ", f)
    print("f_M = ", f_M)
    mainCol1 = 0
    mainCol2 = 0
    for j in range(n):
        if f[j] > 0:
            mainCol1 = f.index(max(f))
        if f_M[j] > 0:
            mainCol2 = f_M.index(max(f_M))
            print("mainCol = ", mainCol2)
            return mainCol2, flag
    if max(f) > max(f_M):
        print("mainCol = ", mainCol1)
        return mainCol1, flag
    elif max(f) < max(f_M):
        print("mainCol = ", mainCol2)
        return mainCol2, flag
    else:
        flag = False
        return mainCol1, flag
# Функция, составляющая новую симплексную таблицу
def new_table(m, n, mainRow, mainCol, mainVar, matrix, A, Cb, C, basis):
    new_table = np.zeros((m, n))
    new_A = []

    for i in range(m):
        if i != mainRow:
            for j in range(n):
                if j != mainCol:
                    new_table[i][j] = round(
                        (matrix[i][j] * mainVar - matrix[i][mainCol] * matrix[mainRow][j]) / mainVar, 1)
            new_table[:, mainCol][i] = 0
            new_A.append(round((A[i] * mainVar - A[mainRow] * matrix[i][mainCol]) / mainVar, 1))
        else:
            new_A.append(round(A[mainRow] / mainVar, 1))
    for j in range(n):
        new_table[mainRow][j] = round(matrix[mainRow][j] / mainVar, 1)
    new_table[:, basis[mainRow]] = 0
    Cb[mainRow] = C[mainCol]
    basis[mainRow] = C.index(C[mainCol])
    print("Новая матрица")
    print(new_table)
    return new_table, new_A, Cb, basis

m = 3
n = 4  
M = 1
C = [3, -2, 4, 0]                        
a = [2, -2, 0, 0]                         
b = [3, 4, 0, -1]                           
c = [-4, 0, 1, 0]                          
A = [4, 6, 7]                                    
source = np.zeros((m, n))                        
source[0] = a
source[1] = b
source[2] = c

print("Исходная матрица")
print(source)
print()
source, n, C = M_task(m, n, source, C)
basis, Cb = basis(m, n, source, C)
flag = True
mainCol, flag = score_line(m, n, C, Cb, source, flag)   #Разрешающий столбец
mainRow = teta_column(m, A, source, mainCol)            #Разрешающая строка
mainVar = source[mainRow][mainCol]                      #Разрешающий элемент
print("mainVar = ", mainVar)

i = 0
while flag:
    i += 1
    print("------------------------------------------------------------")
    print(i, "я итерация")
    source, A, Cb, basis = new_table(m, n, mainRow, mainCol, mainVar, source, A, Cb, C, basis)
    mainCol, flag = score_line(m, n, C, Cb, source, flag)
    if not flag:
        break
    mainRow = teta_column(m, A, source, mainCol)
    mainVar = source[mainRow][mainCol]
    print("mainVar = ", mainVar)
print()
print("basis = ", basis)
result = []
for j in range(n):
    result.append(0)
for i in range(m):
    result[basis[i]] = A[i]
print("result = ", result)
z = 0
for i in range(m):
    z += Cb[i] * A[i]
print("z = ", round(z, 1))

#Поиск необходимой строки
for i in range(m-len(row_i)):
      M_z[k] = 1
M_z[0][1]=0
M_z[1][1]=1
source = np.column_stack((source, M_z))
n = len(source.T)
for i in range(len(row_i)):
    C.append(M)
C.append(1)
print("C = ", C)
print()
print("Матрица предпочтительного вида")
print(source)
return source, n, C


