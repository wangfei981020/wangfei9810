# 在学习神经网络时，除了了解其基本结构外，如何定义和构建一个神经网络模型是接下来的重要步骤。在本篇中，我们将通过 PyTorch 这个深受欢迎的深度学习框架，来学习如何定义一个基本的神经网络模型。

# 定义模型的基本步骤
# 在 PyTorch 中，定义一个神经网络模型主要涉及到以下几个步骤：

# 导入所需的库：
# 首先，我们需要导入相关的 PyTorch 库。

# 创建模型类：
# 在 PyTorch 中，神经网络模型通常是通过继承 torch.nn.Module 类来定义的。

# 定义网络层：
# 在模型的构造函数中定义需要的网络层，例如全连接层、卷积层等。

# **实现前向传播方法 forward**：
# 定义如何将输入数据通过网络层进行转换。

# 导入所需的库
import torch
import torch.nn as nn
import torch.optim as optim

# 创建模型类
# __init__ 方法用于定义网络的层，而 forward 方法定义了如何通过这些层进行前向传播
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size,output_size):
        super(SimpleNN, self).__init__()
        # 定义全连接层
        self.fc1 = nn.Linear(input_size, hidden_size)# 隐藏层
        self.fc2 = nn.Linear(hidden_size, output_size) # 输出层

    def forward(self, x):
        # 前向传播
        x = torch.relu(self.fc1(x)) # 使用 ReLU 激活函数
        x = self.fc2(x)
        return x
    
# 3. 定义网络层
# 在 __init__ 方法中，我们定义了两个全连接层：

# self.fc1：输入层到隐藏层。
# self.fc2：隐藏层到输出层。
# 隐藏层的神经元数量由 hidden_size 参数决定。

# 4. 实现前向传播
# 在 forward 方法中，我们首先将输入数据 x 传递给第一层 fc1，得到隐藏层的输出，然后使用 ReLU 激活函数进行非线性映射。最后，将隐藏层的输出传递给第二层 fc2，得到最终的输出。

input_size = 10
hidden_size = 5
output_size = 2

# 实例模型
model = SimpleNN(input_size, hidden_size, output_size)

# 创建一个随机输入数据（例如，批大小为 1）
input_data = torch.randn(1, input_size)

# 进行前向传播
output_data = model(input_data)

print('Output: ', output_data)