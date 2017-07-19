README
===========================

* CVPR2017 
* [Zhong Z, Zheng L, Cao D, et al. Re-ranking Person Re-identification with k-reciprocal Encoding[J]. 2017.](https://arxiv.org/abs/1701.08398)
* [原始matlab代码](https://github.com/zhunzhong07/person-re-ranking/blob/master/evaluation/utils/re_ranking.m "悬停显示")
* python重写代码

### `API`
```Java
re_ranking(probFea,galFea,k1,k2,lambda_value, MemorySave = False, Minibatch = 2000)
	return final_dist
```

### probFea
    所有probe图像的feature，shape=[probe_num,feature_length],例如market1501的probe_num就是3368，feature_length是特征的维度

### galFea
    所有gallery图像的feature，shape=[gallery_num,feature_length],例如market1501的gallery_num就是19732，feature_length是特征的维度

### k1,k2
    k1,k2为两个整型参数，其中k1>k2，论文中使用k1=20,k2=6

### lambda_value
    lambda_value为jaccord距离和原始距离的加权数，论文使用0.3
    
### GPU_mode
    是否使用GPU计算距离，数据量越大使用GPU模式节省时间越多，默认为使用
    
### MemorySave
    是否已使用节约内存模式，如若使用则以增加计算时间为代价节约内存，默认为不使用节约内存模式，两万张图片约使用5GB内存，内存使用量按照数量平方增长

### Minibatch
    计算距离矩阵的最小切片大小，通过设置Minibatch可以精确的操作内存，默认值为2000

### final_dist 
    返回最终的距离final_dist矩阵，shape=[probe_num,gallery_num]，对于market1501就是一个3368*19732的矩阵
    即每张probe图片和所有gallery图片的re_ranking之后的距离，这个距离用于之后的检索排序

### `资源消耗测试（market1501数据集）`
原版的MATLAB程序：时间消耗5min，内存消耗10.98GB（float32)

重写Python程序：时间消耗17min，内存消耗5.36GB(float16)，时间耗时主要集中算距离这一步，用了15min，MATLAB对矩阵乘法做了大量优化

### `精度分析`
因为我使用float16类型，所有和原始的MATLAB版本在小数点第四位会略微有点差别

### `效果分析`
在market1501数据集我自己写的测试脚本上涨了5~10个点



