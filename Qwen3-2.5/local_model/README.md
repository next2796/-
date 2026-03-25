# Qwen2.5-0.5B 本地部署

## 项目结构

```
local_model/
├── qwen2.5-0.5b-instruct-q5_0.gguf  # GGUF模型文件 (467.75 MB)
├── llama.cpp/                        # llama.cpp源代码
├── llama_server.py                   # Python HTTP服务器 (llama-cpp-python)
├── simple_llama_server.py            # 简化版服务器
├── run_llama_server.py               # llama-server启动器
├── build_llama_cpp.bat               # Windows构建脚本
├── start_server.bat                  # 一键启动脚本
└── README.md                         # 本文件
```

## 快速开始

### 方法一：使用llama-cpp-python（推荐，无需编译）

1. **确保已安装依赖**
   ```bash
   pip install llama-cpp-python flask
   ```

2. **启动服务器**
   ```bash
   python llama_server.py
   ```

3. **访问服务**
   - Web界面: http://localhost:8080
   - API: http://localhost:8080/v1/chat/completions

### 方法二：使用一键启动脚本（Windows）

双击运行 `start_server.bat`，选择启动方式：
- 选项1: 使用llama-cpp-python
- 选项2: 编译llama.cpp（需要Visual Studio）
- 选项3: 使用现有在线服务

### 方法三：编译官方llama.cpp（最佳性能）

1. **确保已安装**
   - Visual Studio Build Tools 或 MinGW
   - CMake

2. **运行构建脚本**
   ```bash
   build_llama_cpp.bat
   ```

3. **启动服务**
   ```bash
   run_llama_server.py
   ```

## 配置参数

### llama_server.py
- `MODEL_PATH`: 模型文件路径
- `N_CTX`: 上下文长度 (默认: 2048)
- `N_THREADS`: 线程数 (默认: 4)
- `PORT`: 服务端口 (默认: 8080)

### llama-server（官方）
```bash
llama-server.exe -m qwen2.5-0.5b-instruct-q5_0.gguf -c 2048 -t 4 --temp 0.7 --top-p 0.9
```

## API使用示例

### 使用curl
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 512
  }'
```

### 使用Python
```python
import requests

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "messages": [{"role": "user", "content": "Hello!"}],
        "temperature": 0.7,
        "max_tokens": 512
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

## 故障排除

### 模型加载失败
1. 检查模型文件是否存在且完整
2. 更新llama-cpp-python: `pip install --upgrade llama-cpp-python`
3. 检查内存是否足够（至少1GB空闲）

### 编译失败
1. 确保已安装Visual Studio Build Tools
2. 确保CMake已添加到PATH
3. 检查是否有足够的磁盘空间

### 端口被占用
修改 `llama_server.py` 中的 `PORT` 变量，或使用其他端口：
```bash
python llama_server.py --port 8081
```

## 性能优化

### CPU优化
- 增加线程数: `-t 8`（根据CPU核心数调整）
- 启用AVX2: 现代CPU自动支持

### 内存优化
- 减少上下文长度: `-c 1024`（适合4GB内存）
- 使用更小的模型量化版本

## 相关链接

- [llama.cpp GitHub](https://github.com/ggml-org/llama.cpp)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Qwen2.5模型](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)

## 许可证

本项目遵循MIT许可证。模型使用遵循Qwen2.5的许可协议。
