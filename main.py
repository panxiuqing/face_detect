#coding=utf-8
import cam
import rec
import os, sys, threading

def check(nums, trainer, path, names):
    """检查捕获的图像是否属于数据库中的用户,
    nums: 捕获图像张数,
    trainer: 训练好的数据库,
    path: 临时存放图像路径,
    names: 数据库中的图像和名字的对应字典
    """
    i = 1
    print '开始识别, 接受阈值为：', trainer.maxd #接受阈值
    print path
    while i <= nums:
        filename = str(i) + '.jpg'
        if filename in os.listdir(path):
            index, mind = trainer.recognize(path+filename)
            #识别并返回最接近的用户编号和欧式距离

            print '最接近', index, '号用户, 距离为: ', mind
            if mind < trainer.maxd: #和最接近的用户的欧式距离小于接受阈值
                print "你是" + names[index], ', 接受!'
                trainer.flag = True #标记已识别，用以通知摄像头停止工作
                os.system('rm /tmp/pp1/*.jpg')              #清除临时目录下的文件
                return
            i += 1
    print "!!!未知用户 拒绝"
    os.system('rm /tmp/pp1/*.jpg')

def main():
    """主函数，判断命令行参数并选择相应的动作"""
    trainer = rec.PCA()                                     #用于训练和识别的对象
    if len(sys.argv) == 3 and sys.argv[1] == 'train':
        save_path = './img/'
        if sys.argv[2].isdigit():
            TrainNum = int(sys.argv[2])
        else:
            print '错误的参数作为训练次数'
            return

        os.system('rm ./img/*.jpg')     #清楚图片文件的原有文件
        video = cam.Cam(rec_type = 'face', use_type = 'train')  #摄像头控制对象，识别类型为face，可选eye
                                                                #使用类型为训练（train）
        name_map = video.begin(trainer=trainer, nums = TrainNum)    #训练摄像头返回用户编号和名字的对应字典
        trainer.createDatabase(save_path, TrainNum)                 #对图片进行训练以及创建数据库
        trainer.save_data('./data/')                                #把训练结果存入data文件夹
        f = open('./data/Namemap.data', 'w')                        #把用户编号和名字的对应字典也存入data文件夹
        f.write(str(name_map))
        f.close()
        print "Complete Train"
    elif len(sys.argv) == 2 and sys.argv[1] == 'check':
        trainer.load_data('./data/')                #从data中读出训练好的数据
        f = open('./data/Namemap.data', 'r')        #用户编号和名字字典也读出
        names = eval(f.read())                      #的出的为字符串，转化为字典
        f.close()
        checkNum = 5                                #检查次数为5次，传给check
        temp_path = '/tmp/pp1/'                     #临时文件夹，传给check
        threading.Thread(target=check, args=(checkNum, trainer, temp_path, names,)).start() #创建一个线程，用于在摄像头取图像的同时进行识别
        video = cam.Cam(rec_type = 'face', use_type='check')    #摄像头控制对象，识别类新为face，使用类型为检查（check）
        video.begin(trainer=trainer, path=temp_path, nums=checkNum) #打开摄像头取图像
    else:
        print """错误的参数,
        示例：
        python main.py train 5
        或者
        python main.py check
        """

    return

if __name__ == "__main__":
    main()
