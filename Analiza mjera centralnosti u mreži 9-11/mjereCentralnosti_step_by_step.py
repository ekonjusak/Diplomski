# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 19:40:13 2018

@author: Elizabeta

"""

import numpy as np

A =np.zeros((62,62))  #matrica susjedstva pridruzena teroristickoj mrezi

for z in range(0,4):
    A[z][4]=1

A[3][5]=A[3][9]= A[4][5]=A[4][6]= A[4][8]=A[4][9]=1
A[5][6]=A[5][8]= A[6][7]=A[6][8]=1
A[7][8]=A[8][9]= A[8][10]=A[8][24]=A[8][37]=1
A[9][14]=A[9][22]= A[10][11]=1
A[11][12]=A[11][16]= A[12][13]=A[12][16]=1
A[13][14]=A[13][16]=A[13][18]= A[14][15]=A[14][16]=A[14][17]=A[14][22]=1
A[15][16]=A[16][17:22]=1
A[16][37]=A[22][24]=A[22][37]=1
A[23][24]=A[23][26]=A[24][26:29]=A[24][33:36]=A[24][37]=1
A[25][37]=A[26][35]=A[26][37]=1
A[27][33:36]=A[27][37]=A[28][33:36]=A[28][37]=1
A[29][37]=A[30][35:38]=A[30][40]=1
A[31][32]=A[32][33]=A[32][35]=A[32][37]=1
A[33][34:36]=A[33][37]=A[34][35]=A[34][37]=A[34][45:49]=1
A[35][36:42] = A[35][43]= A[35][46:49]=A[36][37:42]=1
A[37][38:40]=A[37][41:43] = A[37][45:48]= A[37][51]=1
A[38][39:42]=A[39][40:42]= A[39][44]= A[39][47:49]=1
A[40][41]=A[41][60:62]=1
A[42][43]=A[43][44:46]=A[43][51]=A[43][58:60]=1
A[44][47:49]=A[44][59]=A[45][60]=1
A[46][47]=A[46][53]=A[47][48:55]=1
A[48][49:52]=A[49][50:52]=1
A[50][51]= A[50][55:57]= A[51][55:60]=1
A[52][53]=A[53][54]=1
A[55][56]=A[58][59]=1
A[59][60:62]=A[60][61]=1

#dopunjavanje donjeg trokuta u matrici
def simetric(matrix):
    dim = np.size(matrix[0])
    for i in range(0,dim):
        for j in range(i+1,dim):
            matrix[j][i] = matrix[i][j]
    return(matrix)

A = simetric(A)

#-------------------------------------------------#
#stupanj vrha 
def nodeDegree(matrix):
    dim = np.size(matrix[0])
    degreeList=[]
    for i in range(0,dim):
        degreeList.append(sum(matrix[i])) 
    return(degreeList)
    
print(nodeDegree(A))

#-------------------------------------------------#
#local clustering coefficient
#podgrafovski koeficijent zatvorenosti
# 2* broj povezanih susjeda /( d(v)*(d(v)-1) )
 
secondNodes=[]
connectedNodes = []
counter=[]

def allNeighbours(line,matrix):
    dim = np.size(matrix[0]) 
    Nodes = []   
    for j in range(0,dim):
        if matrix[line][j]==1:
            Nodes += [j]
    return(Nodes)

def intersection(list1, list2):
    return list(set(list1) & set(list2))    

#trazim sve susjede i-tog vrha
for i in range(0,62):
    firstNodes = allNeighbours(i,A)
    # gledam susjede susjeda i imaju li zajedniki vrh s početnim vrhom   
    for z in range(0, len(firstNodes)):
        Node = firstNodes[z]   #uzmem vrh od prvih susjeda i trazim susjede
        secondNodes = allNeighbours(Node,A) # susjedi susjeda
        counter.append((len(intersection(firstNodes, secondNodes))))
        secondNodes=[] #broj zajednickih susjeda
    #susjedi se duplaju 2-3 i 3-2 pa ih dijelim s 2   
    connectedNodes.append(sum(counter)/2 )
    counter= []
    
def localClusteringCoef(neighbour, matrix):
    dim = np.size(matrix[0])
    degrees = nodeDegree(A)
    localClusteringCoef = []
    for i in range(0,dim):
        localClusteringCoef.append(round(2*connectedNodes[i]/ (degrees[i]*(degrees[i]-1)),3)) 
    return(localClusteringCoef)
    
print(localClusteringCoef(connectedNodes, A))

#-----------------------------------------------------#

#matrica udaljenosti D 
D=np.zeros((62,62))

for firstNode in range(0,62):
    for lastNode in range(firstNode+1,62):
        count=1
        listOfNodes=allNeighbours(firstNode,A)
        tempList = []
        while lastNode not in listOfNodes:
            for i in listOfNodes:
                tempList = list(set(tempList + allNeighbours(i,A))) 
            count += 1
            listOfNodes=tempList
            tempList= [] 
        D[firstNode][lastNode]=count

D = simetric(D)
print(D)

#-------------------------------------------------#

#katzova centralnost
#x_i = (I - alpha A)^(-1) * beta

lamda = np.linalg.eigvals(A)
print(max(lamda))

beta = np.arange(1,63)
alpha = 1/8
I = np.identity(62) 

katz1 = np.linalg.inv(I- alpha*A)
katz = np.dot(katz1,beta)

for j in katz:
    print(round(j,3))


print(sum(katz)/62)


















