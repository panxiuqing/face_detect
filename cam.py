#coding=utf-8
import cv, time

class Cam():
    """摄像头控制类"""
    def __init__(self, rec_type='face', use_type='train'):
        haar_dir = '/usr/share/opencv/haarcascades/'
        types = {'face': haar_dir + 'haarcascade_frontalface_alt.xml',
                'face2': haar_dir + 'haarcascade_frontalface_alt2.xml',
                'eye': haar_dir + 'haarcascade_eye.xml'
                } #可选的抓取
        if rec_type in types.keys():
            self.fhc = cv.Load(types.get(rec_type))
        else:
            print "Wrong rec_type"

        self.use_type = use_type

    def begin(self, trainer, path='./img/', nums=10, T = 40, minsize=(100, 100)):
        cap = cv.CaptureFromCAM(-1) #创建摄像头对象
        frames = nums * T #接受帧数，每T帧截取一次
        i = 0
        face = [] #从图像中截取的子图像脸
        name_map = {} #用户编号及对应的名字
        while i < frames:
            img = cv.QueryFrame(cap) #帧队列中取出一帧
            faces = cv.HaarDetectObjects(img, self.fhc, cv.CreateMemStorage(), 1.2, 3, 0, minsize) #寻找脸，opencv提供的函数，寻找框的大小间隔为3，最小框大小为100*100，提高寻找速度
            i += 1
            for (x, y, w, h), n in faces: #对于寻找到的脸
                cv.Rectangle(img, (x, y), (x+w, y+h), 255) #用矩形框出
                face = cv.GetSubRect(img, (x, y, w, h)) #将脸部分取出
            faces = ()
            cv.ShowImage("Camera", img) #显示图像
            cv.WaitKey(10)
            if trainer.flag: #如果已经识别出
                break
            if i % T == 0: #每隔T帧
                if face == []: #若找不到脸
                    print "移动脸的位置，以便摄像头可以完整捕捉到！"
                    i -= T
                else:
                    cv.SaveImage(path+str(i/T)+'.jpg', face) #将找到的
#脸部分保存
                    print '正在保存图片......'
                    time.sleep(0.5)
                    if self.use_type == 'train': #如果为训练模式下，要求用户输入名字
                        name_map[i/T] = raw_input('输入该图片对应的用户名:')
            face = []

        cv.DestroyWindow('Camera')
        return name_map
