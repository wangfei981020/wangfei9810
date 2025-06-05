# import torch
# import torch.nn as nn            # for torch.nn.Module, the parent object for PyTorch models
# import torch.nn.functional as F  # for the activation function

# z = torch.zeros(5,3)
# print(z)
# print(z.dtype)

# # #想要整数而不是浮点数？你可以随时覆盖默认设置
# i = torch.ones((5, 3), dtype=torch.int16)
# print(i)

# # 通常会随机初始化学习权重，通常使用特定的 PRNG 种子来确保结果的可重复性
# torch.manual_seed(1729)
# r1 = torch.rand(2, 2)
# print('A random tensor')
# print(r1)

# r2 = torch.rand(2, 2)
# print('\nA different random tensor.')
# print(r2) # new values

# torch.manual_seed(1729)
# r3 = torch.rand(2, 2)
# print('\nShould match r1:')
# print(r3) # repeats values of r1 because of re-seed


# # PyTorch 张量以直观的方式执行算术运算。形状相似的张量可以相加、相乘等。标量运算会分布到整个张量上
# ones = torch.ones(2, 3)
# print(ones)

# twos = torch.ones(2, 3) * 2 # every element is multiplied by 2
# print(twos)

# threes = ones + twos       # addition allowed because shapes are similar
# print(threes)              # tensors are added element-wise
# print(threes.shape)        # this has the same dimensions as input tensors

# r1 = torch.rand(2, 3)
# r2 = torch.rand(3, 2)
# # uncomment this line to get a runtime error
# # r3 = r1 + r2

# print('--------------------------------------------------------------------')

# # 以下是一些可用的数学运算示例

# r = (torch.rand(2, 2) - 0.5) * 2 # values between -1 and 1
# print('A random matrix, r:')
# print(r)

# # Common mathematical operations are supported:
# print('\nAbsolute value of r:')
# print(torch.abs(r))

# # ...as are trigonometric functions:
# print('\nInverse sine of r:')
# print(torch.asin(r))

# # ...and linear algebra operations like determinant and singular value decomposition
# print('\nDeterminant of r:')
# print(torch.det(r))
# print('\nSingular value decomposition of r:')
# print(torch.svd(r))

# # ...and statistical and aggregate operations:
# print('\nAverage and standard deviation of r:')
# print(torch.std_mean(r))
# print('\nMaximum value of r:')
# print(torch.max(r))


# class LeNet(nn.Module):

#     def __init__(self):
#         super(LeNet, self).__init__()
#         # 1 input image channel (black & white), 6 output channels, 5x5 square convolution
#         # kernel
#         self.conv1 = nn.Conv2d(1, 6, 5)
#         self.conv2 = nn.Conv2d(6, 16, 5)
#         # an affine operation: y = Wx + b
#         self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 5*5 from image dimension
#         self.fc2 = nn.Linear(120, 84)
#         self.fc3 = nn.Linear(84, 10)

#     def forward(self, x):
#         # Max pooling over a (2, 2) window
#         x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
#         # If the size is a square you can only specify a single number
#         x = F.max_pool2d(F.relu(self.conv2(x)), 2)
#         x = x.view(-1, self.num_flat_features(x))
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         x = self.fc3(x)
#         return x

#     def num_flat_features(self, x):
#         size = x.size()[1:]  # all dimensions except the batch dimension
#         num_features = 1
#         for s in size:
#             num_features *= s
#         return num_features

# net = LeNet()
# print(net)                         # what does the object tell us about itself?

# input = torch.rand(1, 1, 32, 32)   # stand-in for a 32x32 black & white image
# print('\nImage batch shape:')
# print(input.shape)

# output = net(input)                # we don't call forward() directly
# print('\nRaw output:')
# print(output)
# print(output.shape)

#1. 随机初始化矩阵 我们可以通过torch.rand()的方法，构造一个随机初始化的矩阵：
import torch

x = torch.rand(4, 3)
print(x)

# 全0矩阵的构建 我们可以通过torch.zeros()构造一个矩阵全为 0，并且通过dtype设置数据类型为 long
# 除此以外，我们还可以通过torch.zero_()和torch.zeros_like()将现有矩阵转换为全0矩阵.
import torch

x = torch.zeros(4, 3, dtype=torch.long)
print(x)

# 张量的构建 我们可以通过torch.tensor()直接使用数据，构造一个张量：

import torch

x = torch.tensor([5.5, 3])
print(x)

# 基于已经存在的 tensor，创建一个 tensor ：

x = x.new_ones(4, 3, dtype=torch.double)
# 创建一个新的全1矩阵tensor，返回的tensor默认具有相同的torch.dtype和torch.device
# 也可以像之前的写法 x = torch.ones(4, 3, dtype=torch.double)
print(x)

x = torch.randn_like(x, dtype=torch.float)
# 重置数据类型
print(x)

# 结果会有一样的size
# 获取它的维度信息
print(x.size())
print(x.shape)


# 常见的构造Tensor的方法：

# 函数                      # 功能

# Tensor(sizes)             # 基础构造函数

# tensor(data)              # 类似于np.array

# ones(sizes)               # 全1

# zeros(sizes)              # 全0

# eye(sizes)                # 对角为1，其余为0

# arange(s,e,step)          # 从s到e，步长为step

# linspace(s,e,steps)       # 从s到e，均匀分成step份

# rand/randn(sizes)         # rand是[0,1)均匀分布；randn是服从N(0，1)的正态分布

# normal(mean,std)          # 正态分布(均值为mean，标准差是std)

# randperm(m)               # 随机排列


# 2.1.3 张量的操作

# 加法操作
y = torch.rand(4, 3)
# print(y)
print(x + y)
# 方式2
print(torch.add(x, y))
# 方式3  in-place，原值修改
y.add_(x)
print(y)

print('-----------------------------------------')
# 索引操作：(类似于numpy) 
# 需要注意的是：索引出来的结果与原数据共享内存，修改一个，另一个会跟着修改。如果不想修改，可以考虑使用copy()等方法

x = torch.rand(4, 3)
print(x)
# 取第二列
print(x[:,1])

y = x[0,:]
y += 1
print(y)
print(x[0, :])# 源tensor也被改了了

# 维度变换 张量的维度变换常见的方法有torch.view()和torch.reshape()，下面我们将介绍第一中方法torch.view()：

x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1 ,8) # -1是指这一维的维数由其他维度决定
print(x.size(), y.size(), z.size())

# 注: torch.view() 返回的新tensor与源tensor共享内存(其实是同一个tensor)，更改其中的一个，另外一个也会跟着改变。
# (顾名思义，view()仅仅是改变了对这个张量的观察角度)

x += 1
print(x)
print(y)

