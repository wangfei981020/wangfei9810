import torch


# 张量的索引
# 在PyTorch中，张量的索引与NumPy基本相似。你可以使用[]来访问张量中的元素。以下是一些常见的索引方法。

# 1.一维张量的索引
# 首先创建一个一维张量

tensor1d = torch.tensor([10,20,30,40,50])
print('一维张量: ',tensor1d) 

# 通过索引访问单个元素
# 访问第一个元素(索引0)
print(tensor1d[0])


# 二维张量的索引
# 创建二维张量
tensor2d = torch.tensor([[1,2,3],[4,5,6],[7,8,9]])
print('二维张量: ',tensor2d)
# 在二维张量中，我们可以通过行和列的索引来访问元素：
# 访问第二行第三列的元素
print('第二行第三列的元素结果: ',tensor2d[1,2])

# 使用切片访问部分元素
# 我们可以通过切片访问张量的一部分。例如，获取一维张量的前两个元素：
# 切片获取前两个元素
print(tensor1d[0:2])
# 对于二维张量，我们可以通过切片获取特定的行或列：
# 获取前两行
print(tensor2d[0:2])

# 获取第二列
print(tensor2d[:,1])

# 张量的高级索引
# 1.布尔索引
# 布尔索引允许基于条件选择元素。例如，我们想选择大于30的所有元素：
# 创建一维张量
tensor1d = torch.tensor([10,20,30,40,50])

# 使用布尔索引
result = tensor1d[tensor1d > 30]
print('一维张量布尔索引结果: ',result)

# 花式索引
# 花式索引允许我们通过指定索引列表来选择元素。例如，选择特定位置的元素：
indices = torch.tensor([0,2,4])
result = tensor1d[indices]
print('一维张量花式索引结果: ',result)

# 切片与视图 
# 切片操作返回的是张量的一个“视图”，这意味着对视图进行修改会影响原始张量。例如：
# 创建二维张量
tensor2d = torch.tensor([[1,2,3],[4,5,6],[7,8,9]])
slice_tensor = tensor2d[0:2]
print(slice_tensor)

# 修改切片
slice_tensor[0,0] = 100
print(tensor2d)