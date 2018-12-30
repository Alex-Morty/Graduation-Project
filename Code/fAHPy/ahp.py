import csv
import numpy as np
import tensorflow as tf
#大概的思路是：
#1.首先输入每个指标下面对应的对比矩阵，每个这个矩阵是由专家比较每两个
#指标之间的相对性重要性形成的，将这个矩阵作为输入，首先计算这个矩阵是否能
#通过一致性的检验。在计算一致性时，要先求出该矩阵的特征值和特征向量。
'''c1,c2 = np.linalg.eig(C)
print (c1)
# [ 2. 1.] 
print (c2)
#[[ 0.89442719 0.70710678]
# [ 0.4472136 0.70710678]]'''
class AHP:
	def __init__(self,array):
		self.row = len(array)
		self.col = len(array[0])
	def get_tezheng(self,array):#获取特征值和特征向量
			te_val ,te_vector = np.linalg.eig(array)
			list1=list(te_val)
			print("特征值为：",te_val)
			print("特征向量为：",te_vector)
			#得到最大特征值对应的特征向量
			max_val = np.max(list1)
			index = list1.index(max_val)
			max_vector = te_vector[:,index]
			print("最大的特征值:"+str(max_val)+"   对应的特征向量为："+str(max_vector))
			return max_val,max_vector

	def RImatrix(self,n):#建立RI矩阵
			d = {}
			n1 = [1,2,3,4,5,6,7,8,9]
			n2 = [0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45]
			for i in range(n):
				d[n1[n]] = n2[n]
			print("该矩阵在一致性检测时采用的RI值为：",d[n1[n]])
			return d[n1[n]]

	def test_consitstence(self,max_val,RI):#测试一致性
			CI = (max_val-self.row)/(self.row-1)
			CR = CI/RI
			if  CR < 0.10 :
				print("判断矩阵的CR值为  "+str(CR) + "通过一致性检验")
				return True
			else:
				print("判断矩阵的CR值为  "+str(CR) + "判断矩阵未通过一致性检验，请重新输入判断矩阵")
				return False  
		    
	def normalize_vector(self,max_vector):#特征向量归一化
			vector_after_normalization=[]
			sum0 = np.sum(max_vector)
			for i in range(len(max_vector)):
				vector_after_normalization.append(max_vector[i]/sum0)
			print("该级指标的权重权重矩阵为：  "+str(vector_after_normalization))
			return vector_after_normalization 
	    
	def weightCalculator(self, normalMatrix):#计算最终指标对应的权重值
		#layers weight calculations.
		listlen = len(normalMatrix) -1
		layerWeights = list()
		while listlen > -1:
			sum = float()
			for i in normalMatrix:
				sum+= i[listlen]
			sumAverage = round(sum / len(normalMatrix),3)
			layerWeights.append(sumAverage)
			listlen-=1
		return layerWeights
import csv
import numpy as np
import tensorflow as tf
def main():#这里需要确定指标的规模即多少个一级指标，多少个二级指标，这样才能确定要计算多少个对比矩阵
	array1=[]
	array2=[]
	def define_structure():
		level_structure = []
		level = int(input("请输入指标的级数："))#输入比如说这是个三级指标体系
		level0 = input("请输入一级下指标的个数：")
		level.append(level0)
		level2 = []
		for i in range(level):#每一级指标下有多少具体的指标个数
			rate_num = input("请输入" +str(i)+ "层下指标的个数：")
			#level2.append(rate_num)
			for j in range(rate_num ):
				two_level_for_one = int(input("请输入第" +str(i)+ " 个一级指标对应的下级指标的个数："))
				level_structure.append(two_level_for_one )
		return level_structure
	n = level_structure
	def creat_matrix(n):
		for i in n:
			length = input("请输入指标对比矩阵的阶数：")
			length = int(length)
			count=0
		for i in range(length):
            for j in range(length):
				count += 1
				x = input("请输入指标对比矩阵的第"+str(count)+ " 个元素：")
				x = float(x)
				array1.append(x)
        for i in range(length*length):
			if (i+1)%length==0:
				array2.append(array1[i-length+1:i+1])
        print(array2)
    array2=np.mat(array2)
    a=AHP(array2)
    max_val,max_vector = a.get_tezheng(array2)
    RI= a.RImatrix(length)
    flag = a.test_consitstence(max_val,RI)
	if flag:
        weight = a.normalize_vector(max_vector)
main()
