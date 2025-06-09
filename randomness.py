from math import gcd
from functools import reduce
from permutation import *
from matplotlib import pyplot as plt
import hashlib
from secrets import token_bytes

epsilon = 1e-6

def generate_nist_test_file(output_file, m, num_bits=1024000):
    all_bits = ''
    num_tables = num_bits // 2048  # 计算需要的置换表数量
    rng = np.random.default_rng(seed=42)
    seeds = rng.uniform(epsilon, 1 - epsilon, size=num_tables)

    for x0 in seeds:
        while is_bad_seed(m, x0):
            x0 = rng.uniform(epsilon, 1 - epsilon)
        perm = permutation(m, x0, 256)  # 生成256元素的置换表
        binary_data = perm_to_bin(perm)  # 转换为二进制字符串（1024比特）
        all_bits += binary_data

    # 将二进制字符串转换为字节数组
    byte_array = bytearray()
    for i in range(0, len(all_bits), 8):
        byte = int(all_bits[i:i+8], 2)
        byte_array.append(byte)

    # 写入二进制文件
    with open(output_file, 'wb') as f:
        f.write(byte_array)
    
    print(f"已生成 {num_bits} 比特的测试文件: {output_file}")

def permute_data(data, permutation):
    """对数据进行置乱"""
    return [data[i] for i in permutation]

def chaotic_secure_random_bits(m, bit_length=10240000):
    # 步骤 1：准备结果容器
    all_bits = ''
    num_blocks = bit_length // 1024  # 每次置换表生成 1024 比特（256 字节）

    for _ in range(num_blocks):
        # 使用新的安全熵源生成混沌系统初值（避免固定 x0）
        seed_bytes = token_bytes(16)
        seed_float = int.from_bytes(hashlib.sha256(seed_bytes).digest(), 'big') % (10**8) / 10**8
        x0 = max(1e-8, min(1 - 1e-8, seed_float))

        # 生成置换表并转为 1024 比特二进制字符串
        perm = permutation(m, x0, 256)
        binary_block = ''.join(format(x, '08b') for x in perm)
        all_bits += binary_block

    # 截取所需长度的位
    all_bits = all_bits[:bit_length]

    # 转为字节并写入文件
    byte_array = bytearray(int(all_bits[i:i+8], 2) for i in range(0, len(all_bits), 8))
    with open('chaotic_random.bin', 'wb') as f:
        f.write(byte_array)

    print(f"已生成 {bit_length} 比特（{bit_length // 8} 字节）的混沌置乱随机序列并保存到 chaotic_random.bin")

# chaotic_secure_random_bits('Logistic', bit_length=10240000)
# 生成测试文件
maps = ['Logistic', 'Tent', 'Bernoulli']
for m in maps:
    generate_nist_test_file(f"{m}.bin", m, num_bits=10240000)