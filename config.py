import math

# 物理常数
E0 = 8.85418782e-12  # 真空介电常数
U0 = 4 * math.pi * 1e-7  # 真空磁导率

# 缩放比例：将原始单位转换为米 (例如 39370 代表 mils 转 m)
# 用户可以直接修改此值或在启动时传入
UNIT_SCALE = 39370.0

# 计算参数
DEFAULT_GAUSS_ORDER = 3
DEFAULT_DIV_X = 1
DEFAULT_DIV_Y = 1