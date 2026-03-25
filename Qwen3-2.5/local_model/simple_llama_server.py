#!/usr/bin/env python3
"""
使用llama-cpp-python创建简单的HTTP服务器来运行本地GGUF模型
无需编译，直接运行
"""
import sys
import os

# 将当前目录添加到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入llama_server模块
from llama_server import app, llm

if __name__ == "__main__":
    print("="*60)
    print("Qwen2.5-0.5B Local Server")
    print("="*60)
    
    if llm:
        print("\n✓ Model loaded successfully!")
        print(f"Web UI: http://localhost:8080/")
        print(f"API: http://localhost:8080/v1/chat/completions")
        print("\nPress Ctrl+C to stop\n")
        app.run(host='0.0.0.0', port=8080, debug=False)
    else:
        print("\n✗ Failed to load model")
        print("\nTrying alternative method...")
        
        # 尝试使用ctransformers
        try:
            from ctransformers import AutoModelForCausalLM
            
            print("Loading with ctransformers...")
            llm = AutoModelForCausalLM.from_pretrained(
                "qwen2.5-0.5b-instruct-q5_0.gguf",
                model_type="qwen2",
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9
            )
            print("✓ Model loaded with ctransformers!")
            print("\nNote: This is a simple wrapper. For full HTTP API, use:")
            print("  http://localhost:5002 (Hugging Face API)")
            
            # 简单的交互式聊天
            print("\n" + "="*60)
            print("Interactive Chat Mode")
            print("="*60)
            print("Type 'exit' to quit\n")
            
            history = []
            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    break
                if not user_input:
                    continue
                
                # 构建对话
                prompt = ""
                for user_msg, bot_msg in history:
                    prompt += f"<|im_start|>user\n{user_msg}<|im_end|>\n"
                    prompt += f"<|im_start|>assistant\n{bot_msg}<|im_end|>\n"
                prompt += f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
                
                # 生成回复
                print("Bot: ", end="", flush=True)
                response = llm(prompt)
                print(response.strip())
                print()
                
                history.append((user_input, response.strip()))
                
        except Exception as e:
            print(f"✗ Failed to load with ctransformers: {e}")
            print("\n" + "="*60)
            print("Please use the existing web services:")
            print("  http://localhost:5002 (Hugging Face API)")
            print("  http://localhost:5003 (Hugging Face API - backup)")
            print("="*60)
