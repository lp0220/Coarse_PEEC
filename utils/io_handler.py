import numpy as np
import os


def load_node_data(filepath, scale):
    """
    加载节点数据
    格式要求: 第一行 'N_N = 数量'，后续行为 'x y z size'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到节点文件: {filepath}")

    with open(filepath, 'r') as f:
        lines = f.readlines()
        # 解析第一行获取节点总数
        n_n = int(lines[0].split()[-1])
        points = np.zeros((n_n, 3))
        node_sizes = np.zeros(n_n)

        for i, line in enumerate(lines[1:n_n + 1]):
            parts = line.split()
            # 读取坐标并进行缩放转换
            points[i] = np.array(parts[:3], dtype='float64') / scale
            # 读取节点尺寸并缩放
            node_sizes[i] = float(parts[-1]) / scale

    return points, node_sizes


def load_branch_data(filepath, node_sizes):
    """
    加载支路数据
    格式要求: 第一行 'N_B = 数量'，后续行为 'node1 node2'
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"找不到支路文件: {filepath}")

    with open(filepath, 'r') as f:
        lines = f.readlines()
        n_b = int(lines[0].split()[-1])
        connects = np.zeros((n_b, 2), dtype="int")
        branch_sizes = np.zeros(n_b)

        for i, line in enumerate(lines[1:n_b + 1]):
            parts = line.split()
            # 存储连接关系 (注意索引转换)
            n1_idx, n2_idx = int(parts[0]), int(parts[1])
            connects[i] = [n1_idx, n2_idx]
            # 支路尺寸通常取两端节点的平均值
            branch_sizes[i] = (node_sizes[n1_idx - 1] + node_sizes[n2_idx - 1]) / 2.0

    return connects, branch_sizes


def save_result(matrix, filename, header_text):
    """保存计算矩阵结果"""
    np.savetxt(filename, matrix, fmt='%.6e', header=header_text)
    print(f"结果已保存至: {filename}")