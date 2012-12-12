# 基于PCA算法的脸部识别程序
实验环境: UBUNTU 12.04

依赖: Python2.7, numpy, OpenCV, python-opencv, PIL

## 说明

### 使用说明

- 如果有多个摄像头，可能需要修改 **cam.py** 中:

```
...
cap = cv.CaptureFromCAM(-1)
...
```

把``-1``修改为代表你需要的摄像头的值

- 基本使用：
    + 训练: ``python main.py train 3``，3 为需要训练的人数
    + 识别: ``python main.py check``，因为没有把一些部分做完整，这里需要先在 */tmp/* 目录下建立一个名为 *pp1* 的文件夹。当然，你可以修改源代码使之更完善。

### 补充说明
- 阈值设置还不够合理，计算出的阈值现在还偏大，不能有效拒绝，可以自行调整，在 **rec.py** 中的 ``PCA.get_max()`` 函数里。

- 还可以加入 2DPCA 算法
