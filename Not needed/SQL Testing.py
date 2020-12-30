from SQL_System import *

data2=[0,0,0,0]
data = SQL_System.decryptData("337965876","Ell10t1324!")


for i in range(0,4):
    data2[i] = SQL_System.vernam(data[i],"Ell10t1324!")


print(data)
print(data2)
