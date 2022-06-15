import matplotlib.pyplot as plot
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import svm
import numpy as np
import pandas as pd
from sklearn import preprocessing
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.model_selection import KFold
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix

#特征工程
'''
dataset= r'data.xlsx' #读取原始数据集
data=pd.DataFrame(pd.read_excel(dataset))
featureData=data.iloc[:,:-1]
corMat = DataFrame(featureData.corr())  #corr 求相关系数矩阵
print(corMat)
writer = pd.ExcelWriter('output.xlsx')
corMat.to_excel(writer,'Sheet1')
writer.save()
plt.figure(figsize=(20, 30))
sns.heatmap(corMat, annot=False, vmax=1, square=True, cmap="Blues",linewidths=0)
plot.show()
'''

#读取文件
dataset= r'11.14.xlsx' #读取特征工程后的Train数据集
data=pd.DataFrame(pd.read_excel(dataset))
#dataset1= r'prediction.xlsx' #读取预测集
#data1=pd.DataFrame(pd.read_excel(dataset1))
'''
#画出所有特征关于目标值的相关系数排名
featureData=data.iloc[:,:15]
corMat = DataFrame(featureData.corr())  #corr 求相关系数矩阵
print(corMat)
writer = pd.ExcelWriter('output1.xlsx')
corMat.to_excel(writer,'Sheet1')
writer.save()
'''
#读取原数据集的描述符特征和目标值
X=data.values[:195,:14]
for i in range(X.shape[1]): #数据归一化
    X[:,[i]] = preprocessing.MinMaxScaler().fit_transform(X[:,[i]])
y=data.values[:195,14]
'''
print(X)
corMat = DataFrame(X)  #corr 求相关系数矩阵
writer = pd.ExcelWriter('normalized.xlsx')
corMat.to_excel(writer,'Sheet1')
writer.save()
'''
'''
#读取预测集prediction的描述符特征
preX=data1.values[:,:]
for i in range(preX.shape[1]): #数据归一化
    preX[:,[i]] = preprocessing.MinMaxScaler().fit_transform(preX[:,[i]])
'''


#读取自定义的训练集和测试集
X=data.values[:140,:14]
for i in range(X.shape[1]):
    X[:,[i]] = preprocessing.MinMaxScaler().fit_transform(X[:,[i]])
y=data.values[:140,14]
testX=data.values[140:195,:14]
for i in range(testX.shape[1]):
    testX[:,[i]] = preprocessing.MinMaxScaler().fit_transform(testX[:,[i]])
testy=data.values[140:195,14]


#选取4种分类算法
clf = RandomForestClassifier(max_depth=4, random_state=0, n_jobs=2)
#clf = svm.SVC(kernel='poly',gamma=5,degree=5)
#clf=ExtraTreesClassifier(n_estimators=10, max_depth=None,min_samples_split=2, random_state=0)
#kernel = 1.0 * RBF([1.0])
#clf=GaussianProcessClassifier(kernel=kernel, warm_start=True)


#使用KFold交叉验证
'''for nk in range(2,13):
 kfolder = KFold(n_splits=nk)
 score=0
 for train, test in kfolder.split(X,y):
   train_data = np.array(data)[train]
   test_data = np.array(data)[test]
   trany=train_data[:,14]
   tranx=train_data[:,:14]
   testx=test_data[:,:14]
   testy=test_data[:,14]
   clf.fit(tranx,trany)
   prey=clf.predict(testx)
   true=0
   for i in range(0,len(testy)):
     if prey[i]==testy[i]:
         true=true+1
   score=true/len(testy)+score
 print(score/nk)'''


#画出ROC曲线
y_score = clf.fit(X, y).predict_proba(testX)
fpr,tpr,threshold = roc_curve(testy, y_score[:, 1])
roc_auc = auc(fpr,tpr)
plt.figure()
lw = 2
plt.figure(figsize=(10,10))
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc) ###假正率为横坐标，真正率为纵坐标做曲线
print(fpr)
print(tpr)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()


#画出混淆矩阵
'''clf.fit(X, y)
prey=clf.predict(testX)
true=0
for i in range(0,len(testy)):
 if prey[i]==testy[i]:
     true=true+1
print(true/55) #accuracy. test dataset has 55 datapoints. 
C = confusion_matrix(testy, prey, labels=[0,1])
plt.imshow(C, cmap=plt.cm.Blues)
indices = range(len(C))
plt.xticks(indices, [0, 1],fontsize=20)
plt.yticks(indices, [0, 1],fontsize=20)
plt.colorbar()
for first_index in range(len(C)):    #第几行
    for second_index in range(len(C)):    #第几列
        plt.text(first_index, second_index, C[first_index][second_index],fontsize=20,horizontalalignment='center')
plt.show()'''