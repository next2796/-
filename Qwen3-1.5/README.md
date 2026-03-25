# Qwen1.5-0.5B ChatBot

基于阿里云通义千问模型的智能对话机器人，使用 Gradio 构建 Web 界面，支持多轮对话。

## 功能特点

- **智能对话**：基于 Qwen1.5-0.5B-Chat 模型，支持多轮对话
- **Web 界面**：使用 Gradio 构建的用户友好界面
- **网络优化**：内置国内镜像，解决 Hugging Face 连接问题
- **自动设备选择**：根据系统环境自动选择 CPU 或 GPU
- **错误处理**：完善的错误处理和重试机制

## 环境要求

- Python 3.9+
- PyTorch
- Transformers
- Gradio
- Requests
- FastAPI (可选)

## 安装依赖

```bash
# 建议在虚拟环境中安装
pip install torch transformers gradio requests fastapi uvicorn
```

## 快速开始

### 方法 1：使用批处理脚本

1. 双击运行 `run_chatbot.bat`
2. 在浏览器中访问：`http://localhost:7860`

### 方法 2：手动运行

```bash
# 在 PowerShell 中运行
& "e:\annaconda\envs\w2v\python.exe" "chatbot_final.py"
```

## 项目结构

```
Qwen3-1.5/
├── chatbot_final.py    # 核心 ChatBot 实现
└── run_chatbot.bat     # 批处理启动脚本
```

## 核心功能

### 1. 模型加载

- 自动从 Hugging Face 下载 Qwen1.5-0.5B-Chat 模型
- 支持国内镜像，解决网络连接问题
- 自动选择设备（CPU 或 GPU）

### 2. 对话推理

- 支持多轮对话
- 构建符合 Qwen 模型要求的对话格式
- 生成自然流畅的回复

### 3. Web 界面

- 使用 Gradio 构建交互式界面
- 支持输入提示词和查看对话历史
- 响应式设计，适配不同设备

## 网络连接优化

项目内置了以下网络连接优化：

- **国内镜像**：使用 https://hf-mirror.com 作为 Hugging Face 国内镜像
- **网络检查**：启动时自动检查网络连接状态
- **错误处理**：包含完整的错误处理和重试机制

## 常见问题

### 1. 无法下载模型

**解决方案**：
- 检查网络连接
- 确保使用了国内镜像
- 尝试手动下载模型到本地

### 2. 运行速度慢

**解决方案**：
- 使用 GPU 加速（如果可用）
- 减少生成的最大 token 数
- 确保系统资源充足

### 3. 内存不足

**解决方案**：
- 使用 CPU 模式运行
- 关闭其他占用内存的程序
- 考虑使用更小的模型

## 技术实现

### 模型加载

```python
# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained(model_path, resume_download=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map=device_map,
    resume_download=True
).eval()
```

### 对话推理

```python
# 构建对话历史
conversation = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
for q, r in history:
    conversation.extend([{'role': 'user', 'content': q}, {'role': 'assistant', 'content': r}])
conversation.append({'role': 'user', 'content': query})

# 生成回复
inputs = tokenizer.apply_chat_template(conversation, add_generation_prompt=True, return_tensors='pt').to(model.device)
outputs = model.generate(input_ids=inputs, max_new_tokens=1024, eos_token_id=tokenizer.eos_token_id, pad_token_id=tokenizer.pad_token_id)
response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
```

### Web 界面

```python
# 创建 Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("# Qwen1.5-0.5B ChatBot")
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="输入消息", placeholder="请输入你的问题...")
    clear = gr.Button("清除对话")
    
    def respond(message, chat_history):
        response = chat_with_model(message, chat_history)
        chat_history.append((message, response))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# 启动 Web 服务
demo.launch(share=False, server_port=7860, server_name="0.0.0.0")
```

## 许可证

本项目基于 MIT 许可证开源。

## 致谢

- [阿里云通义千问](https://www.aliyun.com/product/tongyiqianwen) - 提供基础模型
- [Hugging Face](https://huggingface.co/) - 模型托管和工具
- [Gradio](https://gradio.app/) - Web 界面构建
- [PyTorch](https://pytorch.org/) - 深度学习框架

## 联系方式

如果您有任何问题或建议，欢迎联系我们。