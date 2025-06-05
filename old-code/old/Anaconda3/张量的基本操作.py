import torch


a = torch.tensor([[1, 2], [3, 4]])
b = torch.tensor([[5, 6], [7, 8]])


# 张量加法
c = a + b
print('张量加法结果: \n', c)

# 张量减法
d = a - b
print('张量减法结果: \n',d)

# 元素乘法
e = a * b
print('张量元素乘法结果: \n', e)

# 矩阵乘法
f = torch.mm(a, b)
print('张量矩阵乘法结果: \n',f)

# 张量的转置
# 张量的转置是将行和列进行交换。可以使用torch.transpose或.t()方法实现。

g = a.t()
print('张量转置结果: \n',g)

# 张量的连接
# 对于多个张量，可以使用torch.cat()函数进行连接。这里我们以沿着行和列进行连接为例。
h = torch.tensor([[9,10],[11,12]])
concat_dim0 = torch.cat((a,h),dim=0) # 沿着行 (第一维) 连接
concat_dim1 = torch.cat((a,h),dim=1) # 沿着列 （第二维） 连接

print('沿着行连接结果: \n', concat_dim0)
print('沿着列连接结果: \n', concat_dim1)

# 张量的数值统计
# PyTorch提供了多种函数以获取张量的统计信息，例如：求和，均值，方差等。
sum_a = torch.sum(a)
mean_a = torch.mean(a.float()) # 要求转换为浮点型
std_a = torch.std(a.float())

print('张量的和: ',sum_a)
print('张量的均值: ', mean_a)
print('张量的方差: ',std_a)