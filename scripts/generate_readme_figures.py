import os
import numpy as np
import matplotlib.pyplot as plt


def load_nodes(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0].split()[-1])
    arr = np.array([list(map(float, lines[i + 1].split())) for i in range(n)])
    return arr[:, :3], arr[:, 3]


def load_branches(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0].split()[-1])
    arr = np.array([list(map(int, lines[i + 1].split())) for i in range(n)])
    return arr


def draw_geometry(nodes, branches, out_path):
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=140)

    for i, (x, y, _z) in enumerate(nodes, start=1):
        ax.scatter(x, y, c="tab:blue", s=40)
        ax.text(x + 0.2, y + 0.1, f"N{i}", fontsize=8)

    for i, (n1, n2) in enumerate(branches, start=1):
        p1 = nodes[n1 - 1]
        p2 = nodes[n2 - 1]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], "-", c="tab:red", lw=2)
        mx, my = (p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0
        ax.text(mx, my + 0.15, f"B{i}", fontsize=8, color="tab:red")

    ax.set_title("Example PEEC Node/Branch Topology")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(alpha=0.25)
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def draw_matrices(p_path, l_path, out_path):
    p = np.loadtxt(p_path)
    l = np.loadtxt(l_path)

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), dpi=140)

    im0 = axes[0].imshow(p, cmap="viridis")
    axes[0].set_title("Potential Matrix P")
    axes[0].set_xlabel("Node index")
    axes[0].set_ylabel("Node index")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(l, cmap="magma")
    axes[1].set_title("Inductance Matrix L")
    axes[1].set_xlabel("Branch index")
    axes[1].set_ylabel("Branch index")
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(root, "assets", "images")
    os.makedirs(assets_dir, exist_ok=True)

    nodes, _sizes = load_nodes(os.path.join(root, "data", "Node.txt"))
    branches = load_branches(os.path.join(root, "data", "Branch.txt"))

    draw_geometry(nodes, branches, os.path.join(assets_dir, "topology_example.png"))

    p_file = os.path.join(root, "P.txt")
    l_file = os.path.join(root, "L.txt")
    if os.path.exists(p_file) and os.path.exists(l_file):
        draw_matrices(p_file, l_file, os.path.join(assets_dir, "matrix_heatmaps.png"))


if __name__ == "__main__":
    main()

