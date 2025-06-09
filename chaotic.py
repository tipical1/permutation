import numpy as np
from abc import ABC, abstractmethod

class ChaoticMap(ABC):
    def __init__(self, total_steps):
        self.total_steps = total_steps
    @abstractmethod
    def chaotic_map(self, x0):
        pass
class Logistic(ChaoticMap):
    def __init__(self, total_steps):
        super().__init__(total_steps)
    def chaotic_map(self, x0, mu = 4):
    # 使用Logistic映射生成混沌序列
        x = x0
        total_steps = self.total_steps
        result = []
        for _ in range(total_steps):
            x = mu * x * (1 - x)
            result.append(x)
        return result

class Tent(ChaoticMap):
    def __init__(self, total_steps):
        super().__init__(total_steps)
    def chaotic_map(self, x0, beta = 0.499):
        x = x0
        total_steps = self.total_steps
        result = []
        for _ in range(total_steps):
            x = x / beta if x <= beta else (1 - x) /(1 - beta)
            result.append(x)
        return result

class Bernoulli(ChaoticMap):
    def __init__(self, total_steps):
        super().__init__(total_steps)
    def chaotic_map(self, x0, mu = 0.479):
        # x0 取无理数
        x = x0
        total_steps = self.total_steps
        result = []
        for _ in range(total_steps):
            x = x / (1 - mu) if x <= 1 - mu else (x - 1 + mu) / mu
            result.append(x)
        return result

class Henon(ChaoticMap):
    def __init__(self, total_steps):
        super().__init__(total_steps)
    def chaotic_map(self, x0, y0, a=1.4, b=0.3):
        """
        生成 Henon 映射的混沌序列（仅返回 x 分量）
        
        参数：
            x0, y0        : 初始值（种子）
            total_steps   : 所需的迭代步数
            a, b          : Henon 映射参数（默认 a=1.4, b=0.3）

        返回：
            x_sequence    : 长度为 total_steps 的一维序列（x 分量）
        """
        x, y = x0, y0
        x_sequence = []
        total_steps = self.total_steps
        for _ in range(total_steps):
            x_new = 1 - a * x**2 + y
            y_new = b * x
            x, y = x_new, y_new
            x_sequence.append(x)

        return x_sequence
# def gauss(x0, total_steps, alpha = 4.9, beta = -0.58):
#     # 使用Gauss映射生成混沌序列
#     x = x0
#     result = []
#     for _ in range(total_steps):
#         x = np.exp(-alpha * x**2) + beta
#         result.append(x)
#     return result
