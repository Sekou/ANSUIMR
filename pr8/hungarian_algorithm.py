import numpy as np

#матрица назначений - какому роботу до какого объекта сколько надо проехать
mat = [[12, 8, 14, 10, 24],
       [11, 17, 22, 7, 30],
       [20, 25, 21, 26, 26],
       [11, 17, 18, 15, 8],
       [6, 5, 9, 9, 19]]

#две следующих функции можно трактовать как смещение системы координат в многомерном простарнстве

#упрощение матрицы вдоль строк (приведение дальностей до объектов к минимальной величине)
def reduceRows(mat):
    res=np.array(mat)
    for row in res:
        minv=np.min(row)
        row-=minv
    return res

#упрощение матрицы вдоль колонок (приведение дальностей для роботов к минимальной величине)
def reduceCols(mat):
    res=np.array(mat)
    for ix in range(res.shape[1]):
        minv=np.min(res[:,ix])
        res[:,ix]-=minv
    return res

#список всех нулей
def findZeros(mat):
    res=[]
    for row in mat:
        zz=[i for i, v in enumerate(row) if v==0]
        res.append(zz)
    return res

#число нулей в строке
def getNumZerosInRow(mat, irow):
    return len([v for v in mat[irow] if v==0])

#число нулей в колонке
def getNumZerosInCol(mat, icol):
    return len([v for i, v in enumerate(mat[:,icol]) if v==0])

#матрица зачеркиваний элементов (зачеркиваются "самые простые" назначения)
#matrix for striking out the most simple elements
def getStrikeoutsMat(mat):
    matNew=np.array(mat)
    strikeouts=np.zeros(matNew.shape)
    foundZeros=True
    #вычеркиваем нули на наиболее насыщенных ими линиях
    #we strike out zeros till we can find them
    while foundZeros:
        zerosRows = [getNumZerosInRow(matNew, i) for i in range(matNew.shape[0])]
        zerosCols = [getNumZerosInCol(matNew, i) for i in range(matNew.shape[1])]
        ir=np.argmax(zerosRows)
        ic=np.argmax(zerosCols)
        #вычеркиваем в цикле нули на наиболее зануленных линия
        #we strike out zeros on lines having the most number of zeros
        foundZeros=False
        if zerosRows[ir]>=zerosCols[ic]>0: #whether line has a priority bigger than column for string out
            foundZeros=True
            for i in range(matNew.shape[1]):
                matNew[ir, i]=100500 #forbidding task for robot along row
                strikeouts[ir, i]+=1 #incrementing crossing
        if zerosCols[ic]>zerosRows[ir]>0: #whether column has a priority bigger than line
            foundZeros = True
            for i in range(matNew.shape[0]):
                matNew[i, ic]=100500 #forbidding task for robot along column
                strikeouts[i, ic]+=1 #incrementing crossing
    return strikeouts

#finding minimal value that was not stroked out
def findMinNoncrossedValue(mat, strikeouts):
    pairs = zip(np.array(mat).flatten(), np.array(strikeouts).flatten())
    vals=[a for a, b in pairs if b ==0]
    return min(vals) if len(vals)>0 else -1

#modifying assignments matrix (additional coordinates shift)
def fixMat(mat, strikeouts, minVal):
    matNew=np.array(mat)
    for iy in range(matNew.shape[0]):
        for ix in range(matNew.shape[1]):
            if strikeouts[iy,ix]==0: #no strikeouts
                matNew[iy,ix]-=minVal
            if strikeouts[iy,ix]==2: #double strikeout
                matNew[iy,ix]+=minVal
    return matNew

#finding independent zeros
import itertools
def findIndependentZeroSystems(zeroPositions):
    all_combinations=itertools.product(*zeroPositions)
    unique_combinations=[]
    for combo in all_combinations:
        if len(set(combo))==len(combo):
            unique_combinations.append(list(combo))
    return unique_combinations

def calcComlexity(mat, zeroSystem):
    return sum(mat[i][j] for i,j in enumerate(zeroSystem))

def findAssignments(mat, level=0):
    if level>=9:
        assignments=[]
        for iy in range(mat.shape[0]):
            row=mat[iy]
            row = [(v if not i in assignments else 100500) for i, v in enumerate(row)]
            ix=np.argmin(row)
            assignments.append(ix)
        return assignments

    print("Recursion level: ", level)
    # print("mat0: ", mat)
    mat1=reduceRows(mat)
    # print("mat1: ", mat1)
    mat2=reduceCols(mat1)
    # print("mat2: ", mat2)
    zeroInds=findZeros(mat2)
    # print("zeroInds: ", zeroInds)
    izs = findIndependentZeroSystems(zeroInds)
    # print("IZS: ", izs)
    # we take arbitrarily first independent zero system
    if len(izs)>0: return np.array(izs[0]).flatten().tolist()
    # else: print("Can't find zero system")
    strikeouts = getStrikeoutsMat(mat2)
    # print("strikeouts: ", strikeouts)
    minVal=findMinNoncrossedValue(mat2, strikeouts)
    # print("minVal: ", minVal)
    mat3=fixMat(mat2, strikeouts, minVal)
    # print("mat3: ", mat3)
    #go into recursion
    return findAssignments(mat3, level+1)

    # [[1], [3], [0, 2], [4], [1]] # множество позиций нулей
    # цепочка [1, 3, 2, 4, 1] не является системой независимых нулей, т.к. 1 = 1

# assignments=findAssignments(mat)
# print("Assignments: ", assignments)

# c = calcComlexity(mat, assignments)
# print("Complexity: ", c)