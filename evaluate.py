from math import gcd
from functools import reduce
from permutation import *
from matplotlib import pyplot as plt
from scipy.stats import chisquare, entropy
from collections import Counter
import time

epsilon = 1e-6

def lcm(a, b):
    """计算两个数的最小公倍数"""
    return a * b // gcd(a, b)

def lcm_list(numbers):
    """多个数的最小公倍数"""
    return reduce(lcm, numbers)

def analyze_permutation_cycles(permutation):
    # cycles: 所有不相交的循环列表
    # cycle_lengths: 每个循环的长度
    # length_distribution: 每种长度出现次数的字典
    # total_order: 总阶（最小公倍数）
    N = len(permutation)
    visited = [False] * N
    cycles = []

    for i in range(N):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = permutation[j]
            if len(cycle) > 0:
                cycles.append(cycle)

    cycle_lengths = [len(c) for c in cycles]
    # 统计不同长度的循环个数
    length_distribution = {}
    for length in cycle_lengths:
        length_distribution[length] = length_distribution.get(length, 0) + 1

    # 不同长度循环种数
    num_cycles = len(length_distribution)
    # 总阶为所有循环长度的最小公倍数
    total_order = lcm_list(cycle_lengths)

    return {
        'cycles': cycles,
        'cycle_lengths': cycle_lengths,
        'num_cycles': num_cycles,
        'length_distribution': length_distribution,
        'total_order': total_order
    }



def average_order_over_seeds_general(map_type, N, M=1000, num_seeds=50):
    orders = []
    rng = np.random.default_rng(seed=42)
    seeds = rng.uniform(epsilon, 1 - epsilon, size=num_seeds)

    for x0 in seeds:
        while is_bad_seed(map_type, x0):
            x0 = rng.uniform(epsilon, 1 - epsilon)
        perm = permutation(map_type, x0, N, M)
        analysis = analyze_permutation_cycles(perm)
        orders.append(analysis['total_order'])

    avg_order = sum(orders) / len(orders)
    return avg_order

def analyze_permutation(map_type, perm, x0):
    size = len(perm)
    results = {}
    
    # 1. 位置分布分析
    positions = np.arange(size)
    diff = positions - perm
    results['mean_diff'] = np.mean(diff)
    results['std_diff'] = np.std(diff)
    
    # 2. 汉明距离分析
    identity = np.arange(size)
    hamming_dist = np.sum(perm != identity) / size
    results['hamming_dist'] = hamming_dist
    
    # 3. 自相关分析
    autocorr = np.correlate(perm, perm, mode='full')
    autocorr = autocorr[len(autocorr)//2:]
    autocorr = autocorr / autocorr[0]  # 归一化
    results['autocorr'] = autocorr
    
    # 4. 差分分析
    perturbed_table = permutation(map_type, x0 + 1e-10, size, M=1000)  # 补充M参数
    diff_rate = np.sum(perm != perturbed_table) / size
    results['diff_rate'] = diff_rate
    
    # 5. 熵分析
    # 置换表应为0~N-1的排列，故熵值应接近理论最大值
    entropy_value = entropy(perm)
    results['entropy'] = entropy_value
    
    # 6. 均匀性检验
    observed = np.bincount(perm, minlength=size)
    chi2, p_value = chisquare(observed)  # 自动计算期望频次
    results['chi2'] = chi2
    results['p_value'] = p_value
    
    return results


def interactive_main_menu():
    """交互式测试入口"""
    maps = ['Logistic', 'Tent', 'Bernoulli']
    colors = {'Logistic': 'skyblue', 'Tent': 'lightcoral', 'Bernoulli': 'hotpink'}
    rng = np.random.default_rng(seed=42)
    while True:
        print("\n=== 混沌置乱测试平台 ===")
        print("1. 测试循环圈结构（循环圈个数，长度，和阶）")
        print("2. 生成平均阶-N对比图表")
        print("3. 混沌置乱的其他分析（位置分布分析、汉明距离分析、自相关分析、差分分析、熵分析、均匀性检验）")
        print("0. 退出")
        
        choice = input("请选择测试项目 (1-3): ")
        
        if choice == '1':
            # 测试循环圈个数，长度，和阶
            x0 = float(input("请输入初始值 x0（不输入则默认随机初始化）: ") or rng.uniform(epsilon, 1 - epsilon))
            size = int(input("请输入置乱大小 N（不输入则默认为50）: ") or 50)
            for m in maps:
                print(f"\n=== {m} ===")
                perm = permutation(m, x0, size)
                analysis = analyze_permutation_cycles(perm)
                # print(f"所有循环:")
                # for c in analysis['cycles']:
                #     print(c)
                print("\n循环长度有:", analysis['num_cycles'], "种\n循环长度分布:", analysis['length_distribution'])
                print("置乱总阶:", analysis['total_order'])
            
        elif choice == '2':
            # 测试多个映射和不同N值
            N_values = list(range(10, 110, 10))
            orders_by_map = {m : [average_order_over_seeds_general(m, N) for N in N_values] for m in maps}

            # 绘图
            plt.figure(figsize=(12, 7))
            bar_width = 2.5
            for i, m in enumerate(maps):
                offset = i * bar_width
                plt.bar([n + offset for n in N_values], orders_by_map[m], width=bar_width, label=str(m), color=colors[str(m)])

            plt.xlabel('Permutation Size N') # 置乱大小
            plt.ylabel('Average Total Order') # 平均总阶
            plt.title('Comparison of Average Permutation Order vs N for Different Chaotic Maps') # 不同混沌映射的平均总阶与N的比较
            plt.xticks([n + bar_width for n in N_values], N_values)
            plt.legend()
            plt.grid(True, axis='y')
            plt.tight_layout()
            plt.show()
                   
        elif choice == '3':
            # 混沌置乱的其他分析（位置分布分析、汉明距离分析、自相关分析、差分分析、熵分析、均匀性检验）
            x0 = float(input("设定初始值x0（不输入则随机初始化）：") or rng.uniform(epsilon, 1 - epsilon))
            size = int(input("设定置乱表大小（不输入则默认为50）：") or 50)
            for m in maps:
                perm = permutation(m, x0, size)
                # 分析安全性
                analysis = analyze_permutation(m, perm, x0)
                print(f"{m} 置乱表安全性分析（N={size}）:")
                print(f"- 汉明距离: {analysis['hamming_dist']:.4f} (期望接近1)")
                print(f"- 差分率: {analysis['diff_rate']:.4f} (期望>0.5)") 
                print(f"- 熵值: {analysis['entropy']:.4f} bits (理论最大值 {np.log2(size):.4f})")
                print(f"- 卡方检验P值: {analysis['p_value']:.4f} (期望>0.05)")

        elif choice == '0':
            print("测试结束")
            break
            
        else:
            print("无效输入，请重新选择")

if __name__ == "__main__":
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    interactive_main_menu()