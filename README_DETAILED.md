# nanoGPT 详细文档

![nanoGPT](assets/nanogpt.jpg)

## 项目简介

nanoGPT 是一个用于训练/微调中等规模 GPT 模型的最简单、最快的仓库。它是 [minGPT](https://github.com/karpathy/minGPT) 的重写版本，优先考虑实用性而非教育性。

**注意：** 自 2025 年 11 月起，nanoGPT 有了一个新的改进版本叫做 [nanochat](https://github.com/karpathy/nanochat)。您很可能想要使用 nanochat 而不是 nanoGPT。本仓库现在已经非常古老且已弃用，但为了记录历史，我将其保留。

## 代码结构

```
nanoGPT-master/
├── assets/           # 图片资源
├── config/           # 配置文件
├── data/             # 数据集和准备脚本
│   ├── openwebtext/  # OpenWebText 数据集
│   ├── shakespeare/  # 莎士比亚数据集
│   └── shakespeare_char/  # 字符级莎士比亚数据集
├── bench.py          # 基准测试脚本
├── configurator.py   # 配置管理
├── model.py          # GPT 模型定义
├── sample.py         # 采样/推理脚本
├── train.py          # 训练脚本
└── README.md         # 原始 README
```

## 核心文件功能

### train.py

训练脚本，可在单个 GPU 上以调试模式运行，也可以在更大的训练运行中使用分布式数据并行 (DDP)。

**主要功能：**
- 支持从头开始训练模型
- 支持从检查点恢复训练
- 支持从 OpenAI GPT-2 权重初始化
- 实现分布式数据并行训练
- 自动保存最佳检查点
- 支持学习率调度和梯度裁剪

### model.py

GPT 模型定义，包含：
- GPT 配置类
- GPT 模型实现
- 从预训练模型加载权重的功能

### sample.py

用于从预训练的 GPT-2 模型或您自己训练的模型中采样生成文本。

### bench.py

用于简单的模型基准测试和性能分析。

## 安装

```bash
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

**依赖项：**
- [pytorch](https://pytorch.org) <3
- [numpy](https://numpy.org/install/) <3
- `transformers` 用于加载 GPT-2 检查点 <3
- `datasets` 用于下载和预处理 OpenWebText <3
- `tiktoken` 用于 OpenAI 的快速 BPE 编码 <3
- `wandb` 用于可选的日志记录 <3
- `tqdm` 用于进度条 <3

## 数据集准备

### 1. 字符级莎士比亚数据集

```bash
python data/shakespeare_char/prepare.py
```

这将在数据目录中创建 `train.bin` 和 `val.bin` 文件。

### 2. 莎士比亚数据集（使用 GPT-2 BPE 分词器）

```bash
python data/shakespeare/prepare.py
```

### 3. OpenWebText 数据集

```bash
python data/openwebtext/prepare.py
```

这将下载并分词 [OpenWebText](https://huggingface.co/datasets/openwebtext) 数据集，创建 `train.bin` 和 `val.bin` 文件。

## 训练过程

### 在 GPU 上训练字符级 GPT

```bash
python train.py config/train_shakespeare_char.py
```

**配置说明：**
- 上下文大小：256 个字符
- 特征通道：384
- Transformer 层数：6
- 每层头数：6
- 训练时间：在 A100 GPU 上约 3 分钟
- 最佳验证损失：1.4697
- 模型检查点保存目录：`out-shakespeare-char`

### 在 CPU 上训练（适用于 Macbook 等设备）

```bash
python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0
```

### 复现 GPT-2 (124M)

在至少 8X A100 40GB 节点上运行：

```bash
torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py
```

**训练细节：**
- 训练时间：约 4 天
- 最终损失：~2.85
- 使用 PyTorch 分布式数据并行 (DDP)

## 微调过程

微调与训练没有区别，只是确保从预训练模型初始化并使用较小的学习率。

### 微调 GPT 模型到莎士比亚数据集

```bash
python train.py config/finetune_shakespeare.py
```

**配置说明：**
- 从 GPT2 检查点初始化
- 较短的训练时间
- 较小的学习率
- 模型检查点保存目录：`out-shakespeare`

## 采样/推理

### 从训练的模型中采样

```bash
python sample.py --out_dir=out-shakespeare-char
```

### 从预训练的 GPT-2 模型中采样

```bash
python sample.py \
    --init_from=gpt2-xl \
    --start="What is the answer to life, the universe, and everything?" \
    --num_samples=5 --max_new_tokens=100
```

### 从文件中提示模型

```bash
python sample.py --start=FILE:prompt.txt
```

## 训练完成的数据

训练完成后，模型检查点会保存在指定的 `out_dir` 目录中。以下是训练数据的组织方式：

### 检查点文件结构

```
out-*/          # 训练输出目录
├── ckpt.pt    # 模型检查点文件
└── ...        # 其他可能的输出文件
```

### 检查点内容

`ckpt.pt` 文件包含以下内容：
- `model`：模型状态字典
- `optimizer`：优化器状态字典
- `model_args`：模型参数
- `iter_num`：训练迭代次数
- `best_val_loss`：最佳验证损失
- `config`：训练配置

### 如何使用训练完成的数据

1. **继续训练**：使用 `--init_from=resume` 参数从检查点继续训练
2. **模型推理**：使用 `sample.py` 脚本从训练的模型中采样
3. **模型分析**：加载模型权重进行分析或修改

## 性能说明

- 默认使用 [PyTorch 2.0](https://pytorch.org/get-started/pytorch-2.0/)，通过 `torch.compile()` 提高性能
- 迭代时间从 ~250ms/迭代减少到 135ms/迭代
- 对于 Apple Silicon Macbooks，添加 `--device=mps` 可以使用芯片上的 GPU 加速训练（2-3 倍）

## 故障排除

- 如果遇到与 PyTorch 2.0 相关的错误，尝试添加 `--compile=False` 标志
- 如果内存不足，尝试减小模型大小或 `block_size`（上下文长度）
- 对于多节点训练，如果没有 Infiniband 互连，在启动命令前添加 `NCCL_IB_DISABLE=1`

## 基准测试

OpenAI GPT-2 检查点在 OpenWebText 上的基准测试结果：

| 模型 | 参数 | 训练损失 | 验证损失 |
|------|------|----------|----------|
| gpt2 | 124M | 3.11 | 3.12 |
| gpt2-medium | 350M | 2.85 | 2.84 |
| gpt2-large | 774M | 2.66 | 2.67 |
| gpt2-xl | 1558M | 2.56 | 2.54 |

**注意：** GPT-2 是在（封闭的、从未发布的）WebText 上训练的，而 OpenWebText 只是这个数据集的最佳开放复现。这意味着存在数据集域差距。事实上，使用 GPT-2 (124M) 检查点并直接在 OWT 上微调一段时间，损失会下降到 ~2.85。

## 未来计划

- 研究并添加 FSDP 替代 DDP
- 在标准评估上评估零样本困惑度（例如 LAMBADA、HELM 等）
- 微调微调脚本，当前的超参数不是很好
- 训练期间线性批量大小增加的计划
- 纳入其他嵌入（旋转、alibi）
- 在检查点中分离优化器缓冲区和模型参数
- 围绕网络健康的额外日志记录（例如梯度裁剪事件、幅度）
- 更多关于更好初始化等的研究

## 相关资源

- [Zero To Hero 系列](https://karpathy.ai/zero-to-hero.html)：关于 GPT 和语言建模的视频教程
- [GPT 视频](https://www.youtube.com/watch?v=kCc8FmEb1nY)：如果你有一些语言建模背景，这个视频很受欢迎

## 社区

有关更多问题/讨论，请访问 Discord 上的 **#nanoGPT** 频道：

[![](https://dcbadge.vercel.app/api/server/3zy8kqD9Cp?compact=true&style=flat)](https://discord.gg/3zy8kqD9Cp)

## 致谢

所有 nanoGPT 实验都由 [Lambda labs](https://lambdalabs.com) 的 GPU 提供支持，这是我最喜欢的云 GPU 提供商。感谢 Lambda labs 赞助 nanoGPT！