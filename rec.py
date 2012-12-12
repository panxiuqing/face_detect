#coding=utf-8
import numpy as np
from PIL import Image

class PCA():
    """用于脸的训练和识别"""
    def __init__(self):
        self.Matrix = [] #保存输入的所有脸的矩阵
        self.eigenface = [] #特征脸空间
        self.trainNumber = 0 #训练人数
        self.meanArray = [] #平均脸
        self.projectedImage = [] #差值脸矢量在特征脸空间上的投影
        self.maxd = 0 #阈值
        self.flag = False #标记是否识别
        self.IMAGE_SIZE = (40, 40) #图像统一缩放尺寸

    def save_data(self, path):
        """将训练数据保存到文件"""
        np.save(path + 'Matrix.npy', self.Matrix)
        np.save(path + 'eigenface.npy', self.eigenface)
        np.save(path + 'projectedImage.npy', self.projectedImage)

    def load_data(self, path):
        """从文件中读取训练数据，并计算某些变量"""
        self.Matrix = np.mat(np.load(path+'Matrix.npy'))
        self.eigenface = np.mat(np.load(path+'eigenface.npy'))
        self.meanArray = self.Matrix.mean(0)
        self.projectedImage = np.mat(np.load(path+'projectedImage.npy'))
        x, self.trainNumber = np.shape(self.projectedImage)
        self.maxd = self.get_max()

    def get_imagearray(self, filename):
        """返回灰阶图的单行向量"""
        image = Image.open(filename)
        image = image.resize(self.IMAGE_SIZE)
        grayImage = image.convert('L')
        imageArray =list(grayImage.getdata())
        return imageArray

    def createDatabase(self, path, number):
        """创建训练结果数据库"""
        imageMatrix = [] #图像列表
        for i in range(1, number+1): #对于文件夹中的每个图像
            filename = path+str(i)+'.jpg' #得出文件路径名
            imageArray = self.get_imagearray(filename) #得到单行向量
            imageMatrix.append(imageArray) #加入到图像列表，每行一个图

        imageMatrix = np.mat(imageMatrix) #装换为numpy中的矩阵格式

        self.Matrix = imageMatrix
        self.eigenface = self.eigenfaceCore(imageMatrix) #计算特征脸

        return imageMatrix

    def eigenfaceCore(self, Matrix):
        trainNumber, perTotal = np.shape(Matrix) #图像个数和每个图像大小
        meanArray = Matrix.mean(0) #平均脸，按列取平均
        diffMatrix = Matrix - meanArray #差值脸
        C = diffMatrix * diffMatrix.T #SVD，得到trainNumber * trainNumber的矩阵
        eigenvalues, eigenvectors = np.linalg.eig(C) #特征值和特征向量

        """去除<0.99"""
        eigenvector_list = eigenvectors.T.tolist()
        eigenvalues_list = eigenvalues.tolist() #把特征值和特征向量都转化为列表
        vlist = []
        for i in range(0, trainNumber):
            if eigenvalues[i] < 0.99: 
                vlist.append(i) #得到特征值小于0.99的位置
        for i in vlist:
            eigenvector_list.pop(i)
            eigenvalues_list.pop(i) #删除小于0.99的特征值及对应的特征向量
        eigenvectors = np.array(eigenvector_list).T #特征值转换为向量
        eigenvalues = np.mat(eigenvalues_list) #特征向量转换为矩阵

        eigenfaces = diffMatrix.T * eigenvectors
        eigenfaces = np.array(eigenfaces) / np.sqrt(eigenvalues) #特征脸空间

        self.trainNumber = trainNumber
        self.meanArray = meanArray
        self.projectedImage = eigenfaces.T * diffMatrix.T #差值脸在特征脸空间上的投影
        self.maxd = self.get_max() #计算阈值
        return eigenfaces

    def get_max(self):
        """计算阈值的函数
        投影中任意两列的差值的范数的最大值的一半"""
        maxd = 0
        for i in range(0, self.trainNumber):
            for j in range(i, self.trainNumber):
                norm = np.linalg.norm(self.projectedImage[:,i] - self.projectedImage[:,j])
                if maxd < norm:
                    maxd = norm
        return maxd / 2

    def recognize(self, testImage):
        """识别函数"""
        testImageArray = self.get_imagearray(testImage)
        testImageArray = np.array(testImageArray) #取得测试图像单行向量

        diffTestImage = testImageArray - self.meanArray #测试图像和平均脸的差值脸
        diffTestImage = np.mat(diffTestImage)

        projectedTestImage = self.eigenface.T * diffTestImage.T #投影到特征脸空间

        """欧式距离计算和每个用户脸的距离"""
        distance = []
        for i in range(0, self.trainNumber):
            q = self.projectedImage[:,i]
            temp = np.linalg.norm(projectedTestImage - q)
            distance.append(temp)

        """得到最小距离以及对应的用户编号"""
        minDistance = min(distance)
        index = distance.index(minDistance)

        return index+1, minDistance
