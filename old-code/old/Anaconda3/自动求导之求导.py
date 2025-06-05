
# 自动求导之求导的基本概念

# 什么是求导
# 在数学中，求导是描述一个函数在某一点的变化率的工具，给定一个函数 f(x),其导数 f'(x) 表示当x 发生微小变化时，f(x) 变化的速率，导数不仅用于描述变化，也用于优化问题，比如最小化损失函数

# 例如对于一个简单的线性函数：

# f(x) = 2x +1

# 我们可以直接求导得到: f'(x) = 2


# 自动求导

import torch

# 定义张量并启用梯度计算
x = torch.tensor(2.0,requires_grad=True)
# 定义一个函数

y = x ** 3 + 5 *x ** 2 + 10

# 执行反向传播
y.backward()

# 查看梯度
print(f"f(x) = {y.item()} at x = {x.item()}")
print(f"f'(x) = {x.grad.item()}")


# 使用torch.autograd实现自动求导 

# 什么是torch.autograd？
# torch.autograd是PyTorch中用于实现自动求导的核心包。它能够根据操作记录自动计算梯度，这使得我们可以轻松地进行反向传播（Backpropagation），进而优化模型。在此过程中，torch.autograd会构建一个计算图，图中的节点是张量，而边则表示它们之间的操作关系。

# 使用自动求导的基本步骤
# 使用自动求导的基本步骤
# 在使用torch.autograd时，主要的步骤如下：

# 创建张量：我们需要先创建需要计算梯度的张量，并设置其属性requires_grad=True。
# 构建计算图：对创建的张量进行各种操作以生成新张量。
# 反向传播：通过调用.backward()方法自动计算梯度。
# 访问梯度：可以通过.grad属性来访问计算得到的梯度。
# 案例：简单的线性回归

# 为了更好地理解torch.autograd的实现，我们通过一个简单的线性回归案例来演示自动求导过程。 

import torch
import numpy as np
import matplotlib.pyplot as plt

# 设置随机种子
torch.manual_seed(42)

# 生成数据
x = torch.linspace(0,1,100).reshape(-1,1) # 100个数据点
y = 2*x + 1 + torch.randn(x.size()) * 0.1 # y = 2x +1 +噪声

# 可视化数据
plt.scatter(x.numpy(),y.numpy(), color='blue')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Generated Data')
plt.show()

# 构建模型
# 接下来，我们构建一个简单的线性回归模型。这里我们使用torch.nn.Linear来创建一个线性层。
import torch.nn as nn

# 定义线性模型
model = nn.Linear(1,1) # 输入是1维，输出也是1维

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(),lr=0.01)
# 训练模型

# 现在，我们将进行模型的训练。在每个训练周期中，我们需要执行以下步骤：

# 正向传播：计算预测值。
# 计算损失：使用损失函数计算损失。
# 反向传播：调用.backward()来计算梯度。
# 更新参数：使用优化器更新模型参数。
# 以下是训练过程的代码：

num_epochs = 200

for epoch in range(num_epochs):
    # 正向传播
    outputs = model(x) # 计算预测
    loss = criterion(outputs, y) # 计算损失

    # 反向传播
    optimizer.zero_grad() # 清零之前的梯度
    loss.backward() # 计算梯度
    optimizer.step() # 更新参数

    if (epoch+1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')
# 可视化结果
# 训练完成后，我们可以可视化模型的预测结果：
with torch.no_grad(): # 在这个上下文中不需要计算梯度
    predicted = model(x)

plt.scatter(x.numpy(),y.numpy(),color='blue')
plt.plot(x.numpy(),predicted.numpy(),color='red',linewidth=2)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression Result')
plt.legend(['Predicted','Original'])
plt.show()