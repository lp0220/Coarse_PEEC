import numpy as np
import sys
import config
from core.kernels import cal_p_self, cal_p_oth, cal_l_oth_approx
from core.solver import PEECSolver
from utils.geometry import get_branch_info, split_grid
from utils.io_handler import load_node_data, load_branch_data, save_result


def main(scale=config.UNIT_SCALE):
    print(f"--- PEEC Solver 启动 (当前缩放比: {scale}) ---")

    try:
        points, node_sizes = load_node_data('data/Node.txt', scale)
        connects, branch_sizes = load_branch_data('data/Branch.txt', node_sizes)
        print(f"成功加载: {len(points)} 个节点, {len(connects)} 条支路")
    except Exception as e:
        print(f"数据加载失败: {e}")
        return

    num_nodes = len(points)
    num_branches = len(connects)

    # 2. 计算电位系数矩阵 P
    print("正在计算 P 矩阵...")
    P = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        P[i, i] = cal_p_self(node_sizes[i])
        for j in range(i + 1, num_nodes):
            P[i, j] = P[j, i] = cal_p_oth(points[i], points[j], node_sizes[j])

    # 3. 计算电感矩阵 L
    print("正在计算 L 矩阵 (高精度自感 + 近似互感)...")
    L = np.zeros((num_branches, num_branches))
    solver = PEECSolver(gauss_order=config.DEFAULT_GAUSS_ORDER)

    for i in range(num_branches):
        # 计算对角线：高精度自感
        region, axis, dims = get_branch_info(i, connects, branch_sizes, points)
        subs = split_grid(region, config.DEFAULT_DIV_X, config.DEFAULT_DIV_Y)
        # 仅针对自感进行计算 (即 j = i)
        total_A1 = 0.0
        for s_i in subs:
            # 自感的相互作用是支路自身网格之间的积分
            for s_j in subs:
                _, t_a1, _, _ = solver.compute_pair_integral(s_i, s_j, axis, axis, dims, dims)
                total_A1 += t_a1

        # 仅填充对角线元素 (L[i, i])
        L[i, i] = total_A1

        # 计算非对角线：近似互感
        for j in range(i + 1, num_branches):
            L[i, j] = L[j, i] = cal_l_oth_approx(points, connects[i], connects[j])

        sys.stdout.write(f"\r进度: {i + 1}/{num_branches}")
        sys.stdout.flush()

    # 4. 保存结果
    np.savetxt('P.txt', P, header='Potential Matrix')
    np.savetxt('L.txt', L, header='Inductance Matrix')
    print("\n计算完成！结果已导出。")


if __name__ == "__main__":
    # 支持从命令行指定缩放比
    # current_scale = float(sys.argv[1]) if len(sys.argv) > 1 else config.UNIT_SCALE
    main(1000)