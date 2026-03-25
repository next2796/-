#!/usr/bin/env python3
"""
运行llama-server来本地部署Qwen2.5-0.5B-GGUF模型
"""
import subprocess
import os
import sys
import glob

# 配置
MODEL_PATH = "qwen2.5-0.5b-instruct-q5_0.gguf"
LLAMA_CPP_DIR = "llama.cpp"
HOST = "0.0.0.0"
PORT = 8080

def find_llama_server():
    """查找llama-server可执行文件"""
    possible_paths = [
        os.path.join(LLAMA_CPP_DIR, "build", "bin", "Release", "llama-server.exe"),
        os.path.join(LLAMA_CPP_DIR, "build", "bin", "llama-server.exe"),
        os.path.join(LLAMA_CPP_DIR, "build", "Release", "llama-server.exe"),
        "llama-server.exe",
        "./llama-server.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✓ Found llama-server: {path}")
            return path
    
    return None

def check_model():
    """检查模型文件"""
    if not os.path.exists(MODEL_PATH):
        print(f"✗ Model file not found: {MODEL_PATH}")
        return False
    
    size_mb = os.path.getsize(MODEL_PATH) / 1024 / 1024
    print(f"✓ Model file found: {MODEL_PATH}")
    print(f"  Size: {size_mb:.2f} MB")
    return True

def run_llama_server(llama_server_path):
    """运行llama-server"""
    cmd = [
        llama_server_path,
        "-m", MODEL_PATH,
        "--host", HOST,
        "--port", str(PORT),
        "-c", "2048",      # 上下文长度
        "-n", "512",       # 最大生成长度
        "--temp", "0.7",
        "--top-p", "0.9",
        "-t", "4"          # 使用4个线程
    ]
    
    print("\n" + "="*60)
    print("Starting llama-server...")
    print("="*60)
    print(f"Command: {' '.join(cmd)}")
    print(f"\nWeb UI: http://localhost:{PORT}/")
    print(f"API: http://localhost:{PORT}/v1/chat/completions")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error running server: {e}")
        return False
    
    return True

def main():
    print("="*60)
    print("Qwen2.5-0.5B Local Deployment with llama.cpp")
    print("="*60)
    
    # 检查模型
    if not check_model():
        print("\n✗ Please ensure the model file is in the current directory")
        print("  Expected: qwen2.5-0.5b-instruct-q5_0.gguf")
        sys.exit(1)
    
    # 查找llama-server
    llama_server = find_llama_server()
    
    if not llama_server:
        print("\n" + "="*60)
        print("llama-server not found!")
        print("="*60)
        print("\nPlease build llama.cpp first:")
        print("\nOption 1: Run the build script (if you have Visual Studio)")
        print("  build_llama_cpp.bat")
        print("\nOption 2: Download pre-built binaries")
        print("  1. Visit: https://github.com/ggml-org/llama.cpp/releases")
        print("  2. Download: llama-server-windows-x64.zip")
        print("  3. Extract to this directory")
        print("\nOption 3: Use the existing web services")
        print("  http://localhost:5002 (Hugging Face API)")
        print("  http://localhost:5003 (Hugging Face API - backup)")
        print("="*60)
        sys.exit(1)
    
    # 运行服务
    run_llama_server(llama_server)

if __name__ == "__main__":
    main()
