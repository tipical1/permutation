import numpy as np
from chaotic import *
from matplotlib import pyplot as plt

def permutation(map_type, x0, N, M=1000):
    if map_type == 'Logistic':
        map = Logistic(N+M)
    elif map_type == 'Tent':
        map = Tent(N+M)
    elif map_type == 'Bernoulli':
        map = Bernoulli(N+M)
    elif map_type == 'Henon':
        map = Henon(N+M)
    sequence = map.chaotic_map(x0)
    data = sequence[M:]
    # argsort两次相当于排名: 返回从原索引i排到新位置j的映射
    permutation = np.argsort(np.argsort(data)).tolist()
    return permutation

def plot_permutation(map_type, x0, N, M=1000):
    chaos_seq = permutation(map_type, x0, N, M)
    plt.figure(figsize=(10,6))
    plt.scatter(range(len(chaos_seq)), chaos_seq, 
            s=15, alpha=0.6, edgecolor='k', 
            c=np.linspace(0,1,len(chaos_seq)), 
            cmap='viridis')
    plt.xlabel("Dimension Index", fontsize=12)
    plt.ylabel("Chaotic Value", fontsize=12)
    plt.title(f"Chaotic Sequence Distribution (N={len(chaos_seq)})", fontsize=14)
    plt.colorbar(label='Normalized Index')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def perm_to_bin(permutation):
    # 将置乱表中的每个整数转换为8位二进制字符串，并拼接为一个长字符串
    return ''.join(f'{x:08b}' for x in permutation)

def is_bad_seed(m, x0):
    if m == 'Logistic':
        return x0 in {0, 0.25, 0.5, 0.75, 1}
    elif m == 'Tent' or m == 'Bernoulli':
        return x0 in {0, 1}
    return False
