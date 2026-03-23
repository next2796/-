
import torch
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置中文字体
matplotlib.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

ckpt = torch.load('out-shakespeare-char/ckpt.pt', map_location='cpu')
model_state = ckpt.get('model')

# 美化输出参数名称和形状
print("\n模型参数名称与形状（美化输出）：\n" + '-'*40)
param_sizes = []
for idx, (name, param) in enumerate(model_state.items()):
    print(f"{idx+1:02d}. 层名称：{name}\n    参数形状：{param.shape}\n    参数总数：{np.prod(param.shape)}\n")
    param_sizes.append((name, np.prod(param.shape)))
print('-'*40 + "\n共计参数层数：", len(param_sizes))

# 中文图表：参数数量统计
names, sizes = zip(*param_sizes)
plt.figure(figsize=(12, 8))
plt.barh(names, sizes, color='#4e79a7')
plt.xlabel('参数数量', fontsize=14)
plt.title('模型各层参数数量统计', fontsize=16)
plt.tight_layout()
plt.savefig('param_count_cn.png')
plt.show()

# 中文图表：部分权重分布直方图（embedding/linear层）
for name, param in model_state.items():
    if 'weight' in name and len(param.shape) > 1:
        plt.figure(figsize=(10, 5))
        plt.hist(param.cpu().numpy().flatten(), bins=50, color='#f28e2b')
    plt.title(f'{name} 权重分布', fontsize=15)
        plt.xlabel('权重值', fontsize=13)
        plt.ylabel('频数', fontsize=13)
        plt.tight_layout()
        plt.savefig(f'{name}_hist_cn.png')
        plt.show()
        break  # 只绘制一个示例层
print("\n图表已保存为 param_count_cn.png 和部分权重分布图（xxx_hist_cn.png）。\n")
