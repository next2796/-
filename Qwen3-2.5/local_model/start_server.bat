@echo off
echo ==============================================
echo Qwen2.5-0.5B GGUF Model - 本地服务器启动脚本
echo ==============================================

:: 检查模型文件
if not exist "qwen2.5-0.5b-instruct-q5_0.gguf" (
    echo 错误: 模型文件未找到！
    echo 请确保 qwen2.5-0.5b-instruct-q5_0.gguf 文件在当前目录
    pause
    exit /b 1
)

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Python未安装！
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)

:: 检查依赖
pip list | findstr "flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖...
    pip install --user flask llama-cpp-python
    if %errorlevel% neq 0 (
        echo 依赖安装失败！
        pause
        exit /b 1
    )
    echo 依赖安装成功
)

echo 正在启动服务器...
echo ==============================================
echo 服务器将在 http://localhost:8080 运行
echo 按 Ctrl+C 停止服务器
echo ==============================================

:: 启动服务器
python llama_server.py

pause
