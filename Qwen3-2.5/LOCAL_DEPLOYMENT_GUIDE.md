# Qwen2.5-0.5B GGUF 本地部署指南

## 项目状态

### 模型文件
- **路径**: `./local_model/qwen2.5-0.5b-instruct-q5_0.gguf`
- **大小**: 467.75 MB
- **格式**: GGUF (Q5_0量化)
- **状态**: 文件完整，GGUF格式正确

### 可用服务
| 服务地址 | 后端 | 状态 |
|---------|------|------|
| http://localhost:5002 | Hugging Face Inference API | ✓ 运行中 |
| http://localhost:5003 | Hugging Face Inference API (备用) | ✓ 运行中 |

## 本地部署方案

### 方案1: 使用官方llama.cpp (推荐)

#### 前提条件
- C++ 编译器 (Visual Studio 或 MinGW)
- CMake
- Git

#### 步骤
1. **克隆仓库**
   ```bash
   git clone https://github.com/ggml-org/llama.cpp
   cd llama.cpp
   ```

2. **构建 (Windows)**
   ```bash
   # 使用Visual Studio构建
   cmake -B build -G "Visual Studio 17 2022" -A x64
   cmake --build build --config Release
   ```

3. **运行llama-server**
   ```bash
   ./build/Release/llama-server.exe -m ../local_model/qwen2.5-0.5b-instruct-q5_0.gguf -c 2048
   ```

4. **访问**
   - Web界面: http://localhost:8080
   - API: http://localhost:8080/v1/chat/completions

### 方案2: 使用最新版llama-cpp-python

#### 步骤
1. **更新llama-cpp-python**
   ```bash
   pip install --upgrade llama-cpp-python --force-reinstall
   ```

2. **测试模型加载**
   ```python
   from llama_cpp import Llama
   llm = Llama(
       model_path="./local_model/qwen2.5-0.5b-instruct-q5_0.gguf",
       n_ctx=2048,
       n_threads=4
   )
   ```

3. **运行HTTP服务**
   ```bash
   python llama_server.py
   ```

### 方案3: 使用ctransformers库

#### 步骤
1. **安装ctransformers**
   ```bash
   pip install ctransformers
   ```

2. **测试模型加载**
   ```python
   from ctransformers import AutoModelForCausalLM
   llm = AutoModelForCausalLM.from_pretrained(
       "./local_model/qwen2.5-0.5b-instruct-q5_0.gguf",
       model_type="qwen2"
   )
   ```

### 方案4: 下载预编译llama.cpp二进制文件

1. **下载最新版本**
   - 访问: https://github.com/ggml-org/llama.cpp/releases
   - 下载: `llama-server-windows-x64.zip`

2. **解压并运行**
   ```bash
   ./llama-server.exe -m ./local_model/qwen2.5-0.5b-instruct-q5_0.gguf -c 2048
   ```

## 故障排除

### 常见问题

1. **llama-cpp-python无法加载模型**
   - 原因: 版本不支持Qwen2.5架构
   - 解决: 更新到最新版本或使用官方llama.cpp

2. **编译失败**
   - 原因: 缺少依赖或编译器
   - 解决: 安装Visual Studio Build Tools或MinGW

3. **模型文件损坏**
   - 原因: 下载不完整
   - 解决: 重新下载模型文件

### 验证模型文件

```bash
# 检查文件大小
ls -lh ./local_model/qwen2.5-0.5b-instruct-q5_0.gguf

# 检查GGUF格式
python -c "
with open('./local_model/qwen2.5-0.5b-instruct-q5_0.gguf', 'rb') as f:
    header = f.read(8)
    print(f'GGUF magic: {header.hex()}')
    print(f'Expected: 47475546 (GGUF in little endian)')
"
```

## 性能优化

### CPU优化
- 使用 `-t` 参数指定线程数 (例如: `-t 4`)
- 启用AVX2指令集 (现代CPU都支持)

### 内存优化
- 调整 `-c` 参数控制上下文长度 (默认: 2048)
- 对于4GB内存: `-c 1024`
- 对于8GB内存: `-c 2048`

## 推荐配置

### 基本配置
```bash
# 适合4GB+内存
./llama-server.exe -m ./local_model/qwen2.5-0.5b-instruct-q5_0.gguf -c 2048 -t 4

# 适合8GB+内存
./llama-server.exe -m ./local_model/qwen2.5-0.5b-instruct-q5_0.gguf -c 4096 -t 8
```

### 高级配置
```bash
./llama-server.exe \
  -m ./local_model/qwen2.5-0.5b-instruct-q5_0.gguf \
  -c 4096 \
  -t 4 \
  --temp 0.7 \
  --top-p 0.9 \
  --host 0.0.0.0 \
  --port 8080
```

## 快速启动

如果您不想编译或配置，可以直接使用现有的在线API服务：

- **快速访问**: http://localhost:5002
- **备用服务**: http://localhost:5003

这些服务使用Hugging Face Inference API，无需本地模型即可运行。

## 结论

Qwen2.5-0.5B-GGUF模型文件是完整的，您可以通过以下方式之一在本地部署：

1. **官方llama.cpp** (最推荐，性能最佳)
2. **最新版llama-cpp-python** (最方便)
3. **预编译二进制文件** (无需编译)
4. **在线API服务** (立即可用)

选择最适合您环境的方案，享受本地运行大语言模型的乐趣！
