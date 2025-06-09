import secrets

def generate_secure_random_bits(filename, num_bits=10240000):
    num_bytes = num_bits // 8  # 每8个比特为1字节
    random_bytes = secrets.token_bytes(num_bytes)  # 生成安全的随机字节序列

    with open(filename, 'wb') as f:
        f.write(random_bytes)

    print(f"已生成 {num_bits} 比特（{num_bytes} 字节）的安全随机数并写入 {filename}")

generate_secure_random_bits("secure_random.bin")

# with open("secure_random.bin", "rb") as f:
#     data = f.read()
#     print(f"文件大小: {len(data)} 字节")
#     print(f"总比特数: {len(data) * 8}")